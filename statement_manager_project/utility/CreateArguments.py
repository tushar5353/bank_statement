import argparse
import textwrap

"""
dict = {'argument_name':'name of the argument',
        'require':true/false,
        'help_string':'helpstring',
        'data_type': 'data type',
        'verbose': true/false,
        'default_value':'default value of the argument if nothing is provided',
        'custom_name': 'custom name provided to an argument',
        'action':'store/store_const/store_true/store_false/append/append_const/count',
        'constant_value':'any constant value if any of the const actions is specified'
        }
"""
class CreateArguments:

    def __init__(self, arguments_list, program_info):
        self.arguments_list = arguments_list
        self.program_name = program_info.get('program_name')
        self.description = program_info.get('description')


    def create_cli_arguments(self):
        parser = argparse.ArgumentParser(
                    prog=self.program_name,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description=textwrap.dedent(self.description))

        for options in self.arguments_list:
            argument_name = "--"+options.get('argument_name')
            help_string = options.get('help_string')
            data_type = options.get('data_type')
            default = options.get('default_value')
            custom_name = options.get('custom_name')
            action = options.get('action')
            constant_value = options.get('constant_value')
            require = options.get('require')
            if action in ['store_const','append_const']:
                parser.add_argument(argument_name, help=help_string,\
                                    const=constant_value, action=action, dest=custom_name)
            else:
                parser.add_argument(argument_name, help=help_string, type=data_type,\
                                     default=default, action=action, dest=custom_name)

        return parser.parse_args()
