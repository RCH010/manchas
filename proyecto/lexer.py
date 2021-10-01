import ply.lex as lex
import re

# LEX 
# Sintáxis
# =====================================
# Define reserved words

keywords={
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
    'read': 'READ',
    # === ESPECUAL FUNCTIONS ===
    'mean': 'MEAN',
    'median': 'MEDIAN',
    'mode': 'MODE',
    'variance': 'VARIANCE',
    'stdev': 'STDEV',
}

# =====================================
# Define tokens

tokens = [
    # Literals
    'ID', 'CTEF', 'CTEI', 'CTEC', 'CTESTRING',
    # Delimeters , : ; ( ) [ ]
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

# Assignment
t_EQUALS = r'='

# Operators 
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

t_OR = r'\|\|'
t_AND = r'&&'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

# Literals
t_CTESTRING = r'\".*\"'
t_CTECHAR = r'\'(.{1})\''

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[A-Za-z]([A-Za-z]|[0-9])*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_CTEF(t):
    r'[0-9]+(\.[0-9]+)'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t
# Tokens error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()