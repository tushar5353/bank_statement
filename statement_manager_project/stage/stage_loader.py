import utils
import os

class StageLoader:
    def __init__(self, bank_config):
        self.bank_config = bank_config

    def run(self):
        sql_engine = utils.create_db_engine('db_file', self.bank_config.get('stage_db'))
        file_info = self.get_stage_transactions_ddl_dml()
        self.create_stage_transactions(self.bank_config.get('patterns'), file_info['ddl'], sql_engine)
        self.create_stage_transactions(self.bank_config.get('patterns'), file_info['ddl_tmp'], sql_engine)
        self.update_stage_transactions(self.bank_config.get('patterns'), file_info['dml'], sql_engine)
    
    
    
    def get_stage_transactions_ddl_dml(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        file_info = {
                'ddl': current_path + self.bank_config.get('stage_ddl'), 
                'ddl_tmp': current_path + self.bank_config.get('stage_ddl_tmp'), 
                'dml': current_path + self.bank_config.get('stage_dml')
                }
    
        return file_info
    
    
    def create_stage_transactions(self, pattern, ddl_file, sql_engine):
        utils.execute_sql_file(pattern, ddl_file, sql_engine)
    
    
    def update_stage_transactions(self, pattern, dml_file, sql_engine):
        utils.execute_sql_file(pattern, dml_file, sql_engine)
