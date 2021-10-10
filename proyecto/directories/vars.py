import sys
from utils import Data_types
from directories.directory import Directory

class Vars(Directory):
    def __init__(self, scope):
        super().__init__()
        self.scope = scope

    def get_scope(self):
        return self.scope
    
    def add_new_var(self, id, type, value = None):
        if id in self.dic:
            print('Error', id, 'is already declared on this scope')
            sys.exit()
        # A variable cant be of type void
        if type not in Data_types.values() or type == Data_types['VOID']:
                print('Error', 'return type:', type ,'is an invalid type for', id)
                sys.exit()
        self.dic[id] = {'type': type, 'value': value}

    