import sys
from compiler.lexer import lexer
from compiler.parser import parser, program_scopes, quadruples
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


def main(argv):
    f = open(f"{argv[1]}", "r")
    input = f.read()
    res = parser.parse(input, debug=False)
    
    print(res)
    print_quadruples()
    print_scopes()
    execute()
    
if __name__ == "__main__":
    main(sys.argv)
    
    
