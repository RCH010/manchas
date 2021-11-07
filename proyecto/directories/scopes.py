import sys
from utils import Data_types
from directories.directory import Directory


'''
The Scopes_directory class is a directory for all functions (and main)
(inherits from directory)
'''
class Scopes_directory(Directory):
    '''
    Create new scope on the directory
    '''
    def add_new_scope(self, id, return_type, vars_table):
        if self.exists(id):
            print('Error', id ,'al ready exists on the scope directory')
            sys.exit()
        if return_type not in Data_types.values():
            print('Error', 'return type:', return_type ,'is an invalid type for', id)
            sys.exit()
        params = []
        self.dic[id] = { 'vars': vars_table, 'return_type': return_type, 'params': params, 'cont': None }

    def get_vars_table(self, id):
        return self.dic[id]['vars']

    def get_params_table(self, id):
        return self.dic[id]['params']

    '''
    Set the CONT value on the scopes function directory. CONT --> is the quadruple
    counter where the specified function starts
    '''
    def set_func_cont(self, id, cont):
        self.dic[id]['cont'] = cont

    

    def calculate_function_size(self, id):
        vars_table = self.dic[id]['vars'].dic
        params = self.dic[id]['params']
        # TODO: cuando pase los tipos a un int, esto se accedera directamente
        # [# of INTS,       # of FLOATS,        # of BOOLS,     # of CHARS]
        types_counter = [0] * 4

        # cuando haga lo de que los tipos sean numero esto deberá ser:
        # types_counter[param] += 1
        for param in params:
            data_type = TYPES[param]
            types_counter[data_type] += 1
        
        for key, value in vars_table.items():
            var_type = value['type']
            data_type = TYPES[var_type]
            types_counter[data_type] += 1

        self.dic[id]['types_counter'] = types_counter
        print('contador dde tipooos', types_counter)
        


    def print_directory(self):
        for key, value in self.dic.items():
            print()
            print('SCOPE:', key)
            for k, v in value.items():
                if k == 'vars':
                    print('=====VARS======')
                    v.print_directory()
                    print('===============')
                else:
                    print(k, ' -->', v)
            print()

# TODO: remove this... when int, float etc,are now numbers

TYPES = {
    'int': 0,
    'float': 1,
    'bool': 2,
    'char': 3,
}