class MetaTypes(type):
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("__") and not callable(getattr(dir(self), attr)):
                yield attr

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

'''
1 - 0   ==> Math & Logic Operators
20 - 30 ==> Jumps & functions stuff
30
'''
operators_id = {
    '+': 1,         # SUM
    '-': 2,         # SUBSTRACTION
    '/': 3,         # DIVISION
    '*': 4,         # MULTIPLICATION
    
    '<': 5,         # LESS THAN
    '<=': 6,        # LESS EQUAL THAN
    '>': 7,         # GREATER THAN
    '>=': 8,        # GREATER EQUAL THAN
    '==': 9,        # EQUAL
    '!=': 10,       # DIFFERENT
    
    '&&': 11,       # AND
    '||': 12,       # OR
    
    '=': 13,        # EQUALS
    
    'GOTO': 20,     # Go To
    'GOTOV': 21,    # Go to if true 
    'GOTOF': 22,    # Go to if false
    'GOSUB': 23,    # Go to subfunction
    'ERA': 24,      # Starts function calling
    'PARAM': 25,    # Parameter of function
    'ENDFUNC': 26,  # End of function
    'END': 27,      # End of program

    'RETURN': 30,   # For return of a function
    'PRINT': 31,    # For print statements
    'VERIFY': 32    # For array checking accessing value
}
