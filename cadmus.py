import sys
from tokens import *
from lexer import *
from parse import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: Python3 pinky.py <filename>')
    filename = sys.argv[1]
    print(filename)

    with open(filename) as file:
        source = file.read()
        print("LEXER: ")
        tokens = Lexer(source).tokenize()
        for token in tokens:
            print(token)

        print("PARSED AST:")
        ast = Parser(tokens).parse()
        print(ast)

    
