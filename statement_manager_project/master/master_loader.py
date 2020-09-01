import utils
import os
import re

class MasterLoader:
    def __init__(self, bank_config):
        self.bank_config = bank_config

    def run(self):
        sql_engine = utils.create_db_engine('db_file', self.bank_config.get('master_db'))
        file_info = self.get_master_transactions_ddl_dml()
        self.create_master_transactions(self.bank_config.get('patterns'), file_info['ddl'], sql_engine)
        self.update_master_transactions(self.bank_config.get('patterns'), file_info['dml'], sql_engine)
    
    
    
    def get_master_transactions_ddl_dml(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        file_info = {
                'ddl': current_path + self.bank_config.get('master_ddl'), 
                'dml': current_path + self.bank_config.get('master_dml')
                }
    
        return file_info
    
    
    def create_master_transactions(self, pattern, ddl_file, sql_engine):
        utils.execute_sql_file(pattern, ddl_file, sql_engine)
    
    
    def update_master_transactions(self, pattern, dml_file, sql_engine):
        utils.execute_sql_file(pattern, dml_file, sql_engine)


class CategorizeTransactions:
    def __init__(self, bank_config):
        self.bank_config = bank_config
        self.current_path = os.path.dirname(os.path.abspath(__file__))

    def run(self):
        sql_engine = utils.create_db_engine('db_file', self.bank_config.get('stage_db'))
        rows = self.get_transactions(sql_engine)
        self.update_categories(rows, sql_engine)


    def get_transactions(self, sql_engine):
        pattern =  self.bank_config['patterns']
        dml_file = self.current_path + self.bank_config['stage_dml_select_description']
        result = utils.execute_sql_file(pattern, dml_file, sql_engine)
        rows = utils.convert_sql_result_to_dict(result)

        return rows
        
    def update_categories(self, rows, sql_engine):
        match = []
        pattern = self.bank_config['patterns']
        dml_file = self.current_path + self.bank_config['stage_dml_update_categories']
        string_init = [*self.bank_config['regex'].keys()]
        for row in rows:
            category = "unknown"
            info = "unknown"
            for item in string_init:
                if 'contains' in self.bank_config['regex'][item].keys() and \
                        item in row['description']:
                    match.append(item)
                else if row['description'].startswith(item):
                    match.append(item)
            if len(match):
                category = self.return_info(row['description'], match[0])['category']
                info = self.return_info(row['description'], match[0])['info']
            pattern['<CATEGORY>'] = category.strip().rstrip("\\")
            pattern['<INFO>'] = info.strip().rstrip("\\")
            pattern['<ROW_SHA>'] = row['row_sha']
            utils.execute_sql_file(pattern, dml_file, sql_engine)


    def return_info(self, description, match):
        result = {}
        regex_ = self.bank_config['regex'][match]['expression']
        group = self.bank_config['regex'][match]['group']
        result['category'] = self.bank_config['regex'][match]['category']
        result['info'] = 'unknown'
        for regex in regex_:
            matched = re.findall(regex, repr(description))
            if len(matched) and len(matched[0]) >= group + 1:
                result['info'] = matched[0][group]
                return result
        return result
