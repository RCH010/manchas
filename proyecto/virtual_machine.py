from compiler.parser import program_scopes, quadruples

is_executing = True
instruction_pointer = 0


def execute():
  print('======================================================')
  print('\t\tStarts virtual machine')
  print('======================================================')
  
  check_quadruples()
        
        
def check_quadruples():
  global is_executing, instruction_pointer
  while is_executing:
    operation = quadruples[instruction_pointer].getOperator()
    print(operation)
    instruction_pointer += 1
    if operation == 27:
      is_executing = False
