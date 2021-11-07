import ply.yacc as yacc
import sys
from collections import deque
from lexer import tokens, keywords
from directories.scopes import Scopes_directory
from directories.vars import Vars
from operation import Operation
from utils import Data_types
from quadruples import Quadruple

# Program directory, this contains all functions and the main scope
program_scopes = Scopes_directory()
current_scope = ''
# Used for declaration of many variables in one line (Params on funcitions as well)
# for example: let my_var1, my_var2 : int;
vars_stack = deque()
params_vars_stack = deque()

# Quaduples array, each element should be of type Quadruples
# Each quadruple is an operation, here we also have jumps and stuff
quadruples = [];
# Operands Poper stack (A, B, t1..)
operands = deque()
# Operatores stack (+ -, =, /..)
operators = deque()
# Types stack
types = deque()
# jups stack 
jumps = deque()

###
tempsCount = 0

# PROGRAM
def p_program(p):
    '''program : PROGRAM ID np_create_global SEMI vars program_1 np_end_program
        |  PROGRAM ID np_create_global SEMI program_1 np_end_program'''
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
    '''function : FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN np_set_func_start_point block np_end_function
        | FUNCTION ID COLON return_type np_create_new_scope LPAREN params RPAREN np_set_func_start_point block np_end_function
        | FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN vars np_set_func_start_point block np_end_function
        | FUNCTION ID COLON return_type np_create_new_scope LPAREN params RPAREN vars np_set_func_start_point block np_end_function'''
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
    '''params : ID COLON type np_add_vars np_add_params_type COMMA params
        | ID COLON type np_add_vars np_add_params_type'''

def p_statements(p):
    '''statements : function_call statements1
        | assignment statements1
        | condition statements1
        | writing statements1
        | reading statements1
        | repetition statements1
        | return statements1
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
    '''assignment : ID np_add_id_quad EQUALS np_add_operator expression np_assign_expression SEMI
        | ID LBRACKET expression RBRACKET EQUALS expression SEMI''' #TODO: ARREGLOS
    if(len(p) == 5):
        p[0] = ('equals', p[1], p[3])
    else:
        # TODO Asignación de arrelgos
        p[0] = ('equals-array', p[1], p[3], p[6])

def p_condition(p):
    '''condition : IF LPAREN expression RPAREN np_condition_gotof block np_condition_end_gotof
        |  IF LPAREN expression RPAREN np_condition_gotof block ELSE np_condition_goto_else block np_condition_end_gotof'''

# expression
def p_expression(p):
    '''expression : exp
        | expression1 np_add_quadruple_logical
        | expression0 np_add_quadruple_or_and
    '''
    p[0] = p[1]

def p_expression0(p):
    '''expression0 : expression AND np_add_operator expression
        | expression OR np_add_operator expression'''

def p_expression1(p):
    '''expression1 : exp LT np_add_operator exp
        | exp LE np_add_operator exp
        | exp GT np_add_operator exp
        | exp GE np_add_operator exp
        | exp EQ np_add_operator exp
        | exp NE np_add_operator exp'''
    p[0] = (p[1], p[2], p[3])

def p_exp(p):
    '''exp : term np_add_quadruple_sum_min
        | term exp_1'''

def p_exp_1(p):
    '''exp_1 : PLUS np_add_operator exp
        | MINUS np_add_operator exp'''

def p_term(p):
    '''term : factor np_add_quadruple_times_div
        | factor term_2'''

def p_term_2(p):
    '''term_2 : TIMES np_add_operator term
        | DIVIDE np_add_operator term'''

def p_factor(p):
    '''factor : LPAREN np_add_paren expression RPAREN np_pop_paren 
        | LBRACKET expression RBRACKET
        | function_call
        | factor_prima_1'''

def p_factor_prima_1(p):
    '''factor_prima_1 : PLUS varcte
        | MINUS varcte
        | varcte'''

def p_varcte(p):
    '''varcte : ID np_add_id_quad
        | CTEI np_add_cte_int
        | CTEF np_add_cte_float
        | CTEC np_add_cte_char
        | TRUE np_add_cte_bool
        | FALSE np_add_cte_bool'''
    p[0] = p[1]

def p_writing(p):
    '''writing : PRINT LPAREN writing_1 RPAREN SEMI'''

def p_writing_1(p):
    '''writing_1 : expression np_add_print_quadruple_exp COMMA writing_1
        | CTESTRING  np_add_print_quadruple_str COMMA writing_1
        | expression np_add_print_quadruple_exp
        | CTESTRING np_add_print_quadruple_str'''

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
    '''conditional_loop : WHILE np_while_init LPAREN expression RPAREN np_while_expression DO block np_while_end_block'''

def p_non_conditional_loop(p):
    '''non_conditional_loop : FOR LPAREN ID np_add_id_quad EQUALS np_add_operator expression np_assign_expression_for TO expression np_non_conditional_limit BY expression RPAREN block np_non_conditional_end'''

def p_return(p):
    '''return : RETURN expression SEMI'''

def p_function_call(p):
    '''function_call : ID LPAREN np_check_function_call  RPAREN SEMI
        | ID LPAREN np_check_function_call function_call_1 RPAREN SEMI
        | ID LPAREN np_check_function_call function_call_1 RPAREN
        | ID LPAREN np_check_function_call RPAREN'''

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
#                        NEURALGIC POINTS
# ======================================================================

'''
Create the global scope on the program_scopes by the id of 'program'
Create the 'goto' quadruple that will send the instruction pointer to
the 'main' function
'''
def p_np_create_global(p):
    '''np_create_global : '''
    global program_scopes, current_scope, jumps
    create_scope('program', Data_types['VOID'])
    set_new_quadruple('GOTO', None, None, None)
    jumps.append(len(quadruples) - 1)

'''
Create main scope on the program_scopes with the id of 'main'
pop from the jumps stack and update the GOTO quadruple generated at
the np_create_global
'''
def p_np_create_main_scope(p):
    '''np_create_main_scope : '''
    global jumps
    create_scope('main', Data_types['VOID'])
    main_quadruple_position = jumps.pop()
    old_main_goto_quadruple = quadruples[main_quadruple_position]
    old_main_goto_quadruple.setResult(len(quadruples))

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

# ======================================================================
#                  Code generation linal statements
# ======================================================================

def p_np_add_id_quad(p):
    '''np_add_id_quad : '''
    global operands, types
    # Get var instance from vars table
    current_var = get_var(p[-1])
    var_type = current_var['type']
    # Add number and type int to operands and types stacks
    operands.append(p[-1])
    types.append(var_type)
    #print('np_add_var_quad: -->', p[-1])


def p_np_add_cte_int(p):
    '''np_add_cte_int : '''
    global operands, types
    operands.append(p[-1])
    types.append(Data_types['INTEGER'])
    #print('np_add_cte_int: -->', p[-1])


def p_np_add_cte_float(p):
    '''np_add_cte_float : '''
    global operands, types
    operands.append(p[-1])
    types.append(Data_types['FLOAT'])
    #print('np_add_cte_float: -->', p[-1])


def p_np_add_cte_char(p):
    '''np_add_cte_char : '''
    global operands, types
    operands.append(p[-1])
    types.append(Data_types['CHARACTER'])
    #print('np_add_cte_char: -->', p[-1])


def p_np_add_cte_bool(p):
    '''np_add_cte_bool : '''
    global program_scopes, current_scope
    operands.append(p[-1])
    types.append(Data_types['BOOLEAN'])
    #print('np_add_cte_bool: -->', p[-1])

# Add operator to poper stack
def p_np_add_operator(p):
    '''np_add_operator : '''
    global operators
    #print('add operator', p[-1])
    operators.append(p[-1])

def p_np_add_paren(p):
    '''np_add_paren : '''
    global operators
    #print('add operator', p[-1])
    operators.append(p[-1])

def p_np_pop_paren(p):
    '''np_pop_paren : '''
    global operators
    if operators[-1] != '(':
        print('Error, not ( in operators stack')
        sys.exit()
    operators.pop()


def p_np_add_quadruple_sum_min(p):
    '''np_add_quadruple_sum_min : '''
    generate_new_quadruple(['+', '-'])

def p_np_add_quadruple_times_div(p):
    '''np_add_quadruple_times_div : '''
    generate_new_quadruple(['*', '/'])

def p_np_add_quadruple_logical(p):
    '''np_add_quadruple_logical : '''
    generate_new_quadruple(['<', '<=', '>', '>=', '==', '!='])

def p_np_add_quadruple_or_and(p):
    '''np_add_quadruple_or_and : '''
    generate_new_quadruple(['||', '&&'])

def p_np_assign_expression(p):
    '''np_assign_expression : '''
    global operators, operands, types, quadruples
    operator = operators.pop()
    right_operand = operands.pop()
    right_type = types.pop()
    left_operand = operands.pop()
    left_type = types.pop()
    res_type = Operation.getType(operator, right_type, left_type)

    if res_type == 'Error':
        print('Invalid operation, type mismatch on', right_type, 'and', left_type, 'with a', operator)
        sys.exit()
    set_new_quadruple(operator, right_operand, None, left_operand)

def p_np_condition_gotof(p):
    '''np_condition_gotof : '''
    global operands, types, quadruples, jumps
    res_if_type = types.pop()
    if res_if_type != Data_types['BOOLEAN']:
        print('Error, type mismatch on if')
        sys.exit()
    res_if = operands.pop()
    set_new_quadruple('GOTOF', res_if, None, None)
    jumps.append(len(quadruples) - 1)

def p_np_condition_end_gotof(p):
    '''np_condition_end_gotof : '''
    global jumps, quadruples
    jump_end_pos = jumps.pop()
    old_quadruple = quadruples[jump_end_pos]
    old_quadruple.setResult(len(quadruples))


def p_np_condition_goto_else(p):
    '''np_condition_goto_else : '''
    set_new_quadruple('GOTO', None, None, None)
    jump_end_pos = jumps.pop()
    jumps.append(len(quadruples) - 1)
    old_quadruple = quadruples[jump_end_pos]
    old_quadruple.setResult(len(quadruples))

# ======================================================================
#                  Code generation non-linear statements
#                               WHILE
# ======================================================================

# Where the while starts (before stop condition)
def p_np_while_init (p):
    '''np_while_init : '''
    jumps.append(len(quadruples))

# After
def p_np_while_expression (p):
    '''np_while_expression : '''
    exp_type = types.pop()
    if exp_type != Data_types['BOOLEAN']:
        create_error('Type-mismatch on While expresion')
    exp_res = operands.pop()
    # Generate quadruple, the result reamins
    set_new_quadruple('GOTOF', exp_res, None, None)
    jumps.append(len(quadruples) - 1)

def p_np_while_end_block (p):
    '''np_while_end_block : '''
    end_pos = jumps.pop()
    return_pos = jumps.pop()
    # Generate quadruple, the result reamins
    set_new_quadruple('GOTO', None, None, return_pos)
    # Update the quadr
    old_quadruple = quadruples[end_pos]
    old_quadruple.setResult(len(quadruples))


# ======================================================================
#                  Code generation non-linear statements
#                               FOR
# ======================================================================

'''
A regular non conditional expresion: for (myVar1 = 0 to myVar3 * 10 by 1) { _statements_ }
We add three neuralgic points, the first one: np_assign_expression_for
for (myVar1 = 0 np_assign_expression_for to myVar3 == myVar1 ... by 1) { _statements_ } ...
The second one:
for (myVar1 = 0 ... to myVar3 == myVar1 np_non_conditional_limit 10 by 1) { _statements_ } ...
and the third one:
for (myVar1 = 0 ... to myVar3 == myVar1 ... 10 by 1) { _statements_ } np_non_conditional_end
'''
def p_np_assign_expression_for(p):
    '''np_assign_expression_for : '''
    global operators, operands, types, quadruples, jumps
    operator = operators.pop()
    right_operand = operands.pop()
    right_type = types.pop()
    left_operand = operands.pop()
    left_type = types.pop()
    res_type = Operation.getType(operator, right_type, left_type)
    # In the case of the 'for' the type of the variable must be integer
    if right_type != Data_types['INTEGER'] or left_type != Data_types['INTEGER'] :
        create_error(f'Conditional variable of "For" must be integer')
    set_new_quadruple(operator, right_operand, None, left_operand)
    # save position where the for starts... this will go on the GOTO at the end of the for
    jumps.append(len(quadruples))
    # add the variable of the for in the stacks
    operands.append(left_operand)
    types.append(Data_types['INTEGER'])

def p_np_non_conditional_limit(p):
    ''' np_non_conditional_limit : '''
    global operators, operands, types, quadruples, jumps
    result = operands.pop()
    op_type = types.pop()

    if op_type != Data_types['BOOLEAN']:
        create_error('Invalid type in "For" statement, must be boolean')
    set_new_quadruple('GOTOV', result, None, None)
    jumps.append(len(quadruples) - 1)
    

def p_np_non_conditional_end (p):
    '''np_non_conditional_end : '''
    global operators, operands, types, quadruples, program_scopes, current_scope, tempsCount
    delta_value = operands.pop()
    delta_type = types.pop()
    if delta_type != Data_types['INTEGER']:
        create_error('Invalid type in "For" statement in delta, must be integer')
    for_var_value = operands.pop()
    for_var_type = types.pop()
    res_type = Operation.getType('+', for_var_type, delta_type)
    
    if res_type == 'Error' or res_type != Data_types['INTEGER']:
        create_error(f'Invalid type in "For" expression\n type mismatch on {for_var_type} and {delta_type} with a +')

    current_scope_vars = program_scopes.get_vars_table(current_scope)
    temp_var_name = f"_temp{tempsCount}"
    tempsCount += 1
    current_scope_vars.add_new_var(temp_var_name, res_type)
    set_new_quadruple('+', for_var_value, delta_value, for_var_value)

    end_pos = jumps.pop()
    return_pos = jumps.pop()
    set_new_quadruple('GOTO', None, None, return_pos)

    # Update the GOTOV quadruple
    old_quadruple = quadruples[end_pos]
    old_quadruple.setResult(len(quadruples))


# ====================
#           PRINT
# ====================
def p_np_add_print_quadruple_str(p):
    '''np_add_print_quadruple_str : '''
    value = p[-1]
    set_new_quadruple('PRINT', None, None, value)

def p_np_add_print_quadruple_exp(p):
    '''np_add_print_quadruple_exp : '''
    global quadruples,operands, types
    value = operands.pop()
    v_type = types.pop()
    set_new_quadruple('PRINT', None, None, value)


# =
# Functions stuff
# =
def p_np_add_params_type(p):
    '''np_add_params_type : '''
    global program_scopes, current_scope
    current_scope_params = program_scopes.get_params_table(current_scope)
    current_scope_params.append(p[-2])

def p_np_set_func_start_point(p):
    '''np_set_func_start_point : '''
    global program_scopes, current_scope, quadruples
    program_scopes.set_func_cont(current_scope, len(quadruples))

def p_np_end_function(p):
    '''np_end_function : '''
    global program_scopes, current_scope
    set_new_quadruple('ENDFUNC', None, None, None)
    # Calculate the memory that the function will use
    program_scopes.calculate_function_size(current_scope)
    

def p_np_end_program(p):
    '''np_end_program : '''
    set_new_quadruple('END', None, None, None)


def p_np_check_function_call(p):
    '''np_check_function_call : '''
    global program_scopes
    print('IAAMMM HWEEEERE')
    if not program_scopes.exists(p[-2]):
        create_error(f'Function {p[-1]} is not defined')
    else:
        print('si funciono esot', p[-1])



# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
'''
Create a new scope
'''
def create_scope(scope_id, return_type):
      # Create the global scope
    global program_scopes, current_scope
    program_scopes.add_new_scope(scope_id, return_type, Vars(scope_id))
    current_scope = scope_id


'''
create a new quadruple for an expresion
'''
def generate_new_quadruple(operator_to_check):
    global quadruples, operands, operators, types, program_scopes, current_scope, tempsCount
    if len(operators) > 0 and (operators[-1] in operator_to_check):
        # Get operator and operands from stacks
        # For example: 
        # operator = +    right_operand = 10.5  right_type = FLOAT
        #                 left_operand = 10     left_type = INTEGER
        # res_type should be FLOAT
        operator = operators.pop()
        right_operand = operands.pop()
        right_type = types.pop()
        left_operand = operands.pop()
        left_type = types.pop()
        # Get the resulting type of the operation
        res_type = Operation.getType(operator, right_type, left_type)
        
        if res_type == 'Error':
            create_error(f'Invalid operation, type mismatch on {right_type} and {left_type} with a {operator}')
        # generate new temporal of type rest_type
        current_scope_vars = program_scopes.get_vars_table(current_scope)
        temp_var_name = f"_temp{tempsCount}"
        tempsCount += 1
        current_scope_vars.add_new_var(temp_var_name, res_type)
        # Append a new quadruple to the quadruples list
        set_new_quadruple(operator, left_operand, right_operand, temp_var_name)
        # add to operands and types stacks the result
        operands.append(temp_var_name)
        types.append(res_type)

'''
Get the vars directory given the scope id
First the directory is searched on the current scope
If it's not found, then it is searched on the global scope
'''
def get_var(var_id):
    global program_scopes, current_scope
    scope_vars = program_scopes.get_vars_table(current_scope)
    directory_var = scope_vars.get_one(var_id)
    # if 'not_in_directory' received, check the global scope
    if (directory_var == 'not_in_directory'):
        program_vars = program_scopes.get_vars_table('program')
        directory_var = program_vars.get_one(var_id)
    
    if (directory_var == 'not_in_directory'):
        create_error(f'{var_id} not found in current or global scope')

    return directory_var

'''
Create a new instance of the Quadruple class and append it to the quadruples list
'''
def set_new_quadruple(first, second, third, fourth):
    new_quadruple = Quadruple(first, second, third, fourth)
    quadruples.append(new_quadruple)


'''
Create print an error message and exit the program
'''
def create_error(message):
    print('====================================')
    print('\t Error:')
    print('\t', message)
    print('====================================')
    sys.exit()


parser = yacc.yacc()
