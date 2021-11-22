import ply.lex as lex
import re

# LEX 
# Sintáxis
# =====================================
# Define reserved words

keywords={
    'program': 'PROGRAM',
    # === TYPES ===
    'let': 'LET',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'bool': 'BOOL',
    # == LITERALS ===
    'true': 'TRUE',
    'false': 'FALSE',
    # === FUNCTIONS ===
    'function': 'FUNCTION',
    'main': 'MAIN',
    'void': 'VOID',
    'return': 'RETURN',
    # === BLOCKS ===
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'for': 'FOR',
    'to': 'TO',
    'by': 'BY',
    # == WRITIGN & READING ===
    'print': 'PRINT',
    'println': 'PRINTLN',
    'read': 'READ',
    # === ESPECUAL FUNCTIONS ===
    'mean': 'MEAN',
    'median': 'MEDIAN',
    'pvariance': 'PVARIANCE',   # For Population variance of data
    'pstdev': 'PSTDEV',         # For Population standard deviation of data
    'variance': 'VARIANCE',     # For Sample variance of data
    'stdev': 'STDEV',           # For Sample standard deviation of data
    'random': 'RANDOM',         # For Sample standard deviation of data
    'plot': 'PLOT',             # Plot x and y
}

# =====================================
# Define tokens

tokens = [
    # Literals
    'ID', 'CTEF', 'CTEI', 'CTEC', 'CTESTRING',
    # Delimeters , : ; ( ) [ ] { }
    'COMMA', 'COLON', 'SEMI',
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    # Assignment
    'EQUALS',
    # Operators 
    # <, <=, >, >=, ==, !=
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    # ||, &&
    'OR', 'AND',
    # + - * /
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
]

# Add reserved words to list of tokens
tokens += list(keywords.values())

# =====================================
# Define regex for tokens

t_ignore = ' \t'

# Literals

# Delimeters
t_COMMA = r','
t_COLON = r':'
t_SEMI = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Operators 
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Assignment
t_EQUALS = r'='

t_OR = r'\|\|'
t_AND = r'&&'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

# Literals
t_CTESTRING = r'\".*\"'
t_CTEC = r'\'(.{1})\''

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[A-Za-z]([A-Za-z]|[0-9])*'
    t.type = keywords.get(t.value, 'ID')
    # print(t.type, t.value)
    return t

def t_CTEF(t):
    r'[0-9]+(\.[0-9]+)'
    try:
        t.value = float(t.value)
    except ValueError:
        print("C-26 - Invalid float value", t.value)
        t.value = 0
    return t

def t_CTEI(t):
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("C-27 - Invalid Int value", t.value)
        t.value = 0
    return t

# Tokens error
def t_error(t):
    print("C-28 - Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
lexer = lex.lex()
