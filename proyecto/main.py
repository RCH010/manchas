import sys
from lexer import lexer
from parser import parser

def main(argv):
    f = open(f"{argv[1]}", "r")
    input = f.read()
    res = parser.parse(input, debug=1)
    print(res)

if __name__ == "__main__":
    main(sys.argv)