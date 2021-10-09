from utils import Data_types
from directories.directory import Directory

class Vars(Directory):
    def add_new_var(self, id, type, value = None):
        if id in self.dic:
            print('Error', id, 'is already declared on this scope')
            return 'Error'
        # A variable cant be of type void
        if type not in Data_types or type == Data_types.VOID:
                print('Error', 'return type:', type ,'is an invalid type for', id)
                return 'Error'
        self.dic[id] = {type: type, value: value}