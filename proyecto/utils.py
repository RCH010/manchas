class MetaTypes(type):
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("__"):
                yield attr

class Data_types(metaclass=MetaTypes):
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    CHARACTER = 'CHAR'
    BOOLEAN = 'BOOL'
    VOID = 'VOID'


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
