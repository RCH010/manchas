import sys
from compiler.utils import Data_types, create_error
from compiler.directories.directory import Directory


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
            create_error(f'{id} already exists on this scope', 'C-29')
        if return_type not in Data_types.values():
            create_error(f'Return type: {return_type} is an invalid type for {id}', 'C-30')
        params = []
        params_ids = []
        self.dic[id] = { 'vars': vars_table, 'return_type': return_type, 'params': params, 'params_ids': params_ids,  'cont': None }

    def get_vars_table(self, id):
        return self.dic[id]['vars']

    '''
    get the params array of received function
    '''
    def get_params_array(self, id):
        return self.dic[id]['params']
    
    '''
    get the params array of received function
    '''
    def get_params_ids_array(self, id):
        return self.dic[id]['params_ids']

    '''
    get the return type of the received function
    '''
    def get_return_type(self, id):
        return self.dic[id]['return_type']

    '''
    Set the CONT value on the scopes function directory. CONT --> is the quadruple
    counter where the specified function starts
    '''
    def set_func_cont(self, id, cont):
        self.dic[id]['cont'] = cont

    def get_func_cont(self, id):
        return self.dic[id]['cont']
    
    '''
    Calculate the number of variables (per type) are used on the given scope. 
    This function will create an array with the totals of variables per type
    where the 1st position are the number of intergers, the 2nd the number of
    floats, then the number of booleans and finally the number of chars.
        [ INTS . FLOATS, BOOLS, CHARS ]
    This array is saved of the given scope with the key of: types_counter
    '''
    def calculate_function_size(self, id):
        vars_table = self.dic[id]['vars'].dic
        params = self.dic[id]['params']
        types_counter = [0] * 4 # Starts array with 0's
        total_size = 0
        for key, value in vars_table.items():
            var_type = value['type']
            item_size = 1
            if ('is_array' in value.keys() and value['is_array']):
                item_size = value['array_size']
            data_type = TYPES[var_type]
            types_counter[data_type] += item_size
            total_size += item_size

        self.dic[id]['types_counter'] = types_counter
        self.dic[id]['total_vars'] = total_size
        
    def get_total_size(self, id):
        return self.dic[id]['total_vars']

    def print_directory(self):
        for key, value in self.dic.items():
            print('\n\n\n')
            print(f'------------------- SCOPE {key} -------------------')
            for k, v in value.items():
                if k == 'vars':
                    print(f'________________Vars table of {key}________________')
                    v.print_directory()
                    print('--------------------------------------------------------')
                else:
                    print(k, ':\t\t -->', v)
            print()

TYPES = {
    'int': 0,
    'float': 1,
    'bool': 2,
    'char': 3,
}