import sys
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
    return super_memory[address]

def save_value(address, value):
    global super_memory
    super_memory[address] = value

def make_sum(first, second, save_address):
    first_value = get_value(first)
    second_value = get_value(second)
    sum_result = first_value + second_value
    save_value(save_address, sum_result)

def make_substraction(first, second, save_address):
    first_value = get_value(first)
    second_value = get_value(second)
    sum_result = first_value - second_value
    save_value(save_address, sum_result)

def make_division(first, second, save_address):
    first_value = get_value(first)
    second_value = get_value(second)
    sum_result = first_value / second_value
    save_value(save_address, sum_result)

def make_multiplication(first, second, save_address):
    first_value = get_value(first)
    second_value = get_value(second)
    sum_result = first_value * second_value
    save_value(save_address, sum_result)

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
        
        if operation == 27:         # END - used for end of program
            is_executing = False
            print('-Execution-ended-')
        elif operation == 20:       # GOTO
            # quadruple structure:
            # goto, -, -, new_instruction_pointer
            if (result > len(quadruples)):
                create_error('Instruction pointer is trying to access {result}, that doesnt exits')
            instruction_pointer = result
        elif operation == 1:        # + SUM
            # quadruple structure:
            # + , leftOperand, rigtOperand, save_result_in_this_address
            make_sum(left_operand, right_operand, result)
            instruction_pointer += 1
        elif operation == 2:        # - SUBSTRACTION
            # quadruple structure:
            # - , leftOperand, rigtOperand, save_result_in_this_address
            make_substraction(left_operand, right_operand, result)
            instruction_pointer += 1
        elif operation == 3:        # / DIVISION
            # quadruple structure:
            # / , leftOperand, rigtOperand, save_result_in_this_address
            make_division(left_operand, right_operand, result)
            instruction_pointer += 1
        elif operation == 4:        # * MULTIPLICATION
            # quadruple structure:
            # / , leftOperand, rigtOperand, save_result_in_this_address
            make_multiplication(left_operand, right_operand, result)
            instruction_pointer += 1
        elif operation == 13:        # = ASSIGNMENT
            # quadruple structure:
            # = , value_to_assign, -, place_to_assign
            assing_value(left_operand, result)
            instruction_pointer += 1
        elif operation == 13:        # = ASSIGNMENT
            # quadruple structure:
            # = , value_to_assign, -, place_to_assign
            assing_value(left_operand, result)
            instruction_pointer += 1
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
