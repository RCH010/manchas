import ply.yacc as yacc
import sys
from collections import deque
from compiler.lexer import tokens, keywords
from compiler.directories.scopes import Scopes_directory
from compiler.directories.vars import Vars
from compiler.operation import Operation
from compiler.memory import Memory
from compiler.directories.directory import Directory
from compiler.utils import Data_types, operators_id, types_ID, create_error
from compiler.quadruples import Quadruple

# Program directory, this contains all functions and the main scope
program_scopes = Scopes_directory()
# This indicates the scope in which its is reading
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

constants_table = {}
# Counters for memory management
memory_counters = Memory()
# Temoral counter 
tempsCount = 0

# This indicates if we are dealing with an array at the moment
# of defition: `let myArr : int[8]``
is_array = False
array_size = 0

# Parameters counter
params_count = 0
current_function_call_id = None
params_counts = deque()
function_call_id_stack = deque()

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
# var_1 : int;
# var_1, var_2 : int;
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
    '''type_1 : LBRACKET CTEI RBRACKET
        | epsilon'''
    global operands, types, memory_counters, constants_table, is_array, array_size
    if (p[1] == '['):
        is_array = True
        array_size = p[2]
        
        if array_size < 1:
            create_error(f'You are trying to create an array of size: {array_size} \nArrays must be defined with a value grater than 1', 'C-01')
        create_constat_int_address(array_size)

    else:
        is_array = False
        array_size = None
# 4 variations, with or without params, and with or without vars
def p_function(p):
    '''function : FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN np_set_func_start_point block np_end_function
        | FUNCTION ID COLON return_type np_create_new_scope LPAREN params RPAREN np_set_func_start_point block np_end_function
        | FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN vars np_set_func_start_point block np_end_function
        | FUNCTION ID COLON return_type np_create_new_scope LPAREN params RPAREN vars np_set_func_start_point block np_end_function'''
    p[0] = None

def p_main_block(p):
    '''main_block : MAIN np_create_main_scope LPAREN RPAREN block np_end_main
        | MAIN np_create_main_scope LPAREN RPAREN vars block np_end_main'''

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
    '''statements : void_function_call statements1
        | assignment statements1
        | condition statements1
        | writing statements1
        | reading statements1
        | repetition statements1
        | return statements1'''
    p[0] = (p[1], p[2])

def p_special_functions(p):
    '''special_functions : mean
        | median
        | random
        | variance
        | p_variance
        | standard_deviation
        | p_standard_deviation'''

def p_statements1(p):
    '''statements1 : statements
        | epsilon'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID np_add_id LBRACKET np_check_is_array expression np_verify_array_dim RBRACKET np_get_array_address EQUALS np_add_operator expression np_assign_expression SEMI
        | ID np_add_id EQUALS np_add_operator expression np_assign_expression SEMI'''

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
        | term np_add_quadruple_sum_min exp_1'''

def p_exp_1(p):
    '''exp_1 : PLUS np_add_operator exp
        | MINUS np_add_operator exp'''

def p_term(p):
    '''term : factor np_add_quadruple_times_div
        | factor np_add_quadruple_times_div term_2'''

def p_term_2(p):
    '''term_2 : TIMES np_add_operator term
        | DIVIDE np_add_operator term'''

def p_factor(p):
    '''factor : LPAREN np_add_paren expression RPAREN np_pop_paren 
        | ID np_add_id LBRACKET np_check_is_array expression np_verify_array_dim RBRACKET np_get_array_address
        | factor_prima_1
        | function_call
        | special_functions'''

def p_factor_prima_1(p):
    '''factor_prima_1 : PLUS varcte
        | MINUS np_set_as_negative varcte
        | varcte'''

def p_varcte(p):
    '''varcte : ID np_add_id
        | CTEI np_add_cte_int
        | CTEF np_add_cte_float
        | CTEC np_add_cte_char
        | TRUE np_add_cte_bool
        | FALSE np_add_cte_bool'''
    p[0] = p[1]

def p_writing(p):
    '''writing : PRINT LPAREN writing_1 RPAREN SEMI
        | PRINTLN LPAREN writing_2 RPAREN SEMI'''

def p_writing_1(p):
    '''writing_1 : expression np_add_print_quadruple_exp COMMA writing_1
        | CTESTRING  np_add_print_quadruple_str COMMA writing_1
        | expression np_add_print_quadruple_exp
        | CTESTRING np_add_print_quadruple_str'''

def p_writing_2(p):
    '''writing_2 : expression np_add_println_quadruple_exp COMMA writing_2
        | CTESTRING  np_add_println_quadruple_str COMMA writing_2
        | expression np_add_println_quadruple_exp
        | CTESTRING np_add_println_quadruple_str'''

def p_reading(p):
    '''reading : READ LPAREN reading_1 RPAREN np_add_read_quadruple SEMI'''

def p_reading_1(p):
    '''reading_1 : ID np_add_id
        | ID np_add_id LBRACKET np_check_is_array expression np_verify_array_dim RBRACKET np_get_array_address'''

def p_repetition(p):
    '''repetition : non_conditional_loop
        | conditional_loop'''

def p_conditional_loop(p):
    '''conditional_loop : WHILE np_while_init LPAREN expression RPAREN np_while_expression DO block np_while_end_block'''

def p_non_conditional_loop(p):
    '''non_conditional_loop : FOR LPAREN ID np_add_id EQUALS np_add_operator expression np_assign_expression_for TO expression np_non_conditional_limit BY expression RPAREN block np_non_conditional_end'''

def p_return(p):
    '''return : RETURN expression np_add_return_quadruple SEMI'''

def p_function_call(p):
    '''function_call : ID LPAREN np_check_function_call np_function_end_params RPAREN
        | ID LPAREN np_check_function_call function_call_1 np_function_end_params RPAREN'''

def p_void_function_call(p):
    '''void_function_call :  ID LPAREN np_check_function_call np_function_end_params RPAREN SEMI
        | ID LPAREN np_check_function_call function_call_1 np_function_end_params RPAREN SEMI'''

def p_function_call_1(p):
    '''function_call_1 : expression np_function_call_add_param
        | expression np_function_call_add_param COMMA function_call_1'''

def p_mean(p):
    '''mean : MEAN LPAREN ID RPAREN np_add_mean_quadruple'''

def p_median(p):
    '''median : MEDIAN LPAREN ID RPAREN np_add_median_quadruple'''

def p_random(p):
    '''random : RANDOM LPAREN CTEI COMMA CTEI RPAREN np_add_random_quadruple'''

def p_variance(p):
    '''variance : VARIANCE LPAREN ID RPAREN np_add_variance_quadruple'''

def p_p_variance(p):
    '''p_variance : PVARIANCE LPAREN ID RPAREN np_add_p_variance_quadruple'''

def p_standard_deviation(p):
    '''standard_deviation : STDEV LPAREN ID RPAREN np_add_stdev_quadruple'''
    
def p_p_standard_deviation(p):
    '''p_standard_deviation : PSTDEV LPAREN ID RPAREN np_add_p_stdev_quadruple'''



def p_epsilon(p):
    '''epsilon : '''
    p[0] = None

def p_error(token):
    print(f"Syntax Error: {token.value!r}")
    print(token)
    token.lexer.skip(1)
    sys.exit()


# ======================================================================
# ======================================================================
# ======================================================================
#                        NEURALGIC POINTS
# ======================================================================
# ======================================================================
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
    set_new_quadruple('GOTO', -1, -1, -1)
    jumps.append(len(quadruples) - 1)
    # Create an addres for 0, in constants table
    create_constat_int_address(0)

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
    old_main_goto_quadruple.set_result(len(quadruples))

'''
Create a new scope when a new function is created
Additionally, create a global variable with the same name and type
used for assignment when function is called
'''
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
    # Create a global variable with the name of the function, and type
    # This is used for assigning a value when the function is called
    if return_type != Data_types['VOID']:
        global_scope_vars = program_scopes.get_vars_table('program')
        global_scope_vars.add_new_var(function_id, return_type)
        new_address = get_vars_new_address(return_type, False, 1, 'program')
        global_scope_vars.set_address(function_id, new_address)
        global_scope_vars.set_arrray_values(function_id, is_array, array_size)


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
    global program_scopes, current_scope, vars_stack, is_array, array_size
    # Add the last var to stack o the var
    var_id = p[-3]
    vars_stack.append(p[-3])
    vars_type = p[-1]
    if (array_size is None):
        memory_space_to_save = 1
    else: 
        memory_space_to_save = array_size
    while vars_stack:
        current_scope_vars = program_scopes.get_vars_table(current_scope)
        current_scope_vars.add_new_var(vars_stack[0], vars_type)
        new_address = get_vars_new_address(vars_type, False, memory_space_to_save)
        current_scope_vars.set_address(vars_stack[0], new_address)
        current_scope_vars.set_arrray_values(vars_stack[0], is_array, array_size)
        vars_stack.popleft()

# ======================================================================
#                  Code generation lineal statements
# ======================================================================
'''
add ID to operands and types stack
this np is used on the _expression_ and on the for delcaration
'''
def p_np_add_id(p):
    '''np_add_id : '''
    global operands, types
    # Get var instance from vars table
    current_var = get_var(p[-1])
    var_type = current_var['type']
    var_address = current_var['address']
    # Add number(virtual address) and type int to operands and types stacks
    operands.append(var_address)
    types.append(var_type)

'''
Add integer memory address on operands and types array
- If not added, add the constant to constants table
'''
def p_np_add_cte_int(p):
    '''np_add_cte_int : '''
    global operands, types, memory_counters, constants_table
    value = p[-1]
    if value not in constants_table:    
        new_mem_address = memory_counters.count_const_int
        constants_table[value] = new_mem_address
        memory_counters.update_counter('const', Data_types['INTEGER'])
    address_of_constant = constants_table[value]
    operands.append(address_of_constant)
    types.append(Data_types['INTEGER'])

'''
Add float memory address on operands and types array
- If not added, add the constant to constants table
'''
def p_np_add_cte_float(p):
    '''np_add_cte_float : '''
    global operands, types, memory_counters, constants_table
    value = p[-1]
    if value not in constants_table:    
        new_mem_address = memory_counters.count_const_float
        constants_table[value] = new_mem_address
        memory_counters.update_counter('const', Data_types['FLOAT'])
    address_of_constant = constants_table[value]
    operands.append(address_of_constant)
    types.append(Data_types['FLOAT'])

'''
Add char memory address on operands and types array
- If not added, add the constant to constants table
'''
def p_np_add_cte_char(p):
    '''np_add_cte_char : '''
    global operands, types, memory_counters, constants_table
    value = p[-1]
    if value not in constants_table:    
        new_mem_address = memory_counters.count_const_char
        constants_table[value] = new_mem_address
        memory_counters.update_counter('const', Data_types['CHARACTER'])
    address_of_constant = constants_table[value]
    operands.append(address_of_constant)
    types.append(Data_types['CHARACTER'])

'''
Add bool memory address on operands and types array
- If not added, add the constant to constants table
'''
def p_np_add_cte_bool(p):
    '''np_add_cte_bool : '''
    global program_scopes, current_scope, memory_counters, constants_table, operands, types
    value = p[-1]
    if value not in constants_table:    
        new_mem_address = memory_counters.count_const_bool
        constants_table[value] = new_mem_address
        memory_counters.update_counter('const', Data_types['BOOLEAN'])
    address_of_constant = constants_table[value]
    operands.append(address_of_constant)
    types.append(Data_types['BOOLEAN'])
    
def p_np_set_as_negative(p):
    '''np_set_as_negative : '''
    global memory_counters, constants_table, operands, types, operators
    if -1 not in constants_table:    
        new_mem_address = memory_counters.count_const_int
        constants_table[-1] = new_mem_address
        memory_counters.update_counter('const', Data_types['INTEGER'])
    address_of_constant = constants_table[-1]
    operands.append(address_of_constant)
    types.append(Data_types['INTEGER'])
    operators.append('*')

# Add operator to poper stack
def p_np_add_operator(p):
    '''np_add_operator : '''
    global operators
    operators.append(p[-1])

def p_np_add_paren(p):
    '''np_add_paren : '''
    global operators
    operators.append(p[-1])

def p_np_pop_paren(p):
    '''np_pop_paren : '''
    global operators
    if operators[-1] != '(':
        create_error('Error, not ( in operators stack', 'C-02')
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
    operator = operators.pop()          # = 
    right_operand = operands.pop()
    right_type = types.pop()
    left_operand = operands.pop()
    left_type = types.pop()
    res_type = Operation.getType(operator, right_type, left_type)
    if res_type == 'Error':
        create_error(f'Invalid operation, type mismatch on {right_type}, and {left_type} with a {operator}', 'C-03')
    set_new_quadruple(operator, right_operand, -1, left_operand)

def p_np_condition_gotof(p):
    '''np_condition_gotof : '''
    global operands, types, quadruples, jumps
    res_if_type = types.pop()
    if res_if_type != Data_types['BOOLEAN']:
        create_error(f'Error, type mismatch on if statement, it must be a boolean', 'C-04')
    res_if = operands.pop()
    set_new_quadruple('GOTOF', res_if, -1, -1)
    jumps.append(len(quadruples) - 1)

def p_np_condition_end_gotof(p):
    '''np_condition_end_gotof : '''
    global jumps, quadruples
    jump_end_pos = jumps.pop()
    old_quadruple = quadruples[jump_end_pos]
    old_quadruple.set_result(len(quadruples))


def p_np_condition_goto_else(p):
    '''np_condition_goto_else : '''
    set_new_quadruple('GOTO', -1, -1, -1)
    jump_end_pos = jumps.pop()
    jumps.append(len(quadruples) - 1)
    old_quadruple = quadruples[jump_end_pos]
    old_quadruple.set_result(len(quadruples))

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
        create_error('Type-mismatch on While expresion, it must be a boolean on a while expression', 'C-05')
    exp_res = operands.pop()
    # Generate quadruple, the result reamins
    set_new_quadruple('GOTOF', exp_res, -1, -1)
    jumps.append(len(quadruples) - 1)

def p_np_while_end_block (p):
    '''np_while_end_block : '''
    end_pos = jumps.pop()
    return_pos = jumps.pop()
    # Generate quadruple, the result reamins
    set_new_quadruple('GOTO', -1, -1, return_pos)
    # Update the quadr
    old_quadruple = quadruples[end_pos]
    old_quadruple.set_result(len(quadruples))


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
        create_error(f'Conditional variable of "For" must be an integer', 'C-06')
    set_new_quadruple(operator, right_operand, -1, left_operand)
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
        create_error('Invalid type in "For" statement (stop condition), must be boolean', 'C-07')
    set_new_quadruple('GOTOV', result, -1, -1)
    jumps.append(len(quadruples) - 1)
    

def p_np_non_conditional_end (p):
    '''np_non_conditional_end : '''
    global operators, operands, types, quadruples, program_scopes, current_scope, tempsCount

    delta_value = operands.pop()
    delta_type = types.pop()
    if delta_type != Data_types['INTEGER']:
        create_error('Invalid type in "For" statement in delta, must be integer', 'C-08')
    for_var_value = operands.pop()
    for_var_type = types.pop()
    res_type = Operation.getType('+', for_var_type, delta_type)
    
    if res_type == 'Error' or res_type != Data_types['INTEGER']:
        create_error(f'Invalid type in "For" expression\n type mismatch on {for_var_type} and {delta_type} with a +', 'C-09')
    
    set_new_quadruple('+', for_var_value, delta_value, for_var_value)
    end_pos = jumps.pop()
    return_pos = jumps.pop()
    set_new_quadruple('GOTO', -1, -1, return_pos)

    # Update the GOTOV quadruple
    old_quadruple = quadruples[end_pos]
    old_quadruple.set_result(len(quadruples))

# ======================================================================
#                               PRINT
# ======================================================================
'''
Create a quadruple for print
When value is on p[-1]
'''
def p_np_add_print_quadruple_str(p):
    '''np_add_print_quadruple_str : '''
    value = p[-1]
    set_new_quadruple('PRINT', -1, -1, value)

'''
Create a quadruple for print
When value is on operands stack
'''
def p_np_add_print_quadruple_exp(p):
    '''np_add_print_quadruple_exp : '''
    global operands, types
    value = operands.pop()
    v_type = types.pop()
    set_new_quadruple('PRINT', -1, -1, value)

'''
Create a quadruple for println
When value is on p[-1]
'''
def p_np_add_println_quadruple_str(p):
    '''np_add_println_quadruple_str : '''
    value = p[-1]
    set_new_quadruple('PRINTLN', -1, -1, value)

'''
Create a quadruple for println
When value is on operands stack
'''
def p_np_add_println_quadruple_exp(p):
    '''np_add_println_quadruple_exp : '''
    global operands, types
    value = operands.pop()
    v_type = types.pop()
    set_new_quadruple('PRINTLN', -1, -1, value)


# ======================================================================
#                               RETURN
# ======================================================================

'''
Return must have a value to return
'''
def p_np_add_return_quadruple(p):
    '''np_add_return_quadruple : '''
    global current_scope, program_scopes, operands, types
    func_return_type = program_scopes.get_return_type(current_scope)
    value = operands.pop()
    v_type = types.pop()
    if (v_type != func_return_type):
        create_error(f'Function {current_scope}, has a return type of {func_return_type}, and you are trying to return a {v_type}', 'C-10')
    set_new_quadruple('RETURN', -1, -1, value)

# ======================================================================
#                               Functions stuff
# ======================================================================
'''
Add the type of the current parameter to the params array of the function
Used on function declaration
Used for creating the function signature
'''
def p_np_add_params_type(p):
    '''np_add_params_type : '''
    global program_scopes, current_scope
    current_scope_params = program_scopes.get_params_array(current_scope)
    current_scope_ids_params = program_scopes.get_params_ids_array(current_scope)
    current_scope_ids_params.append(p[-4])
    current_scope_params.append(p[-2])

def p_np_set_func_start_point(p):
    '''np_set_func_start_point : '''
    global program_scopes, current_scope, quadruples
    program_scopes.set_func_cont(current_scope, len(quadruples))

def p_np_end_function(p):
    '''np_end_function : '''
    global program_scopes, current_scope, memory_counters
    set_new_quadruple('ENDFUNC', -1, -1, -1)
    # Calculate the memory that the function will use
    program_scopes.calculate_function_size(current_scope)
    # Reset temp, local and pointers values
    # TODO: pointers
    memory_counters.reset_local_counters()
    memory_counters.reset_temp_counters()
    
def p_np_end_main(p):
    '''np_end_main : '''
    global program_scopes, current_scope
    program_scopes.calculate_function_size(current_scope)
    program_scopes.calculate_function_size('program')


def p_np_end_program(p):
    '''np_end_program : '''
    set_new_quadruple('END', -1, -1, -1)


def p_np_check_function_call(p):
    '''np_check_function_call : '''
    global program_scopes, params_counts, current_scope, current_function_call_id, function_call_id_stack, operators
    current_function_call_id = p[-2]
    if not program_scopes.exists(current_function_call_id):
        create_error(f'Function {current_function_call_id} is not defined', 'C-11')
    params_counts.append(0)
    function_call_id_stack.append(current_function_call_id)
    set_new_quadruple('ERA', -1, -1, current_function_call_id)
    # Add fake buttom
    operators.append('~')

def p_np_function_call_add_param(p):
    '''np_function_call_add_param : '''
    global types, operators, params_counts, function_call_id_stack, program_scopes
    argument = operands.pop()
    argument_type = types.pop()
    params_count = params_counts.pop()
    current_function_call_id = function_call_id_stack[-1]
    function_call_params = program_scopes.get_params_array(current_function_call_id)
    
    if(function_call_params[params_count] != argument_type):
        create_error(f'''
        The {params_count + 1}º argument of function {current_function_call_id}
        should be of type {function_call_params[params_count]} and you are giving a 
        {argument_type}
        ''', 'C-12')
    set_new_quadruple('PARAM', argument, -1, f'_param_{params_count}')
    params_count += 1
    params_counts.append(params_count)
    
def p_np_function_end_params(p):
    '''np_function_end_params : '''
    global params_counts, program_scopes, current_scope, tempsCount, function_call_id_stack, operators
    params_count = params_counts.pop()
    current_function_call_id = function_call_id_stack.pop()
    function_call_params = program_scopes.get_params_array(current_function_call_id)
    size_of_params = len(function_call_params)
    # POP fake buttom
    operators.pop()
    if(size_of_params != params_count):
        create_error(f'''The function {current_function_call_id}, expected {size_of_params} 
            arguments, you gave {params_count} arguments''', 'C-13')
    initial_function_addres = program_scopes.get_func_cont(current_function_call_id)
    set_new_quadruple('GOSUB', current_function_call_id, -1, initial_function_addres)
    
    fun_return_type = program_scopes.get_return_type(current_function_call_id)
    if fun_return_type != Data_types['VOID']:
        current_scope_vars = program_scopes.get_vars_table(current_scope)
        temp_var_name = f"_temp{tempsCount}"
        tempsCount += 1
        # Create temp var on table of vars
        current_scope_vars.add_new_var(temp_var_name, fun_return_type)
        # Ger address of this temporal var, and set it on the vars table of temp_var_name
        new_address = get_vars_new_address(fun_return_type, True)
        current_scope_vars.set_address(temp_var_name, new_address)
        # Append a new quadruple to the quadruples list
        # Parche Guadalupano
        global_vars = program_scopes.get_vars_table('program')
        directory_var = global_vars.get_one(current_function_call_id)
        function_var_address = directory_var['address']
        set_new_quadruple('=', function_var_address, -1, new_address)
        # add to operands and types stacks the result
        operands.append(new_address)
        types.append(fun_return_type)

# ======================================================================
#                               Array stuff
# ======================================================================

def p_np_check_is_array(p):
    '''np_check_is_array : '''
    global operands, types, operators
    array_id = operands.pop()   
    type_array = types.pop()
    
    array_id = p[-2]
    array_id_assignment = p[-3]
    if(array_id is None):
        array_id = array_id_assignment
    
    # Get var instance from vars table for the array
    current_var = get_var(array_id)
    var_type = current_var['type']
    var_address = current_var['address']
    is_array = current_var['is_array']
    if (not is_array):
        create_error(f'{array_id} is not defined as an array.', 'C-14')
    # Add number(virtual address) and type to operands and types stacks
    operands.append(var_address)
    types.append(var_type)
    # ADD FAKE BOTTOM so expression of accessing array is contained
    operators.append('|')

def p_np_verify_array_dim(p):
    '''np_verify_array_dim : '''
    global operands, constants_table, types
    accessing_array_val = operands[-1]
    accessing_array_type = types[-1]
    array_id = p[-4]
    array_id_assignment = p[-5]
    if (array_id is None): 
        array_id = array_id_assignment
    current_var = get_var(array_id)
    array_defined_size = current_var['array_size']
    array_inferior_limit = constants_table[0]
    array_superior_limit = constants_table[array_defined_size]
    if (accessing_array_type != Data_types['INTEGER']):
        create_error(f'You are trying to access {array_id} with an {accessing_array_type} value. This must be an integer', 'C-15')
    # For example: myArray[x+1]
    # the accessing_array_val is  the virtual addres of th expression: x+1
    # the array_inferior_limit is 0 (for this language, all arrays start at 0)
    # the array_superior_limit is the defined size of the array (let myArray: int[10]) --> 10 in v address
    set_new_quadruple('VERIFY', accessing_array_val, array_inferior_limit, array_superior_limit)
    
def p_np_get_array_address(p):
    '''np_get_array_address : '''
    global operands, types, constants_table
    accessing_array_value = operands.pop()  #La posición del arreglo que se quiere (como dir de memoria)
    accessing_array_type = types.pop()      # tipo de eseo
    array_initial_address = operands.pop()  # dirreción del arreglo
    # array_type = types.pop()                # tipo del arreglo
    
    # The accessing address is set on the constants address, beacause
    # we are going to sum that address with the offset (to get the address
    # in which the n element of the array is)
    array_init_address_const_address = create_constat_int_address(array_initial_address)
    pointer_address = create_new_pointer_address()
    
    set_new_quadruple('+', accessing_array_value, array_init_address_const_address, pointer_address)
    operators.pop() # Remove fake bottom

    operands.append(pointer_address)
    
# ======================================================================
#                               READ
# ======================================================================
'''
Create the read quadruple
The structure for this one is
# READ, -1, type, variable_to_set_read_value
'''
def p_np_add_read_quadruple(p):
    '''np_add_read_quadruple : '''
    global operands, types
    var = operands.pop()
    v_type = types.pop()
    type_ID = types_ID[v_type]
    set_new_quadruple('READ', -1, type_ID, var)

# ======================================================================
#                          SPECIAL FUNCTIONS
# ======================================================================

def p_np_add_mean_quadruple(p):
    '''np_add_mean_quadruple : '''
    create_quadruple_special_array_functions(p[-2], 'MEAN')

def p_np_add_median_quadruple(p):
    '''np_add_median_quadruple : '''
    create_quadruple_special_array_functions(p[-2], 'MEDIAN')
    
def p_np_add_random_quadruple(p):
    '''np_add_random_quadruple : '''
    result_address = define_new_temporal_address(Data_types['INTEGER'])
    # Add it to stacks so it can be used on a expression or else
    lower_limit = p[-4]
    upper_limit = p[-2]
    operands.append(result_address)
    types.append(Data_types['INTEGER'])
    # Create special function quadruple
    set_new_quadruple('RANDOM', lower_limit, upper_limit, result_address)
    
def p_np_add_variance_quadruple(p):
    '''np_add_variance_quadruple : '''
    create_quadruple_special_array_functions(p[-2], 'VARIANCE')
    
def p_np_add_p_variance_quadruple(p):
    '''np_add_p_variance_quadruple : '''
    create_quadruple_special_array_functions(p[-2], 'PVARIANCE')

def p_np_add_stdev_quadruple(p):
    '''np_add_stdev_quadruple : '''
    create_quadruple_special_array_functions(p[-2], 'STDEV')

def p_np_add_p_stdev_quadruple(p):
    '''np_add_p_stdev_quadruple : '''
    create_quadruple_special_array_functions(p[-2], 'PSTDEV')

# ==============================================================================
# ==============================================================================
# =========================== Other functions ==================================
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
This is only used from the expression 
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
            create_error(f'Invalid operation, type mismatch on {right_type} and {left_type} with a {operator}', 'C-16')
        # generate new temporal of type rest_type
        current_scope_vars = program_scopes.get_vars_table(current_scope)
        temp_var_name = f"_temp{tempsCount}"
        tempsCount += 1
        # Create temp var on table of vars
        current_scope_vars.add_new_var(temp_var_name, res_type)
        # Ger address of this temporal var, and set it on the vars table of temp_var_name
        new_address = get_vars_new_address(res_type, True)
        current_scope_vars.set_address(temp_var_name, new_address)
        # Append a new quadruple to the quadruples list
        # set_new_quadruple(operator, left_operand, right_operand, new_address)
        set_new_quadruple(operator, left_operand, right_operand, new_address)
        # add to operands and types stacks the result
        operands.append(new_address)
        types.append(res_type)
        
def create_constat_int_address(value):
    global memory_counters, constants_table
    if value not in constants_table:
        new_mem_address = memory_counters.count_const_int
        constants_table[value] = new_mem_address
        memory_counters.update_counter('const', Data_types['INTEGER'])
        return new_mem_address
    return constants_table[value]

def create_new_pointer_address():
    global memory_counters
    new_pointer_address = memory_counters.count_pointers
    memory_counters.update_counter('pointer', None)
    return new_pointer_address
    
def get_global_types_map(memory_counters):
    global_types_map = {
        Data_types['INTEGER']: memory_counters.count_global_int,
        Data_types['FLOAT']: memory_counters.count_global_float,
        Data_types['CHARACTER']: memory_counters.count_global_char,
        Data_types['BOOLEAN']: memory_counters.count_global_bool,
    }
    return global_types_map


def get_local_types_map(memory_counters):
    local_types_map = {
        Data_types['INTEGER']: memory_counters.count_local_int,
        Data_types['FLOAT']: memory_counters.count_local_float,
        Data_types['CHARACTER']: memory_counters.count_local_char,
        Data_types['BOOLEAN']: memory_counters.count_local_bool,
    }
    return local_types_map

def get_temporal_types_map(memory_counters):
    local_types_map = {
        Data_types['INTEGER']: memory_counters.count_temp_int,
        Data_types['FLOAT']: memory_counters.count_temp_float,
        Data_types['CHARACTER']: memory_counters.count_temp_char,
        Data_types['BOOLEAN']: memory_counters.count_temp_bool,
    }
    return local_types_map


'''
Get a new memory address for a new variable
'''    
def get_vars_new_address(var_type, is_temporal = False, space_to_save = 1, other_scope = None):
    global current_scope, memory_counters
    if other_scope is None:
        scope = current_scope
    else:
        scope = other_scope
    if is_temporal:
        temporal_types_map = get_temporal_types_map(memory_counters)
        new_mem_address = temporal_types_map[var_type]
        memory_counters.update_counter('temp', var_type, space_to_save)
        return new_mem_address
    if(scope == 'program'):
        global_types_map = get_global_types_map(memory_counters)
        new_mem_address = global_types_map[var_type]
        memory_counters.update_counter('global', var_type, space_to_save)
        return new_mem_address
    local_types_map = get_local_types_map(memory_counters)
    new_mem_address = local_types_map[var_type]
    memory_counters.update_counter('local', var_type, space_to_save)
    return new_mem_address


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
        create_error(f'{var_id} not found in current or global scope \n in get_var function', 'C-17')

    return directory_var

'''
Create a new instance of the Quadruple class and append it to the quadruples list
'''
def set_new_quadruple(first, second, third, fourth):
    operator_id = operators_id[first]       # convert the operator (GOTO, +, =, RETURN) to its id (number)
    new_quadruple = Quadruple(operator_id, second, third, fourth)
    quadruples.append(new_quadruple)

'''

'''
def define_new_temporal_address(type):
    global program_scopes, tempsCount, current_scope
    current_scope_vars = program_scopes.get_vars_table(current_scope)
    temp_var_name = f"_temp{tempsCount}"
    tempsCount += 1
    # Create temp var on table of vars
    current_scope_vars.add_new_var(temp_var_name, Data_types['FLOAT'])
    # Ger address of this temporal var, and set it on the vars table of temp_var_name
    new_address = get_vars_new_address(type, True)
    current_scope_vars.set_address(temp_var_name, new_address)
    return new_address

'''
This function creates the quadruple used on some of the special functions
(mean, median). It validates the array_id is an array and of integer/float
type. Then creates a new temporal variable, that is added to the operands and
types stack. So it can be used later. (the return of the function)
'''
def create_quadruple_special_array_functions(array_id, quadruple_str):
    current_var = get_var(array_id)
    var_type = current_var['type']
    array_var_address = current_var['address']
    is_array = current_var['is_array']
    array_size = current_var['array_size']
    # Validate the var is an array and of integer/float type
    if (not is_array) or (var_type not in [Data_types['INTEGER'], Data_types['FLOAT']]):
        create_error('The {quadruple_str} function only accepts an array of floats or integers.', 'C-18')
    # Create a temporal variable, this is where the result will be saved
    result_address = define_new_temporal_address(Data_types['FLOAT'])
    # Add it to stacks so it can be used on a expression or else
    operands.append(result_address)
    types.append(Data_types['FLOAT'])
    # Create special function quadruple
    set_new_quadruple(quadruple_str, array_size, array_var_address, result_address)


parser = yacc.yacc()
