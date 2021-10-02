import ply.yacc as yacc
from lexer import tokens, keywords

symbol_table = {}

# PROGRAM
def p_program(p):
    '''program : PROGRAM ID SEMI program_1'''
    p[0] = 'correct'

def p_program_1(p):
    '''program_1 : vars program_1
        | function program_1
        | main_block'''

# VARS
def p_vars(p):
    '''vars : LET vars_prima_1'''

def p_vars_prima_1(p):
    '''vars_prima_1 : ID COLON type SEMI
        | ID COMMA vars_prima_1'''

def p_type(p):
    '''type : INT type_1
        | FLOAT type_1
        | CHAR type_1
        | BOOL type_1'''

def p_type_1(p):
    '''type_1 : LBRACKET expression RBRACKET
        | epsilon'''

def p_function(p):
    '''function : FUNCTION ID COLON return_type LPAREN params RPAREN block
        | ID COLON return_type LPAREN RPAREN block'''

def p_main_block(p):
    '''main_block : MAIN LPAREN RPAREN block'''

def p_block(p):
    '''block : LBRACE statements RBRACE'''

def p_return_type(p):
    '''return_type : VOID
        | type'''

def p_params(p):
    '''params : ID COLON type COMMA params
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
    '''assignment : ID EQUALS expression SEMI
        | ID LBRACKET expression RBRACKET EQUALS expression SEMI'''

def p_condition(p):
    '''condition : IF LPAREN expression RPAREN block
        |  IF LPAREN expression RPAREN block ELSE block'''

# expression
def p_expression(p):
    '''expression : exp
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
    '''non_conditional_loop : FOR LPAREN ID EQUALS expression TO expression BY expression RPAREN'''

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
    print(p)
    p[0] = None

def p_error(token):
    print(f"Syntax Error: {token.value!r}")
    print(token)
    token.lexer.skip(1)


parser = yacc.yacc()