from tokens import *

class Lexer:
    def __init__(self, source):
        #TODO:
        self.source = source
        self.start_character = 0
        self.current_character = 0
        self.current_line = 1
        self.tokens = []

    def advance(self):
        character = self.source[self.current_character]
        self.current_character = self.current_character + 1
        return character

    def add_token(self, token_type):
        self.tokens.append(Token(token_type, self.source[self.start_character, self.current_character]))

    def tokenize(self):
        while self.current_character < len(self.source):
            self.start = self.current_character
            character = self.advance()
            if character == '+':
                self.add_token(TOK_PLUS)
        return self.tokens
