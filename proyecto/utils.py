class MetaTypes(type):
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("__") and not callable(getattr(dir(self), attr)):
                yield attr

# class Data_types(metaclass=MetaTypes):
#     INTEGER = 'int'
#     FLOAT = 'float'
#     CHARACTER = 'char'
#     BOOLEAN = 'bool'
#     VOID = 'void'
Data_types = {
    'INTEGER': 'int',
    'FLOAT': 'float',
    'CHARACTER': 'char',
    'BOOLEAN': 'bool',
    'VOID': 'void',
}

class Relation_operators(metaclass=MetaTypes):
    # Arithmetic operators
    SUM = '+'
    MINUS = '-'
    DIVISION = '/'
    TIMES = '*'
    # Relation operators
    LESSTHAN = '<'
    LESSEQUALTHAN = '<='
    GREATERTHAN = '>'
    GREATEREQUALTHAN = '>='
    EQUAL = '=='
    DIFFERENT = '!='
    # Boolean operators
    AND = '&&'
    OR = '||'
    # Aignment
    EQUALS = '='

