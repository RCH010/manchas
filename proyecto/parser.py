import ply.yacc as yacc
import sys
from collections import deque
from lexer import tokens, keywords
from directories.scopes import Scopes_directory
from directories.vars import Vars
from utils import Data_types

# symbol_table = {
#     "mi_variable": 
# }

# procedimientos = {
#     "global": Class procedimientos
#     ... "mi_funcion": class procedimientos

# }

# Program directory, this contains all functions and the main scope
program_scopes = Scopes_directory()
current_scope = ''
# Used for declaration of many variables in one line
# for example: let my_var1, my_var2 : int;
vars_stack = deque()
params_vars_stack = deque()

# PROGRAM
def p_program(p):
    '''program : PROGRAM ID np_create_global SEMI vars program_1
        |  PROGRAM ID np_create_global SEMI program_1'''
    p[0] = 'correct'

def p_program_1(p):
    '''program_1 : function program_1
        | main_block'''
    p[0] = None


# VARS
def p_vars(p):
    '''vars : vars_1'''
    p[0] = ('let', p[1])

def p_vars_1(p):
    '''vars_1 : LET vars_prima_1 vars_1
        | LET vars_prima_1'''
# var_1, var_2 : int;
# var_1 : int;
def p_vars_prima_1(p):
    '''vars_prima_1 : ID COLON type np_add_vars SEMI
        | ID  np_add_satck_vars COMMA vars_prima_1'''
    # añado la var a mi tabla de variables

def p_type(p):
    '''type : INT type_1
        | FLOAT type_1
        | CHAR type_1
        | BOOL type_1'''
    p[0] = p[1]

def p_type_1(p):
    '''type_1 : LBRACKET expression RBRACKET
        | epsilon'''

def p_function(p):
    '''function : FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN block
        | FUNCTION ID COLON return_type np_create_new_scope LPAREN params RPAREN block
        | FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN vars block
        | FUNCTION ID COLON return_type np_create_new_scope LPAREN params RPAREN vars block'''
    p[0] = None

def p_main_block(p):
    '''main_block : MAIN np_create_main_scope LPAREN RPAREN block
        | MAIN np_create_main_scope LPAREN RPAREN vars block'''

def p_block(p):
    '''block : LBRACE statements RBRACE'''

def p_return_type(p):
    '''return_type : VOID
        | type'''
    p[0] = p[1]

def p_params(p):
    '''params : ID COLON type np_add_vars COMMA params
        | ID COLON type np_add_vars'''

def p_statements(p):
    '''statements : assignment statements1
        | condition statements1
        | writing statements1
        | reading statements1
        | repetition statements1
        | return statements1
        | function_call statements1
        | expression statements1
        | special_functions statements1'''
    p[0] = (p[1], p[2])

def p_special_functions(p):
    '''special_functions : mean
        | median
        | mode
        | variance
        | standard_deviation'''

def p_statements1(p):
    '''statements1 : statements
        | epsilon'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID EQUALS expression SEMI
        | ID LBRACKET expression RBRACKET EQUALS expression SEMI'''
    if(len(p) == 5):
        p[0] = ('equals', p[1], p[3])
    else:
        p[0] = ('equals-array', p[1], p[3], p[6])

def p_condition(p):
    '''condition : IF LPAREN expression RPAREN block
        |  IF LPAREN expression RPAREN block ELSE block'''

# expression
def p_expression(p):
    '''expression : exp
        | expression1
    '''
    p[0] = p[1]

def p_expression1(p):
    '''expression1 : exp LT exp
        | exp LE exp
        | exp GT exp
        | exp GE exp
        | exp EQ exp
        | exp NE exp
        | exp AND exp
        | exp OR exp'''
    p[0] = (p[1], p[2], p[3])

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
    '''factor : LPAREN expression RPAREN
        | LBRACKET expression RBRACKET
        | function_call
        | factor_prima_1'''

def p_factor_prima_1(p):
    '''factor_prima_1 : PLUS varcte
        | MINUS varcte
        | varcte'''

def p_varcte(p):
    '''varcte : ID
        | CTEI
        | CTEF
        | CTEC
        | TRUE
        | FALSE'''

def p_writing(p):
    '''writing : PRINT LPAREN writing_1 RPAREN SEMI'''

def p_writing_1(p):
    '''writing_1 : expression COMMA writing_1
        | expression
        | CTESTRING
        | CTESTRING COMMA'''

def p_reading(p):
    '''reading : READ LPAREN reading_1 RPAREN SEMI'''

def p_reading_1(p):
    '''reading_1 : ID COMMA reading_1
        | ID LBRACKET expression RBRACKET COMMA reading_1
        | ID
        | ID LBRACKET expression RBRACKET'''

def p_repetition(p):
    '''repetition : non_conditional_loop
        | conditional_loop'''

def p_conditional_loop(p):
    '''conditional_loop : WHILE LPAREN expression RPAREN DO block'''

def p_non_conditional_loop(p):
    '''non_conditional_loop : FOR LPAREN ID EQUALS expression TO expression BY expression RPAREN block'''

def p_return(p):
    '''return : RETURN expression SEMI'''

def p_function_call(p):
    '''function_call : ID LPAREN RPAREN SEMI
        | ID LPAREN function_call_1 RPAREN SEMI
        | ID LPAREN function_call_1 RPAREN
        | ID LPAREN RPAREN'''

def p_function_call_1(p):
    '''function_call_1 : expression
        | expression COMMA function_call_1'''

def p_mean(p):
    '''mean : MEAN LPAREN expression RPAREN SEMI'''

def p_median(p):
    '''median : MEDIAN LPAREN expression RPAREN SEMI'''

def p_mode(p):
    '''mode : MODE LPAREN expression RPAREN SEMI'''

def p_variance(p):
    '''variance : VARIANCE LPAREN expression RPAREN SEMI'''

def p_standard_deviation(p):
    '''standard_deviation : STDEV LPAREN expression RPAREN SEMI'''

def p_epsilon(p):
    '''epsilon : '''
    p[0] = None

def p_error(token):
    print(f"Syntax Error: {token.value!r}")
    print(token)
    token.lexer.skip(1)
    sys.exit()


# ======================================================================
#                        Functions for scopes
# ======================================================================

def p_np_create_global(p):
    '''np_create_global : '''
    global program_scopes, current_scope
    create_scope('program', Data_types['VOID'])

def p_np_create_main_scope(p):
    '''np_create_main_scope : '''
    create_scope('main', Data_types['VOID'])

# p[-4]   p[-3]p[-2]  p[-1]     p[0]
# FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN  block
#  p[-4]  p[-3] p[-2]  p[-1]    p[0]
# FUNCTION ID COLON return_type np_create_new_scope LPAREN params RPAREN  block
def p_np_create_new_scope(p):
    '''np_create_new_scope : '''
    global program_scopes, current_scope
    function_id = p[-3]
    return_type = p[-1]
    create_scope(function_id, return_type)

def create_scope(scope_id, return_type):
      # Create the global scope
    global program_scopes, current_scope
    print('New Scope', scope_id)
    program_scopes.add_new_scope(scope_id, return_type, Vars(scope_id))
    current_scope = scope_id



# For example
# let my_var, my_var2, my_last_var : int NP_ADD_VARS ;
# function miSuperFunction : void (uno:int, dos:bool)
# function miSuperFunction : void (uno:int np_add_vars, dos:bool np_add_vars)

# Here is adding to stack my_var, my_var2
def p_np_add_satck_vars (p):
    '''np_add_satck_vars : '''
    global vars_stack
    vars_stack.append(p[-1])

# Here is adding to stack my_last_var
def p_np_add_vars(p):
    '''np_add_vars : '''
    global program_scopes, current_scope, vars_stack
    # Add the last var to stack o the var
    var_id = p[-3]
    vars_stack.append(p[-3])
    vars_type = p[-1]

    while vars_stack:
        current_scope_vars = program_scopes.get_vars_table(current_scope)
        current_scope_vars.add_new_var(vars_stack[0], vars_type)
        vars_stack.popleft()


parser = yacc.yacc()
