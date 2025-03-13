from tokens import *

class Lexer:
    def __init__(self, source):
        self.source = source
        self.start_character = 0
        self.current_character = 0
        self.current_line = 1
        self.tokens = []

    def advance(self, n = 1):
        character = self.source[self.current_character]
        self.current_character = self.current_character + n
        return character

    def add_token(self, token_type): # Slicing syntax
        self.tokens.append(Token(token_type, \
                                 self.source[self.start_character:self.current_character], \
                                 self.current_line))

    def peek(self):
        # Overflow safe, has hit when file was too long
        # due to logic used in tokenizing identifiers.
        # IDK why maybe there is a bug in identifiers that needs to get fixed
        if self.current_character >= len(self.source):
            return '\0'
        return self.source[self.current_character]

    # Maybe we can represent N as something else
    def lookahead(self, n=1):
        # Overflow safe, hopefully never hit
        # changed from current_line to current_character
        if self.current_character + n >= len(self.source):
            return '\0'

        return self.source[self.current_character + n]

    # character is the previous current character and
    # current character is incremented in advanced()
    # function at the start of the tokenize function

    # NOTE: Maybe match should not consume character
    def match(self, expected):
        # check for overflow
        if self.current_character >= len(self.source):
            return False

        # Check to see if current character is expected
        if self.source[self.current_character] != expected:
            return False

        self.current_character += 1 # consume character
        return True

    def handle_digit(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.lookahead().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
            self.add_token(TOK_FLOAT)
        else:
            self.add_token(TOK_INTEGER)

    def handle_string(self):
        # Removed bounds checking because peek has it,
        # If this fails thats why
        while self.peek().isalpha():
            self.advance()
        if self.current_character >= len(self.source):
            raise SyntaxError(f'[Line {self.current_line}] Unterminated string.')
        if self.peek() == '"' or self.peek() == '\'':
            self.advance()
            self.add_token(TOK_STRING)
        else:
            # Need better error handling
            raise SyntaxError(f'[Line {self.current_line}] Unterminated string.')

    def handle_identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        # Check to see if identifier is a keyword in the keywords dict in tokens.py
        potential_keyword = self.source[self.start_character:self.current_character]
        keyword_type = keywords.get(potential_keyword)
        
        if keyword_type == None:
            self.add_token(TOK_IDENTIFIER)
        else:
            self.add_token(keyword_type)
               
    # Digit is printing 6 times when it
    # should be 3 are there two passes of the source code?
    def tokenize(self):
        while self.current_character < len(self.source):
            self.start_character = self.current_character
            character = self.advance()
            # Skip blank, tabs, carriage return (CR) characters
            if character == (' ' or '\t' or '\r'):
                pass
            # Increment new line
            elif character == '\n':
                self.current_line = self.current_line + 1
            # Skip comments and advance to new line
            elif character == '-':
                if self.match('-'):
                    while self.peek() != '\n' and not(self.current_character >= \
                                                      len(self.source)):
                        self.advance()
                else:
                    self.add_token(TOK_MINUS)
            elif character == '(':
                # Mutli-line comments
                if self.match('*'):
                    skip = False
                    while not(self.current_character >= len(self.source)):
                        if not skip and self.peek() == '*' and self.lookahead() == ')':
                            break
                        if self.peek() == '\\':
                            skip = True
                        else:
                            skip = False
                        self.advance()
                    self.advance(n=2)
                else:
                    self.add_token(TOK_RPAREN)
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
            elif character == '*':
                # Catch an illegal nested comment
                if self.match(')'):
                    raise SyntaxError(f'[Line {self.current_line}] Error at {character} Nested comments need to be escaped.')   
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
            # Greater than or equal, greater than,
            # less than or equal, less than
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
            # Equivalent (No equals operator in the language)
            elif character == '=':
                if self.match('='):
                    self.add_token(TOK_EQ)
            # Not equal, not
            elif character == '~':
                if self.match('='):
                    self.add_token(TOK_NE)
                else:
                    self.add_token(TOK_NOT)
            # Assignment operator, colon
            elif character == ':':
                if self.match('='):
                    self.add_token(TOK_ASSIGN)
                else:
                    self.add_token(TOK_COLON)
            # Check if it is a digit, then perform the
            # logic of reading either ints or floats
            elif character.isdigit():
                self.handle_digit()            
            # Check if it is a ' or " and
            # then perform the logic of reading a string token
            elif character == '"' or character == '\'':
                self.handle_string()
            # TODO: Check if it is an alpha character (a letter) or _,.
            # then we must handle an identifier
            elif character.isalpha() or character == '_':
                self.handle_identifier()
            else:
                raise SyntaxError(f'[Line {self.current_line}] Error at {character}: Unexpected character.')

        return self.tokens





















































                                                                                                                                                                                                                                                
