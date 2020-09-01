import yaml
import os

class Config:
    def __init__(self, config_file_type):
        self.config_file_type = config_file_type
        self.mappings = self.create_mappings()

    def create_mappings(self):
        mappings = {}
        mappings['bank_config_file'] = \
            {'citibank': 'citibank',
             'hdfc': 'hdfc'}
        return mappings

    def _valid_keys(self, key):
        return self.mappings[self.config_file_type][key]

    def get_info(self, key):
        config = self.read_config()
        if self.config_file_type == 'bank_config_file':
            key = self._valid_keys(key)
        return config[key]
        
    def read_config(self):
        current_path =os.path.dirname(os.path.abspath(__file__))
    
        file_mapping = \
            {'bank_config_file': 'bank_conf.yaml',
             'db_file': 'db_conf.yaml'
            }
        config_file = current_path +'/' + file_mapping[self.config_file_type]
        return yaml.load(open(config_file))
