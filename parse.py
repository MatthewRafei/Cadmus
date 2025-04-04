from tokens import *
from model import *
from lexer import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0

    def advance(self):
        token = self.tokens[self.curr]
        self.curr = self.curr + 1
        return token

    def peek(self):
        return self.tokens[self.curr]

    def is_next(self, expected_type):
        
        # Overflow protection
        if self.curr >= len(self.tokens):
            return False

        return self.peek().token_type == expected_type

    def expect(self, expected_type):
        # Overflow protection
        if self.curr >= len(self.tokens):
            print(f'Found {self.previous_token().lexme!r} at the end of parsing')
        elif self.peek().token_type == expected_type:
            token = self.advance()
            return token
        else:
            raise SyntaxError(f'Expected {exptected_type!r}, found {self.peek().lexme!r}.')

    def previous_token(self):
        return self.tokens[self.curr - 1]

    def match(self, expected_type):
        if self.curr >= len(self.tokens):
            return False
        if self.peek().token_type != expected_type:
            return False
        self.curr = self.curr + 1
        return True
    
#########################################################################
    
    def primary(self):

        # RETURN INT
        if self.match(TOK_INTEGER):
            return Integer(int(self.previous_token().lexeme))

        # RETURN FLOAT
        if self.match(TOK_FLOAT):
            return Float(float(self.previous_token().lexeme))
        
        if self.match(TOK_LPAREN):
            # GOTO EXPRESSION
            expr = self.expr()
            if (not self.match(TOK_RPARN)):
                raise SyntaxError(f'Error: ")" expected.')
            else:
                # RETURN GROUPING
                return Grouping(expr)
        
    def unary(self):
        if self.match(TOK_NOT) or self.match(TOK_MINUS) or self.match(TOK_PLUS):
            op = self.previous_token()
            # GOTO UNARY
            operand = self.unary() # Recusrive because of cases like ~~~~x ++++y ----z
            # RETURN UNOP
            return UnOp(op, operand)
        # GOTO PRIMARY
        # RETURN PRIMARY
        return self.primary()

    def factor(self):
        # GOTO UNARY
        return self.unary()

    def term(self):
        
        # GOTO FACTOR
        expr = self.factor()
        
        while self.match(TOK_STAR) or self.match(TOK_SLASH):
            op = self.previous_token()
            # GOTO FACTOR
            right = self.factor()
            expr = BinOp(op, expr, right)

        # RETURN EXPRESSION
        return expr

    def expr(self):
        
        # GOTO TERM
        expr = self.term()
        
        while self.match(TOK_PLUS) or self.match(TOK_MINUS):
            op = self.previous_token()
            # GOTO TERM
            right = self.term()
            expr = BinOp(op, expr, right)

        # RETURN EXPRESSION
        return expr

    def parse(self):
        # GOTO EXPRESSION
        ast = self.expr()
        return ast        
