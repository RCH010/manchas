import sys

'''
Base class for a directory.
Scopes class and vars class inherit from Directory
'''
class Directory():

    def __init__(self):
        self.dic = {}

    def exists(self, id):
        return id in self.dic

    def getOne(self, id):
        if id not in self.dic:
            print (id, 'not in directory')
            sys.exit()
    
    def print_directory_keys(self):
        for key, value in self.dic.items():
            print(key)

    def print_directory(self):
        for key, value in self.dic.items():
            print(key, '->',value)