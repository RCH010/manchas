import sys
import operator
from compiler.parser import program_scopes, quadruples, constants_table

is_executing = True
instruction_pointer = 0
super_memory = {}

'''
print memory map
'''


def print_super_memory():
    global super_memory
    for index, address in enumerate(super_memory):
        print(index, '\t\t', address, '\t\t', super_memory[address])


'''
On VM starts, this function is called
This loads constants on super_memory
'''


def load_constats():
    global constants_table, super_memory
    for index, constant in enumerate(constants_table):
        address = constants_table[constant]
        super_memory[address] = constant


'''
Create print an error message and exit the program
'''
def create_error(message):
    print('====================================')
    print('Error:\n')
    print(message)
    print('====================================')
    sys.exit()

    

def get_value(address):
    global super_memory
    if (address not in super_memory):
        create_error(f'{address} hasnt been assigned')
    value = super_memory[address]
    if (value == 'true'):
        value = True
    if (value == 'false'):
        value = False
    return value


def save_value(address, value):
    global super_memory
    # TODO: ver que debo revisar
    super_memory[address] = value
    
def update_instruction_pointer(new_position = None):
    global instruction_pointer
    if new_position is None:
        new_position = instruction_pointer + 1
    if (new_position > len(quadruples)):
        create_error('Instruction pointer is trying to access {new_position}, that doesnt exits')
    instruction_pointer = new_position
    
def generic_operation (first, second, address_to_save, operation):
    first_value = get_value(first)
    second_value = get_value(second)
    result = operation(first_value, second_value)
    save_value(address_to_save, result)

def assing_value(value_address, address_to_save):
    value = get_value(value_address)
    save_value(address_to_save, value)
    # TODO: apuntadores de arreglos

def print_value(value):
    if(type(value) is int): # is an address
        value_to_print = get_value(value)
    else:   # is a string
        value_to_print = value[1:-1]
    print(value_to_print)


def check_quadruples():
    global is_executing, instruction_pointer, super_memory

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
        elif operation == 31:       # PRINT 
            # quadruple structure:
            # PRINT , -, -, value_to_print
            print_value(result)
            instruction_pointer += 1
        else:
            instruction_pointer += 1


def execute():
    print('======================================================')
    print('\t\tStarts virtual machine')
    print('======================================================')
    load_constats()
    print('-Execution-starts-')
    check_quadruples()
    # print_super_memory()
