import os
import sys
import re
from sqlalchemy import create_engine
from config import *


def import_source_module(bank_name, module_name):
    path = os.path.dirname(os.path.abspath(__file__)).split('/')[0:-1]
    path.extend(('sources', bank_name))
    path = "/".join(path)
    module_imported = import_module(path, module_name)

    return module_imported

def import_module(sys_path, module_name):
    sys.path.append(sys_path)
    module = __import__(module_name)

    return module


def create_db_engine(config_type, database):
    user = get_config(config_type, 'user')
    passwd = get_config(config_type, 'passwd')
    host = get_config(config_type, 'host')
    port = get_config(config_type, 'port')
    credentials = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(user, passwd, host, str(port), database)
    engine = create_engine(credentials, echo=False)

    return engine


def execute_sql_file(patterns, sql_file, sql_engine):
    f = open(sql_file, 'r')
    sql = f.read()
    for re_expression, replacement in patterns.items():
        sql = re.sub(re_expression, replacement, sql)
    with sql_engine.connect() as con:
        result = con.execute(sql)

    return result

def convert_sql_result_to_dict(result):
    return [{column: value for column, value in row.items()} for row in result]

def get_config(config_type, key):
    config_obj = Config(config_type)
    return config_obj.get_info(key)
