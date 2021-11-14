import sys
from compiler.lexer import lexer
from compiler.parser import parser, program_scopes, quadruples
from virtual_machine import execute


def main(argv):
    print('==============================')
    f = open(f"{argv[1]}", "r")
    input = f.read()
    res = parser.parse(input, debug=False)
    print('\t\t QUADRUPES')
    print('==================================================')
    for indx, quad in enumerate(quadruples):
        print(indx, end='') 
        quad.print()
    program_scopes.print_directory()
    print(res)

    execute()
if __name__ == "__main__":
    main(sys.argv)