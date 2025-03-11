from tokens import *

class Lexer:
    def __init__(self, source):
        self.source = source
        self.start_character = 0
        self.current_character = 0
        self.current_line = 1
        self.tokens = []

    def advance(self):
        character = self.source[self.current_character]
        self.current_character = self.current_character + 1
        return character

    def add_token(self, token_type): # Slicing syntax
        self.tokens.append(Token(token_type, self.source[self.start_character:self.current_character], self.current_line))

    def peek(self):
        return self.source[self.current_character]

    # Maybe we can represent N as something else
    def lookahead(self, n=1):

        # Overflow safe, hopefully never hit
        if self.current_line >= len(self.source):
            return '\0'
        
        return self.source[self.current_character + n]

    # character is the previous current character and current character is incremented in advanced() function at the start of the tokenize function
    def match(self, expected):
        # check for overflow
        if self.current_character >= len(self.source):
            return False

        # Check to see if current character is expected
        if self.source[self.current_character] != expected:
            return False
        
        self.current_character = self.current_character + 1 # consume character
        return True

    # Digit is printing 6 times when it should be 3 are there two passes of the source code?
    def tokenize(self):
        while self.current_character < len(self.source):
            self.start_character = self.current_character
            character = self.advance()

            # Skip blank, tabs, carriage return (CR) characters
            if character == (' ' or '\t' or '\r'):
                pass
            
            # Increment new line
            if character == '\n':
                self.current_line = self.current_line + 1
            
            # Skip comments and advance to new line
            if character == '#':
                while self.peek() != '\n' and not(self.current_character >= len(self.source)):
                    self.advance()
            
            if character == '(':
                self.add_token(TOK_LPAREN)
            elif character == ')':
                self.add_token(TOK_RPAREN)
            elif character == '{':
                self.add_token(TOK_LCURLY)
            elif character == '}':
                self.add_token(TOK_RCURLY)
            elif character == '[':
                self.add_token(TOK_LSQUAR)
            elif character == ']':
                self.add_token(TOK_RSQUAR)
            elif character == ',':
                self.add_token(TOK_COMMA)
            elif character == '.':
                self.add_token(TOK_DOT)
            elif character == '+':
                self.add_token(TOK_PLUS)
            elif character == '-':
                self.add_token(TOK_MINUS)
            elif character == '*':
                self.add_token(TOK_STAR)
            elif character == '/':
                self.add_token(TOK_SLASH)
            elif character == '^':
                self.add_token(TOK_CARET)
            elif character == '%':
                self.add_token(TOK_MOD)
            elif character == ';':
                self.add_token(TOK_SEMICOLON)
            elif character == '?':
                self.add_token(TOK_QUESTION)

            # Greater than or equal, greater than, less than or equal, less than
            elif character == '>':
                if self.match('='):
                    self.add_token(TOK_GE)
                elif self.match('>'):
                    self.add_token(TOK_GTGT)
                else:
                    self.add_token(TOK_GT)
            elif character == '<':
                if self.match('='):
                    self.add_token(TOK_LE)
                elif self.match('<'):
                    self.add_token(TOK_LTLT)
                else:
                    self.add_token(TOK_LT)

            # Equivalent (No equals operator as of yet)
            if character == '=':
                if self.match('='):
                    self.add_token(TOK_EQ)

            # Not equal, not
            if character == '~':
                if self.match('='):
                    self.add_token(TOK_NE)
                else:
                    self.add_token(TOK_NOT)

            # Assignment operator, colon
            if character == ':':
                if self.match('='):
                    self.add_token(TOK_ASSIGN)
                else:
                    self.add_token(TOK_COLON)

            # TODO: Check if it is a digit, then perform the logic of reading either ints or floats

            if character.isdigit():
                print("DIGIT")

            # TODO: Check if it is a ' and then perform the logic of reading a string token
            
            # TODO: Check if it is an alpha character (a letter) or _, then we must handle an identifier

        return self.tokens

