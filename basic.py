# _____ __  __ _____   ____  _____ _______ _____
# |_   _|  \/  |  __ \ / __ \|  __ \__   __/ ____|
#   | | | \  / | |__) | |  | | |__) | | | | (___
#   | | | |\/| |  ___/| |  | |  _  /  | |  \___ \
#  _| |_| |  | | |    | |__| | | \ \  | |  ____) |
# |_____|_|  |_|_|     \____/|_|  \_\ |_| |_____/

from string_with_arrows import *
import string

#   _____ ____  _   _  _____ _______       _   _ _______ _____
#  / ____/ __ \| \ | |/ ____|__   __|/\   | \ | |__   __/ ____|
# | |   | |  | |  \| | (___    | |  /  \  |  \| |  | | | (___
# | |   | |  | | . ` |\___ \   | | / /\ \ | . ` |  | |  \___ \
# | |___| |__| | |\  |____) |  | |/ ____ \| |\  |  | |  ____) |
# \_____\____/|_| \_|_____/   |_/_/    \_\_| \_|  |_| |_____/

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

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
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'RunTime Error', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'\n{self.error_name}: {self.details}\n'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f' File {pos.fn}, line {pos.ln + 1}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result


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
TT_IDENTIFIER = 'IDENTIFIER'  #Identifier
TT_KEYWORD = 'KEYWORD'  #Keyword
TT_FUNC = 'FUNC'  #Function
TT_ISA = '='  #Is a
#......
TT_LPAREN = 'LPAREN'  # (
TT_RPAREN = 'RPAREN'  # )
TT_COMMA = 'COMMA'  # , 
TT_ARROW = 'ARROW'  # ->
TT_EOF = 'EOF'  #EOF

KEYWORDS = [
    'VAR',
    'AND',
    'OR',
    'NOT',
    'IF',
    'ELIF',
    'ELSE',
    'THEN',
    'FUNC'
]


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

    def matches(self, type, value):
        return self.type == type and self.value == value

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
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier()) 
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
               tokens.append(self.make_minus_or_arrow())
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
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == '<':
                tokens.append(self.make_less_than()) 
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
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
        
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()
        
        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos) 
    
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=self.pos, pos_end=self.pos), None
        self.advance()
        return None, ExpectedCharError(self.pos, self.pos, "Expected '=' after '!'")
    
    def make_equals(self):
        tok_type = TT_ISA
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type = TT_EQ
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type = TT_GE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type = TT_LE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_minus_or_arrow(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '>':
            self.advance()
            tok_type = TT_ARROW
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos) 



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

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
          
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    
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
        
class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1][0]).pos_end

         

class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks ,body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        if self.var_name_tok: # checks if the function has a name
            self.pos_start = self.var_name_tok.pos_start 
        elif len(self.arg_name_toks) > 0: # if there isnt a name then it checks if there are arguments
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start  # if there are no arguments then it checks the body node
        
        self.pos_end = self.body_node.pos_end

class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end # gets the last argument
        else:
            self.pos_end = self.node_to_call.pos_end

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

    def register_advancement(self):
        self.advance_count = 1

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
    def if_expr(self):
        res= ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, 'IF'):# checks if the current token is an if
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,
                                                   self.current_tok.pos_end, "Expected 'IF'"))
        res.register(self.advance())

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):# checks if the current token is a then
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,
                                                  self.current_tok.pos_end, "Expected 'THEN'"))
        res.register(self.advance())

        expr= res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr)) # adds the condition and the expression to the cases

        while self.current_tok.matches(TT_KEYWORD, 'ELIF'):# checks if there are more than one condition
            res.register(self.advance())

            condition = res.register(self.expr())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'THEN'):# checks if the current token is a then
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,
                                                      self.current_tok.pos_end, "Expected 'THEN'"))
            
            res.register(self.advance())

            expr= res.register(self.expr())
            if res.error: return res
            cases.append((condition, expr)) # adds the condition and the expression to the cases

        if self.current_tok.matches(TT_KEYWORD, 'ELSE'): # checks if there is an else

            res.register(self.advance())

            else_case = res.register(self.expr()) 
            if res.error: return res
        
        return res.success(IfNode(cases, else_case))





    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected '+', '-', '*', '%', '/', '==', '!=', '>', '<', '>=', '<=', 'AND', 'OR'"))
        return res

    def call(self):
        res= ParseResult()
        factor=res.register(self.factor())
        if res.error: return res

        if self.current_tok.type == TT_LPAREN: 
            res.register(self.advance())
            arg_nodes = []

            if self.current_tok.type == TT_RPAREN: # checks if there are no arguments
                res.register(self.advance())
            else: #there are arguments
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, 
                                                          self.current_tok.pos_end, "Expected ')', 'VAR', 'FUNC', int, identifier, '+', '-', '(' or 'NOT'"))
               
                while self.current_tok.type == TT_COMMA:# checks if there are more than one argument
                    res.register(self.advance())

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_tok.type != TT_RPAREN: # checks if the arguments have ended
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ',' or ')'"))
                
                res.register(self.advance())
            return res.success(CallNode(factor, arg_nodes))
        return res.success(factor)

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

        elif tok.type == TT_IDENTIFIER:
            var_name = tok
            res.register(self.advance())
        
            # Check if this is a function call
            if self.current_tok.type == TT_LPAREN:
                res.register(self.advance())
                arg_nodes = []

                if self.current_tok.type != TT_RPAREN:
                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res.failure(InvalidSyntaxError(self.current_tok.pos_start,
                                                          self.current_tok.pos_end, "Expected ')', int, identifier, '+', '-', '('"))

                    while self.current_tok.type == TT_COMMA:
                        res.register(self.advance())
                        arg_nodes.append(res.register(self.expr()))
                        if res.error: return res

                    if self.current_tok.type != TT_RPAREN:
                        return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ',' or ')'"))

                res.register(self.advance())
                return res.success(CallNode(VarAccessNode(var_name), arg_nodes))

            return res.success(VarAccessNode(var_name))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected ')'"))

        elif tok.matches(TT_KEYWORD, 'FUNC'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)
        
        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, 'Expected int, identifier, "+", "-", "("'))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD))
    
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS)) 

    def comp_expr(self):
        res= ParseResult()
        if self.current_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok = self.current_tok
            res.register(self.advance())

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))
        
        node= res.register(self.bin_op(self.arith_expr, (TT_EQ, TT_NE, TT_LT, TT_GT, TT_LE, TT_GE)))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,
                                                   self.current_tok.pos_end, "Expected int, +, -, (, 'NOT'"))
        return res.success(node)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register(self.advance())

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,
                                                      self.current_tok.pos_end, "Expected identifier"))
            var_name = self.current_tok
            res.register(self.advance())

            if self.current_tok.type != TT_ISA:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,
                                                      self.current_tok.pos_end, "Expected '='"))
            res.register(self.advance())

            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'))))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,
                                                  self.current_tok.pos_end, "Expected int, '+', '-', 'FUNC', or 'VAR'"))
        return res.success(node)
    
    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'FUNC'): # checks if the current token is a function
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, 
                                                  self.current_tok.pos_end, "Expected 'FUNC'"))
        res.register(self.advance())

        if self.current_tok.type == TT_IDENTIFIER: # checks if the function has a name
            var_name_tok = self.current_tok
            res.register(self.advance())
            if self.current_tok.type != TT_LPAREN: # checks if the function has arguments
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, 
                                                      self.current_tok.pos_end, "Expected '('"))
        else: # we didnt find a name so we check for arguments
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN: # checks if the function has arguments
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, 
                                                      self.current_tok.pos_end, "Expected identifier or '('"))
        res.register(self.advance())  
        arg_name_toks = []
        
        if self.current_tok.type == TT_IDENTIFIER: # checks if the function has arguments
            arg_name_toks.append(self.current_tok)
            res.register(self.advance())

            while self.current_tok.type == TT_COMMA: # checks if the function has more than one argument
                res.register(self.advance())
                if self.current_tok.type != TT_IDENTIFIER: # expects an identifier after a comma
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, 
                                                          self.current_tok.pos_end, "Expected identifier"))
                arg_name_toks.append(self.current_tok)
                res.register(self.advance())

            if self.current_tok.type != TT_RPAREN: # checks if the function has ended
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, 
                                                      self.current_tok.pos_end, "Expected ',' or ')'"))
        else:
            if self.current_tok.type != TT_RPAREN: # checks if the function has ended
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, 
                                                      self.current_tok.pos_end, "Expected identifier or ')'"))
        res.register(self.advance())
        if self.current_tok.type != TT_ARROW: # checks if the function has a return 
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, 
                                                  self.current_tok.pos_end, "Expected '->'"))
        res.register(self.advance())
        node_to_return = res.register(self.expr())
        if res.error: return res
        return res.success(FuncDefNode(var_name_tok, arg_name_toks, node_to_return))
            


    ########################
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
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

class Value:

    def set_pos(self, pos_start = None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self,context=None):
        self.context = context
        return self
    
    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)
    
    def moded_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_le(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ge(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def execute(self, args):
        return RunTimeResult().failure(self.illegal_operation())
    
    def is_true(self):
        return False

    def copy(self):
        raise Exception('No copy method defined')

    def illegal_operation(self, other=None):
        if not other: other = self
        return RunTimeError(
			self.pos_start, other.pos_end,
			'Illegal operation',
			self.context
		)
class Number(Value):
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context) , None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context) , None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(other.pos_start, other.pos_end, 'Division by zero', self.context)
            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)


    def moded_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(other.pos_start, other.pos_end, 'Modulo by zero')
            return Number(self.value % other.value).set_context(self.context) , None
        else:
            return None, Value.illegal_operation(self, other)
        
    def copy(self):
        new_number = Number(self.value)
        new_number.set_pos(self.pos_start, self.pos_end)
        new_number.set_context(self.context)
        return new_number
    
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_ge(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_le(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
    
    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)
    
    def copy(self):
        new_number = Number(self.value)
        new_number.set_pos(self.pos_start, self.pos_end)
        new_number.set_context(self.context)
        return new_number
    
class Function(Value):
    def __init__(self, name, body_node, arg_name):
        super().__init__()
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_name = arg_name

    def execute(self, args):
        res = RunTimeResult()
        interpreter = Interpreter()
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        # Create a trace log for function calls
        call_trace = []

        # Check if we have too many or too few arguments
        if len(args) > len(self.arg_name):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.arg_name)} too many args passed into '{self.name}'",
                self.context
            ))

        if len(args) < len(self.arg_name):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(self.arg_name) - len(args)} too few args passed into '{self.name}'",
                self.context
            ))

        # Assign the arguments to the function's local scope
        for i in range(len(args)):
            arg_name = self.arg_name[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        # Recursion support: Add the function itself to the symbol table
        new_context.symbol_table.set(self.name, self)

        # Log the function call with arguments
        arg_str = ", ".join([f"{self.arg_name[i]}={args[i]}" for i in range(len(args))])
        call_trace.append(f"Call: {self.name}({arg_str})")

        # Execute the body of the function
        value = res.register(interpreter.visit(self.body_node, new_context))
        if res.error: return res

        # Log the function return value
        call_trace.append(f"Return: {self.name} -> {value}")

        # Store the trace in the result
        return res.success((value, call_trace))

    def copy(self):
        new_function = Function(self.name, self.body_node, self.arg_name)
        new_function.set_context(self.context)
        new_function.set_pos(self.pos_start, self.pos_end)
        return new_function

    def __repr__(self):
        return f"<function {self.name}>"

#   _____ ____  _   _ _______ ________   _________
#  / ____/ __ \| \ | |__   __|  ____\ \ / /__   __|
# | |   | |  | |  \| |  | |  | |__   \ V /   | |
# | |   | |  | | . ` |  | |  |  __|   > <    | |
# | |___| |__| | |\  |  | |  | |____ / . \   | |
#  \_____\____/|_| \_|  |_|  |______/_/ \_\  |_|

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

# _______  __   __  __   __  _______  _______  ___        _______  _______  _______  ___      _______ 
# |       ||  | |  ||  |_|  ||  _    ||       ||   |      |       ||   _   ||  _    ||   |    |       |
# |  _____||  |_|  ||       || |_|   ||   _   ||   |      |_     _||  |_|  || |_|   ||   |    |    ___|
# | |_____ |       ||       ||       ||  | |  ||   |        |   |  |       ||       ||   |    |   |___ 
# |_____  ||_     _||       ||  _   | |  |_|  ||   |___     |   |  |       ||  _   | |   |___ |    ___|
#  _____| |  |   |  | ||_|| || |_|   ||       ||       |    |   |  |   _   || |_|   ||       ||   |___ 
# |_______|  |___|  |_|   |_||_______||_______||_______|    |___|  |__| |__||_______||_______||_______|

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        # Check if the variable already exists
        if name in self.symbols:
            # Instead of raising an exception, return an error message
            print(f"Variable/Function '{name}' already exists.")
            return RunTimeResult().failure(RunTimeError(None, None, f"Variable/Function '{name}' already exists.", None))
        else:
            self.symbols[name] = value
            return None  # No error, successful assignment

    def remove(self, name):
        del self.symbols[name]

    

#  _____ _   _ _______ ______ _____  _____  _____  ______ _______ ______ _____
# |_   _| \ | |__   __|  ____|  __ \|  __ \|  __ \|  ____|__   __|  ____|  __ \
#   | | |  \| |  | |  | |__  | |__) | |__) | |__) | |__     | |  | |__  | |__) |
#   | | | . ` |  | |  |  __| |  _  /|  ___/|  _  /|  __|    | |  |  __| |  _  /
#  _| |_| |\  |  | |  | |____| | \ \| |    | | \ \| |____   | |  | |____| | \ \
# |_____|_| \_|  |_|  |______|_|  \_\_|    |_|  \_\______|  |_|  |______|_|  \_\

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ############################################


    def visit_NumberNode(self, node, context):
        return RunTimeResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAssignNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value

        # Check if variable already exists
        if context.symbol_table.get(var_name) is not None:
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                f"Variable '{var_name}' already exists",
                context
            ))

        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name,value)
        return res.success(value)

    def visit_VarAccessNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        
        if not value:
            return res.failure(RunTimeError(node.pos_start, node.pos_end, f"'{var_name}' is not defined", context))
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RunTimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
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
        elif node.op_tok.type == TT_EQ:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GE:
            result, error = left.get_comparison_ge(right)
        elif node.op_tok.type == TT_LE:
            result, error = left.get_comparison_le(right)
        elif node.op_tok.matches(TT_KEYWORD, 'AND'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))


    def visit_UnaryOpNode(self, node, context):
        res = RunTimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None
        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
    
    def visit_IfNode(self, node, context):
        res=RunTimeResult()

        for condition, expr in node.cases: # checks if the condition is true for each case
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true(): # if the condition is true then it returns the expression
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)
            
        if node.else_case: # if there is an else case then it returns the expression
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)
        
        return res.success(None)
        
    def visit_FuncDefNode(self, node, context):
        res = RunTimeResult()
        func_name = node.var_name_tok.value if node.var_name_tok else None  # Check if the function has a name
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]  # Get the arguments of the function
        if func_name and context.symbol_table.get(func_name) is not None:
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                f"Function '{func_name}' already exists",
                context
            ))

        # Create the function
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start,
                                                                                            node.pos_end)

        # If the function has a name, add it to the symbol table so it can refer to itself (allow recursion)
        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RunTimeResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)  # gets the function to call

        for arg_node in node.arg_nodes:  # gets the arguments of the function
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        # Execute the function (functions are pure, no state changes)
        return_value, call_trace = res.register(value_to_call.execute(args))
        if res.error: return res

        # Print or store the call trace (if desired)
        for trace in call_trace:
            print(trace)

        return res.success(return_value)
#  _____  _    _ _   _
# |  __ \| |  | | \ | |
# | |__) | |  | |  \| |
# |  _  /| |  | | . ` |
# | | \ \| |__| | |\  |
# |_|  \_\\____/|_| \_|

global_symbol_table = SymbolTable()
global_symbol_table.set('NULL', Number(0))
global_symbol_table.set('TRUE', Number(1))
global_symbol_table.set('FALSE', Number(0))

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
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error




