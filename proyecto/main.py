import sys
from compiler.lexer import lexer
from compiler.parser import parser, program_scopes, quadruples, constants_table
from virtual_machine import execute

def print_quadruples():
    print('======================================================')
    print('\t\t\tQuadruples')
    print('======================================================')
    for indx, quad in enumerate(quadruples):
        print(indx, end='') 
        quad.print()

def print_scopes():
    print('======================================================')
    print('\t\tScopes Directory')
    print('======================================================')
    program_scopes.print_directory()

def print_constants():
    print('======================================================')
    print('\t\tConstants Directory')
    print('======================================================')
    for indx, const in enumerate(constants_table):
        print(indx, '\t\t', const, '\t\t', constants_table[const])

def main(argv):
    f = open(f"{argv[1]}", "r")
    input = f.read()
    res = parser.parse(input, debug=False)
    print(res)
    
    print_quadruples()
    # print_constants()
    # print_scopes()
    
    # Start intermediate code execution on virtual_machine
    execute()
    
if __name__ == "__main__":
    main(sys.argv)
    
    
