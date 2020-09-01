import sys
import pandas as pd
from config import *
import CreateArguments as ca
import utils
import camelot
from stage_loader import StageLoader
from master_loader import MasterLoader, CategorizeTransactions

class LoadData:
    def read_pdf(self, pdf_file, path, password, bank_name):
        csv_file = pdf_file.split(".")[0] + ".csv"
        if bank_name=="citibank":
            pdf_data=camelot.read_pdf(path+pdf_file,password=password,flavor='stream',pages='1-end')
        if bank_name=="hdfc":
            pdf_data=camelot.read_pdf(path+pdf_file,password=password,line_scale=40,pages='1-end')
        return pdf_data

    def return_config(self, config_obj, key):
        return config_obj.get_info(key)


    def load_data(self, data_frame, engine, table_name, mode):
        data_frame.to_sql(name=table_name, con=engine, if_exists=mode)

class LoadStatementData(LoadData):

    def run(self):
        args = self.create_cli_args()
        bank_module = utils.import_source_module(args.bank_name, 'clean_raw_data')
        bank_config = utils.get_config('bank_config_file', args.bank_name)
        if args.run_type in ['raw', 'all']:
            pdf_data = super().read_pdf(args.statement_file, args.file_path, args.file_password, args.bank_name)
            clean_data = bank_module.run(pdf_data, bank_config)
            print(clean_data)
            engine = utils.create_db_engine('db_file', bank_config.get('raw_db'))
            super().load_data(clean_data, engine, 'transactions', 'replace')
        if args.run_type in ['stage', 'all']:
            stage_loader = StageLoader(bank_config)
            stage_loader.run()
        if args.run_type in ['master', 'all']:
            master_loader = MasterLoader(bank_config)
            master_loader.run()
        if args.run_type in ['categorize', 'all']:
            categorize_transactions = CategorizeTransactions(bank_config)
            categorize_transactions.run()


    def create_cli_args(self):
        arg_list = [
                   {'argument_name': 'statement_file',
                    'require': True,
                    'help_string': 'Bank Statement pdf file',
                    'verbose': True,
                    'default_value': 'file.pdf',
                    'custome_name': 'statement_file',
                    'data_type': str,
                    'action': 'store'
                    },
                   {'argument_name': 'file_path',
                    'require': True,
                    'help_string': 'Bank Statement pdf file path',
                    'verbose': True,
                    'default_value': '',
                    'custome_name': 'file_path',
                    'data_type': str,
                    'action': 'store'
                    },
                   {'argument_name': 'bank_name',
                    'require': True,
                    'help_string': 'Bank Name: `CITIBANK`, `HDFC`',
                    'verbose': True,
                    'default_value': '',
                    'custome_name': 'bank_name',
                    'data_type': str,
                    'action': 'store'
                    },
                   {'argument_name': 'file_password',
                    'require': True,
                    'help_string': 'Bank Statement pdf file password',
                    'verbose': True,
                    'default_value': None,
                    'custome_name': 'file_path',
                    'data_type': str,
                    'action': 'store'
                    },
                   {'argument_name': 'run_type',
                    'require': True,
                    'help_string': 'raw/stage/master/categorize/all',
                    'verbose': True,
                    'default_value': None,
                    'custome_name': 'run_type',
                    'data_type': str,
                    'action': 'store'
                    },
                   ]
        description = """
                      This program takes the pdf bank statement and
                      inserts it into the database for further analysis
                      """
        program_info = {'program_name': 'Bank Statement Manager',
                        'description': description }
                        
        obj = ca.CreateArguments(arg_list, program_info)
        args = obj.create_cli_arguments()
        return args
        
