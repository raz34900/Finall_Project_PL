# _____ __  __ _____   ____  _____ _______ _____
# |_   _|  \/  |  __ \ / __ \|  __ \__   __/ ____|
#   | | | \  / | |__) | |  | | |__) | | | | (___
#   | | | |\/| |  ___/| |  | |  _  /  | |  \___ \
#  _| |_| |  | | |    | |__| | | \ \  | |  ____) |
# |_____|_|  |_|_|     \____/|_|  \_\ |_| |_____/

from string_with_arrows import *

#   _____ ____  _   _  _____ _______       _   _ _______ _____
#  / ____/ __ \| \ | |/ ____|__   __|/\   | \ | |__   __/ ____|
# | |   | |  | |  \| | (___    | |  /  \  |  \| |  | | | (___
# | |   | |  | | . ` |\___ \   | | / /\ \ | . ` |  | |  \___ \
# | |___| |__| | |\  |____) |  | |/ ____ \| |\  |  | |  ____) |
# \_____\____/|_| \_|_____/   |_/_/    \_\_| \_|  |_| |_____/

DIGITS = '0123456789'

# ______ _____  _____   ____  _____   _____
# |  ____|  __ \|  __ \ / __ \|  __ \ / ____|
# | |__  | |__) | |__) | |  | | |__) | (___
# |  __| |  _  /|  _  /| |  | |  _  / \___ \
# | |____| | \ \| | \ \| |__| | | \ \ ____) |
# |______|_|  \_\_|  \_\\____/|_|  \_\_____/

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __str__(self):
        result = f'\n{self.error_name}: {self.details}'
        result += f'\nFile {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def as_string(self):
        return self.__str__()


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, details = ''):
        super().__init__(pos_start, pos_end, 'RunTime Error', details)

#  _____   ____   _____ _____ _______ _____ ____  _   _
# |  __ \ / __ \ / ____|_   _|__   __|_   _/ __ \| \ | |
# | |__) | |  | | (___   | |    | |    | || |  | |  \| |
# |  ___/| |  | |\___ \  | |    | |    | || |  | | . ` |
# | |    | |__| |____) |_| |_   | |   _| || |__| | |\  |
# |_|     \____/|_____/|_____|  |_|  |_____\____/|_| \_|
#

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#  _______ ____  _  ________ _   _  _____
# |__   __/ __ \| |/ /  ____| \ | |/ ____|
#    | | | |  | | ' /| |__  |  \| | (___
#    | | | |  | |  < |  __| | . ` |\___ \
#    | | | |__| | . \| |____| |\  |____) |
#    |_|  \____/|_|\_\______|_| \_|_____/

TT_INT = 'INT'  #Integer
TT_BOOL = 'BOOL'  #Boolean
#Boolean operators
TT_AND = 'AND'  # &&
TT_OR = 'OR'  # ||
TT_NOT = 'NOT'  # !
#Comparison
TT_EQ = 'EQ'  # ==
TT_NE = 'NE'  # !=
TT_GT = 'GT'  # >
TT_LT = 'LT'  # <
TT_GE = 'GE'  # >=
TT_LE = 'LE'  # <=
#Operators
TT_PLUS = 'PLUS'  # +
TT_MINUS = 'MINUS'  # -
TT_MUL = 'MUL'  # *
TT_DIV = 'DIV'  # /
TT_MOD = 'MOD'  # %
#Functions
TT_NAME = 'NAME'  #Name
TT_LAMBDA = 'LAMBDA'  #Lambda
TT_FUNC = 'FUNC'  #Function
#......
TT_LPAREN = 'LPAREN'  # (
TT_RPAREN = 'RPAREN'  # )
TT_EOF = 'EOF'  #EOF


class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance('')
        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'


#  _      ________   ________ _____
# | |    |  ____\ \ / /  ____|  __ \
# | |    | |__   \ V /| |__  | |__) |
# | |    |  __|   > < |  __| |  _  /
# | |____| |____ / . \| |____| | \ \
# |______|______/_/ \_\______|_|  \_ \


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
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'\n")

        tokens.append(Token(TT_EOF, pos_start=self.pos))

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_INT, float(num_str), pos_start, self.pos)


#  _   _  ____  _____  ______  _____
# | \ | |/ __ \|  __ \|  ____|/ ____|
# |  \| | |  | | |  | | |__  | (___
# | . ` | |  | | |  | |  __|  \___ \
# | |\  | |__| | |__| | |____ ____) |
# |_| \_|\____/|_____/|______|_____/


class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos = tok.pos_start  ######################## added

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
class UnaryOpNode:
        def __init__(self, op_tok, node):
            self.op_tok = op_tok
            self.node = node
            self.pos_start = self.op_tok.pos_start
            #self.pos_end = self.op_tok.pos_end
            self.pos_end = getattr(node, 'pos', self.op_tok.pos_end) ################### changed

        def __repr__(self):
            return f'({self.op_tok}, {self.node})'


#  _____        _____   _____ ______   _____  ______  _____ _    _ _   _______
# |  __ \ /\   |  __ \ / ____|  ____| |  __ \|  ____|/ ____| |  | | | |__   __|
# | |__) /  \  | |__) | (___ | |__    | |__) | |__  | (___ | |  | | |    | |
# |  ___/ /\ \ |  _  / \___ \|  __|   |  _  /|  __|  \___ \| |  | | |    | |
# | |  / ____ \| | \ \ ____) | |____  | | \ \| |____ ____) | |__| | |____| |
# |_| /_/    \_\_|  \_\_____/|______| |_|  \_\______|_____/ \____/|______|_|

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


#  _____        _____   _____ ______ _____
# |  __ \ /\   |  __ \ / ____|  ____|  __ \
# | |__) /  \  | |__) | (___ | |__  | |__) |
# |  ___/ /\ \ |  _  / \___ \|  __| |  _  /
# | |  / ____ \| | \ \ ____) | |____| | \ \
# |_| /_/    \_\_|  \_\_____/|______|_|  \_\

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    ############################
    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected '+', '-', '*', '%', or '/'"))
        return res

    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TT_INT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected ')'"))

        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, 'Expected int'))


    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    ########################
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

#  _____  _    _ _   _ _______ _____ __  __ ______    _____  ______  _____ _    _ _   _______
# |  __ \| |  | | \ | |__   __|_   _|  \/  |  ____|  |  __ \|  ____|/ ____| |  | | | |__   __|
# | |__) | |  | |  \| |  | |    | | | \  / | |__     | |__) | |__  | (___ | |  | | |    | |
# |  _  /| |  | | . ` |  | |    | | | |\/| |  __|    |  _  /|  __|  \___ \| |  | | |    | |
# | | \ \| |__| | |\  |  | |   _| |_| |  | | |____   | | \ \| |____ ____) | |__| | |____| |
# |_|  \_\\____/|_| \_|  |_|  |_____|_|  |_|______|  |_|  \_\______|_____/ \____/|______|_|

class RunTimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    # def register(self, res): ################## instance added to the function
    #     if isinstance(res, RunTimeResult):
    #         if res.error: self.error = res.error
    #         return res.value
    #     return res

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

# __      __     _     _    _ ______  _____
# \ \    / /\   | |   | |  | |  ____|/ ____|
#  \ \  / /  \  | |   | |  | | |__  | (___
#   \ \/ / /\ \ | |   | |  | |  __|  \___ \
#    \  / ____ \| |___| |__| | |____ ____) |
#     \/_/    \_\______\____/|______|_____/


class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start = None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value) , None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value) , None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(other.pos_start, other.pos_end, 'Division by zero')
            return Number(self.value / other.value), None


    def moded_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(other.pos_start, other.pos_end, 'Modulo by zero')
            return Number(self.value % other.value) , None

    def __repr__(self):
        return str(self.value)



#  _____ _   _ _______ ______ _____  _____  _____  ______ _______ ______ _____
# |_   _| \ | |__   __|  ____|  __ \|  __ \|  __ \|  ____|__   __|  ____|  __ \
#   | | |  \| |  | |  | |__  | |__) | |__) | |__) | |__     | |  | |__  | |__) |
#   | | | . ` |  | |  |  __| |  _  /|  ___/|  _  /|  __|    | |  |  __| |  _  /
#  _| |_| |\  |  | |  | |____| | \ \| |    | | \ \| |____   | |  | |____| | \ \
# |_____|_| \_|  |_|  |______|_|  \_\_|    |_|  \_\______|  |_|  |______|_|  \_\

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ############################################


    def visit_NumberNode(self, node):
        return RunTimeResult().success(
            Number(node.tok.value).set_pos(node.pos_start, node.pos_end))
    def visit_BinOpNode(self, node):
        res = RunTimeResult()
        left = res.register(self.visit(node.left_node))
        if res.error: return res
        right = res.register(self.visit(node.right_node))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error =  left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.moded_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))


    def visit_UnaryOpNode(self, node):
        res = RunTimeResult()
        number = res.register(self.visit(node.node))
        if res.error: return res

        error = None
        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))





#  _____  _    _ _   _
# |  __ \| |  | | \ | |
# | |__) | |  | |  \| |
# |  _  /| |  | | . ` |
# | | \ \| |__| | |\  |
# |_|  \_\\____/|_| \_|


def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # General AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    #Run the interpreter
    interpreter = Interpreter()
    result = interpreter.visit(ast.node)

    return result.value, result.error




