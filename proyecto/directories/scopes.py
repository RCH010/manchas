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
            return 'Error'
        if return_type not in Data_types:
            print('Error', 'return type:', return_type ,'is an invalid type for', id)
            return 'Error'
        self.dic[id] = { vars: vars_table }

    

    
  
