import sys
from compiler.utils import Data_types, create_error
from compiler.directories.directory import Directory

'''
Vars directory, is used to manage all variables from a specific scope
a instance of Vars is used on an instance of Scopes
'''
class Vars(Directory):
    def __init__(self, scope):
        super().__init__()
        self.scope = scope

    def get_scope(self):
        return self.scope
    
    def add_new_var(self, id, type, value = None):
        if id in self.dic:
            create_error('Cannot add this variable {id} is already declared on this scope', 'C-31')
        # A variable cant be of type void
        if type not in Data_types.values() or type == Data_types['VOID']:
            create_error(f'Return type: {type} is an invalid type for {id}', 'C-32')
        self.dic[id] = {'type': type ,'value': value, 'address': None}
    
    def set_address(self, id, address):
        self.dic[id]['address'] = address
    
    def get_address(self, id):
        return self.dic[id]['address']
    
    def set_arrray_values(self, id, is_array = False, array_size = None):
        self.dic[id]['is_array'] = is_array
        self.dic[id]['array_size'] = array_size
    
    def get_vars_dictionary(self):
        return self.dic
    
