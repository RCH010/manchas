import ply.yacc as yacc
from lexer import tokens, keywords

symbol_table = {}

def p_epsilon(p):
    '''epsilon : '''
    p[0] = None

# PROGRAM
def p_program(p):
    '''program : PROGRAM ID SEMICOLON program_1'''
    pass

def p_program_1(p):
    '''program_1 : vars program_1
        | function program_1
        | main_block'''

# VARS
def p_vars(p):
    '''vars : LET ID vars_prima_1'''

def p_vars_prima_1(p):
    '''vars_prima_1 : vars_prima_2 COLON type SEMICOLON vars_prima_1 
        | vars_prima_2 COLON type SEMICOLON'''

def p_vars_prima_2(p):
    '''vars_prima_2 : ID 
        | ID COMMA vars_prima_2'''

def p_type(p):
    '''type : INT type_1
        | FLOAT type_1
        | CHAR type_1
        | BOOL type_1'''

def p_type_1(p):
    '''type_1 : LBRACKET expression RBRACKET
        | epsilon'''

def p_function(p):
    '''function : ID COLON return_type LPAREN params RPAREN block
        | ID COLON return_type LPAREN RPAREN block'''

def p_main_block(p):
    '''main : LPAREN RPAREN block'''

def p_block(p):
    '''block : LBRACE statements RBRACE'''

def p_return_type(p):
    '''return_type : void
        | type'''

def p_params(p):
    '''params : ID COLON type params_1 COMMA params
        | ID COLON type'''

def p_statements(p):
    '''statements : assignment
        | condition
        | writing
        | reading
        | repetition
        | return
        | function_call
        | expression
        | special_functions'''

def p_special_functions(p):
    '''special_functions : mean
        | median
        | mode
        | variance
        | standard_deviation'''

def p_assignment(p):
    '''assignment : ID EQUALS expression SEMICOLON
        | ID LBRACKET expression RBRACKET EQUALS expression SEMICOLON'''

def p_condition(p):
    '''condition : IF LBRACE expression RBRACE block
        |  IF LBRACE expression RBRACE block ELSE block'''

# EXPRESION
def p_expresion(p):
    '''expresion : exp
        | exp LT exp
        | exp LE exp
        | exp GT exp
        | exp GE exp
        | exp EQ exp
        | exp NE exp
        | exp AND exp
        | exp OR exp
    '''

def p_exp(p):
    '''exp : term
        | term exp_1'''

def p_exp_1(p):
    '''exp_1 : PLUS exp
        | MINUS exp'''

def p_term(p):
    '''term : factor
        | factor term_2'''

def p_term_2(p):
    '''term_2 : TIMES term
        | DIVIDE term'''

def p_factor(p):
    '''factor : LPAREN expresion RPAREN
        | LBRACKET expresion RBRACKET
        | function_call
        | factor_prima_1'''

def p_factor_prima_1(p):
    '''factor_prima_1 : PLUS varcte
        | MINUS varcte
        | varcte'''

def p_varcte(p):
    '''vartcte : ID
        | CTEI
        | CTEF
        | CTEC
        | TRUE
        | FALSE'''