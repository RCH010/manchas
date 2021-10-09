class Directory():

    def __init__(self):
        self.dic = {}

    def exists(self, id):
        return id in self.dic

    def getOne(self, id):
        if id not in self.dic:
            print (id, 'not in directory')
            return 'Error'
    