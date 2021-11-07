import sys
from lexer import lexer
from parser import parser, program_scopes, quadruples



def main(argv):
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

if __name__ == "__main__":
    main(sys.argv)