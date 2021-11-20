import sys
import operator
from collections import deque
from compiler.parser import program_scopes, quadruples, constants_table
from compiler.utils import Data_types

# This var, indicates the amount of available spaces in memory
memory_size = 1000

class Memory:
    def __init__(self):
        self.memory = {}

types_values = {
    1: Data_types['INTEGER'],
    2: Data_types['FLOAT'],
    3: Data_types['CHARACTER'],
    4: Data_types['BOOLEAN'],
}

is_executing = True
instruction_pointer = 0

# Cuando empiece tiene que ir directo al main
# pero para eso tengo que crear una memoria

super_memory = Memory()
current_memory = None
memory_stack = deque()

params_queue = deque()
instruction_pointer_stack = deque()
id_function_calls = deque()


'''
print memory map
'''
def print_super_memory():
    global super_memory
    for index, address in enumerate(super_memory.memory):
        print(index, '\t\t', address, '\t\t', super_memory.memory[address])
def print_current_memory():
    global current_memory
    for index, address in enumerate(current_memory.memory):
        print(index, '\t\t', address, '\t\t', current_memory.memory[address])

def check_and_update_memory(size, id):
    global memory_size
    if (size > memory_size):
        create_error('This program cannot be executed due to lack of available memory', id)
    memory_size -= size
    
'''
On VM starts, this function is called
This loads constants on super_memory
and it checks for memory size
'''
def start_super_memory():
    global constants_table, super_memory, memory_size
    # Load Constants
    for index, constant in enumerate(constants_table):
        address = constants_table[constant]
        super_memory.memory[address] = constant
    global_size = len(constants_table)
    global_size += program_scopes.get_total_size('program')
    check_and_update_memory(global_size, 1)
    

def start_main_memory():
    global current_memory, memory_stack
    main_size = program_scopes.get_total_size('main')
    check_and_update_memory(main_size, 2)
    # Create the memory for main scope
    current_memory = Memory()
'''
Create print an error message and exit the program
'''
def create_error(message, id = ''):
    print('====================================')
    print(f'Error:\t ID:{id}\n')
    print(message)
    print('====================================')
    sys.exit()

    
def find_address(pointer):
    if pointer in current_memory.memory:
        value = current_memory.memory[pointer]
    elif pointer in super_memory.memory:
        value = super_memory.memory[pointer]
    else:
        create_error(f'{pointer} hasnt been assigned', 3)
        
    if (value == 'true'):
        value = True
    if (value == 'false'):
        value = False
    return value

def get_value(address):
    global super_memory, current_memory
    if (str(address)[0] == '5'):
        address = find_address(address)
    value = find_address(address)
    return value


def save_value(address, value):
    global super_memory, current_memory
    memory_section = int(address / 100000)
    is_global_var = lambda memory_section : memory_section is 1
    if is_global_var(memory_section):
        super_memory.memory[address] = value
    else:
        current_memory.memory[address] = value
    
def update_instruction_pointer(new_position = None):
    global instruction_pointer
    if new_position is None:
        new_position = instruction_pointer + 1
    if (new_position > len(quadruples)):
        create_error('Instruction pointer is trying to access {new_position}, that doesnt exits', 4)
    instruction_pointer = new_position
    
def generic_operation (first, second, address_to_save, operation):
    first_value = get_value(first)
    second_value = get_value(second)
    result = operation(first_value, second_value)
    save_value(address_to_save, result)

def assing_value(value_address, address_to_save):
    if (str(address_to_save)[0] == '5'):
        address_to_save = find_address(address_to_save)
    
    value = get_value(value_address)
    save_value(address_to_save, value)

def print_value(value):
    if(type(value) is int): # is an address
        value_to_print = get_value(value)
    else:   # is a string
        value_to_print = value[1:-1]
    print(value_to_print)

def save_memory_for_function(function_id):
    global program_scopes
    if not program_scopes.exists(function_id):
        create_error(f'{function_id} is not defined on this program', 5)
    func_size = program_scopes.get_total_size(function_id)
    # Save memory space for function
    check_and_update_memory(func_size, 6)
    
def go_to_function(function_id, new_instruction_pomter):
    global memory_stack, instruction_pointer_stack, program_scopes, instruction_pointer, current_memory, id_function_calls, params_queue
    params_ids = program_scopes.get_params_ids_array(function_id)
    # Create instance of memory for function
    new_current_memory = Memory()
    # If function should receive params
    if len(params_ids) is not 0:
        for param_id in params_ids:
            var_address = get_function_scope_var_address(function_id, param_id)
            param_value = get_value(params_queue.popleft())
            new_current_memory.memory[var_address] = param_value
    # Save instruction pointer
    # Add 1, so its after the gosub quadruple
    instruction_pointer_stack.append(instruction_pointer + 1)
    update_instruction_pointer(new_instruction_pomter)
    # Save current memory (send it to bed) and set up the new one
    memory_stack.append(current_memory)
    current_memory = new_current_memory
    # Save the id of the function
    id_function_calls.append(function_id)



def on_function_end():
    global id_function_calls, program_scopes, instruction_pointer_stack, current_memory, memory_stack, memory_size
    # If this is the case, then the function must be void
    function_id = id_function_calls.pop()
    func_return_type = program_scopes.get_return_type(function_id)
    if func_return_type != Data_types['VOID']:
        create_error(f'Function {function_id}, must have a return statement, with a value of type {func_return_type}', 7)
    # Wake up old current memory
    new_current_memory = memory_stack.pop()
    # Get old instruction pointer
    new_instruction_pointer = instruction_pointer_stack.pop()
    # change the current memory to the old one, the other is deleted (because Im using python)
    current_memory = new_current_memory
    update_instruction_pointer(new_instruction_pointer)
    # free memory space
    func_size = program_scopes.get_total_size(function_id)
    memory_size += func_size
    
def get_function_global_var_address(function_id):
    global program_scopes
    global_vars = program_scopes.get_vars_table('program')
    directory_var = global_vars.get_one(function_id)
    return directory_var['address']

def get_function_scope_var_address(scope_id, var_id):
    global program_scopes
    scope_vars = program_scopes.get_vars_table(scope_id)
    directory_var = scope_vars.get_one(var_id)
    return directory_var['address']


def on_function_end_with_return(return_value_address):
    global id_function_calls, program_scopes, instruction_pointer_stack, current_memory, memory_stack, memory_size
    # If this is the case, then the returned value must be of the type
    # and parche guadalupano
    function_id = id_function_calls.pop()
    func_return_type = program_scopes.get_return_type(function_id)
    type_return_value_number = str(return_value_address)[1]
    if types_values[int(type_return_value_number)] != func_return_type:
        create_error(f'Function {function_id} shoud be returning a {func_return_type}, instead it is being returned a {types_values[str(return_value_address)[1]]}', 8)
    global_var_address = get_function_global_var_address(function_id)
    returned_value = get_value(return_value_address)
    save_value(global_var_address, returned_value)
    # Wake up old current memory
    new_current_memory = memory_stack.pop()
    # Get old instruction pointer
    new_instruction_pointer = instruction_pointer_stack.pop()
    # change the current memory to the old one, the other is deleted (because Im using python)
    current_memory = new_current_memory
    update_instruction_pointer(new_instruction_pointer)
        # free memory space
    func_size = program_scopes.get_total_size(function_id)
    memory_size += func_size
    
def add_param_for_function_call(value_address):
    global params_queue
    params_queue.append(value_address)
    
def save_value_on_input(address_to_save, type_to_read):
    input_value = input()
    try:
        if type_to_read == 1:           # INT
            input_value = int(input_value)
        elif type_to_read == 2:         # FLOAT
            input_value = float(input_value)
        elif type_to_read == 3:         # CHARACTER
            input_value = str(input_value)
            if len(input_value) > 1:
                create_error(f'The input value is not a valid type, for a character is must be of length 1. ', 10)
        elif type_to_read == 4:         # BOOL
            if input_value == 'true':
                input_value = True
            elif input_value == 'false':
                input_value = False
            else:
                create_error(f'For boolean values, you must provide "false" or "true"', 11)
    except:
        create_error(f'The read statement expected a {types_values[type_to_read]}.', 12)
    
        
    if (str(address_to_save)[0] == '5'):
        address_to_save = find_address(address_to_save)
    
    save_value(address_to_save, input_value)
    

def verify_array_address_access(access_value, arr_inferior_limit, arr_upp_limit):
    value = get_value(access_value)
    inferior_limit = get_value(arr_inferior_limit)
    upper_limit = get_value(arr_upp_limit)
    if value < inferior_limit or value >= upper_limit:
        create_error(f'Out of bounds\n Trying to acces value {value}, but limits are {inferior_limit} and {upper_limit}', 9)


    
    
def check_quadruples():
    global is_executing, instruction_pointer

    while is_executing:
        
        operation = quadruples[instruction_pointer].get_operator()
        left_operand = quadruples[instruction_pointer].get_left_operand()
        right_operand = quadruples[instruction_pointer].get_right_operand()
        result = quadruples[instruction_pointer].get_result()
        # print(operation)
        # print(instruction_pointer)
        # print(operation, left_operand, right_operand, result)
        
        if operation == 27:         # END - used for end of program
            is_executing = False
            print('-Execution-ended-')
        elif operation == 1:        # + SUM
            # quadruple structure:
            # + , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.add)
            update_instruction_pointer()
        elif operation == 2:        # - SUBSTRACTION
            # quadruple structure:
            # - , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.sub)
            update_instruction_pointer()
        elif operation == 3:        # / DIVISION
            # quadruple structure:
            # / , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.truediv)
            update_instruction_pointer()
        elif operation == 4:        # * MULTIPLICATION
            # quadruple structure:
            # / , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.mul)
            update_instruction_pointer()
        elif operation == 5:        # < LESS THAN
            # quadruple structure:
            # < , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.lt)
            update_instruction_pointer()
        elif operation == 6:        # <= LESS EQUAL THAN
            # quadruple structure:
            # <= , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.le)
            update_instruction_pointer()
        elif operation == 7:        # > GREATER THAN 
            # quadruple structure:
            # > , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.gt)
            update_instruction_pointer()
        elif operation == 8:        # >= GREATER EQUAL THAN 
            # quadruple structure:
            # >= , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.ge)
            update_instruction_pointer()
        elif operation == 9:        # == EQUAL 
            # quadruple structure:
            # == , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.eq)
            update_instruction_pointer()
        elif operation == 10:        # != NOT EQUAL 
            # quadruple structure:
            # != , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.ne)
            update_instruction_pointer()
        elif operation == 11:        # && AND
            # quadruple structure:
            # && , leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.and_)
            update_instruction_pointer()
        elif operation == 12:        # || OR
            # quadruple structure:
            # ||, leftOperand, rigtOperand, save_result_in_this_address
            generic_operation(left_operand, right_operand, result, operator.or_)
            update_instruction_pointer()
        elif operation == 13:        # = ASSIGNMENT
            # quadruple structure:
            # = , value_to_assign, -, place_to_assign
            assing_value(left_operand, result)
            update_instruction_pointer()
        elif operation == 20:       # GOTO
            # quadruple structure:
            # GOTO, -, -, new_instruction_pointer
            update_instruction_pointer(result)
        elif operation == 21:       # GOTOV
            # quadruple structure:
            # GOTOV, bool_value, -, new_instruction_pointer
            if (get_value(left_operand)):
                update_instruction_pointer(result)
            else:
                update_instruction_pointer()
        elif operation == 22:       # GOTOF
            # quadruple structure:
            # GOTOF, bool_value, -, new_instruction_pointer
            if (get_value(left_operand)):
                update_instruction_pointer()
            else:
                update_instruction_pointer(result)
        elif operation == 23:        # GOSUB
            # quadruple structure:
            # GOSUB, function_id, -, new_instruction_pointer
            go_to_function(left_operand, result)
        elif operation == 24:        # ERA
            # quadruple structure:
            # ERA, -, -, function_id
            save_memory_for_function(result)
            update_instruction_pointer()
        elif operation == 25:        # PARAM
            # quadruple structure:
            # PARAM, value, -, _param_#
            add_param_for_function_call(left_operand)
            update_instruction_pointer()
        elif operation == 26:        # ENDFUNC
            # quadruple structure:
            # ENDFUNC, -, -, -
            on_function_end()
        elif operation == 30:        # RETURN
            # quadruple structure:
            # RETURN, -, -, value
            on_function_end_with_return(result)
        elif operation == 31:       # PRINT 
            # quadruple structure:
            # PRINT , -, -, value_to_print
            print_value(result)
            update_instruction_pointer()
        elif operation == 32:       # VERIFY 
            # quadruple structure:
            # VERIFY , access_value, arr_inferior_limit, arr_sup_limit
            verify_array_address_access(left_operand, right_operand, result)
            update_instruction_pointer()
        elif operation == 33:       # READ 
            # quadruple structure:
            # READ , -1, type, address_to_save_value
            save_value_on_input(result, right_operand)
            update_instruction_pointer()
        else:
            instruction_pointer += 1


def execute():
    print('======================================================')
    print('\t\tStarts virtual machine')
    print('======================================================')
    start_super_memory()
    start_main_memory()
    print('-Execution-starts-')
    check_quadruples()
    # print('=global==')
    # print_super_memory()
    # print('=last current==')
    # print_current_memory()
 