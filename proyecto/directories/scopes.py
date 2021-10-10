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
        self.dic[id] = { 'vars': vars_table, 'return_type': return_type }

    def get_vars_table(self, id):
        return self.dic[id]['vars']

    def print_directory(self):
        for key, value in self.dic.items():
            print()
            print('SCOPE:', key)
            for k, v in value.items():
                if k == 'vars':
                    print(k, ':')
                    v.print_directory()
                else:
                    print(k, '->', v)
            print()

