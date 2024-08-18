############################
# CONSTANTS
############################

DIGITS = '0123456789'


############################
# ERRORS
############################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details


    def __str__(self):
        result = f'{self.error_name}: {self.details}'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

    def as_string(self):
        return self.__str__()

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


############################
# POSITION
############################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)





############################
# TOKENS
############################

#DataTypes
TT_INT = 'TT_INT' #Integer
TT_BOOL = 'TT_BOOL' #Boolean
#Boolean operators
TT_AND = 'TT_AND' # &&
TT_OR = 'TT_OR' # ||
TT_NOT = 'TT_NOT' # !
#Comparison
TT_EQ = 'TT_EQ' # ==
TT_NE = 'TT_NE' # !=
TT_GT = 'TT_GT' # >
TT_LT = 'TT_LT' # <
TT_GE = 'TT_GE' # >=
TT_LE = 'TT_LE' # <=
#Operators
TT_PLUS = 'TT_PLUS' # +
TT_MINUS = 'TT_MINUS' # -
TT_MUL = 'TT_MUL' # *
TT_DIV = 'TT_DIV' # /
TT_MOD = 'TT_MOD' # %
#Functions
TT_NAME = 'TT_NAME' #Name
TT_LAMBDA = 'TT_LAMBDA' #Lambda
TT_FUNC = 'TT_FUNC' #Function
#......

class Token:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

############################
# LEXER
############################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = (Position(-1, 0, -1, fn, text))
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:

                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'\n")


        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_INT, float(num_str))


############################
#RUN
############################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
