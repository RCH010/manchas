class Element():
    def __init__(self, id, type, scope):
        self.id = id
        self.type = type
    
    def set_scope(self, scope):
        self.scope = scope
    
    def get_scope(self):
        return self.scope