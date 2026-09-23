# parser.py
from enum import IntEnum
from typing import List, Optional, Callable, Dict, Any
import token_types as tt
from lexer import Lexer, Token
from ast_nodes import (
    Program, Statement, Expression, LetStatement, ConstStatement,
    AssignmentStatement, IndexAssignmentStatement, ReturnStatement,
    PrintStatement, ExpressionStatement, BlockStatement, IfStatement,
    WhileStatement, ForInStatement, FunctionStatement, ImportStatement,
    TryCatchStatement, ThrowStatement, Identifier, NumberLiteral,
    StringLiteral, BooleanLiteral, NullLiteral, ListLiteral, DictLiteral,
    IndexExpression, PrefixExpression, InfixExpression, CallExpression,
    Parameter, ClassStatement, DestructureLetStatement, DotAssignmentStatement,
    ThisExpression, DotExpression, ArrowFunctionLiteral, RangeExpression
)

class Precedence(IntEnum):
    LOWEST = 1
    NULL_COALESCE = 2  # ??
    LOGICAL = 3        # and, or, އަދި, ނުވަތަ
    BITWISE_OR = 4     # |
    BITWISE_XOR = 5    # ^
    BITWISE_AND = 6    # &
    EQUALS = 7         # ==, !=
    LESSGREATER = 8    # >, <, <=, >=
    RANGE = 9          # ..
    BITWISE_SHIFT = 10 # <<, >>
    SUM = 11           # +, -
    PRODUCT = 12       # *, /, %
    EXPONENT = 13      # **
    PREFIX = 14        # -X, !X, ~X
    CALL = 15          # func(X)
    INDEX = 16         # array[index]
    DOT = 17           # obj.prop

PRECEDENCES: Dict[str, Precedence] = {
    tt.TT_NULL_COALESCE: Precedence.NULL_COALESCE,
    tt.TT_AND: Precedence.LOGICAL,
    tt.TT_OR: Precedence.LOGICAL,
    tt.TT_BIT_OR: Precedence.BITWISE_OR,
    tt.TT_BIT_XOR: Precedence.BITWISE_XOR,
    tt.TT_BIT_AND: Precedence.BITWISE_AND,
    tt.TT_EQ: Precedence.EQUALS,
    tt.TT_NOT_EQ: Precedence.EQUALS,
    tt.TT_LT: Precedence.LESSGREATER,
    tt.TT_GT: Precedence.LESSGREATER,
    tt.TT_LTE: Precedence.LESSGREATER,
    tt.TT_GTE: Precedence.LESSGREATER,
    tt.TT_RANGE: Precedence.RANGE,
    tt.TT_BIT_SHL: Precedence.BITWISE_SHIFT,
    tt.TT_BIT_SHR: Precedence.BITWISE_SHIFT,
    tt.TT_PLUS: Precedence.SUM,
    tt.TT_MINUS: Precedence.SUM,
    tt.TT_ASTERISK: Precedence.PRODUCT,
    tt.TT_SLASH: Precedence.PRODUCT,
    tt.TT_MODULO: Precedence.PRODUCT,
    tt.TT_EXPONENT: Precedence.EXPONENT,
    tt.TT_LPAREN: Precedence.CALL,
    tt.TT_LBRACKET: Precedence.INDEX,
    tt.TT_DOT: Precedence.DOT,
}

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.errors: List[str] = []
        self.cur_token: Token = Token(tt.TT_EOF, "")
        self.peek_token: Token = Token(tt.TT_EOF, "")

        self.prefix_parse_fns: Dict[str, Callable[[], Optional[Expression]]] = {}
        self.infix_parse_fns: Dict[str, Callable[[Expression], Optional[Expression]]] = {}

        self._register_prefix(tt.TT_IDENTIFIER, self._parse_identifier)
        self._register_prefix(tt.TT_NUMBER, self._parse_number_literal)
        self._register_prefix(tt.TT_STRING, self._parse_string_literal)
        self._register_prefix(tt.TT_TRUE, self._parse_boolean_literal)
        self._register_prefix(tt.TT_FALSE, self._parse_boolean_literal)
        self._register_prefix(tt.TT_NULL, self._parse_null_literal)
        self._register_prefix(tt.TT_BANG, self._parse_prefix_expression)
        self._register_prefix(tt.TT_MINUS, self._parse_prefix_expression)
        self._register_prefix(tt.TT_BIT_NOT, self._parse_prefix_expression)
        self._register_prefix(tt.TT_LPAREN, self._parse_grouped_expression)
        self._register_prefix(tt.TT_LBRACKET, self._parse_list_literal)
        self._register_prefix(tt.TT_LBRACE, self._parse_dict_literal)
        self._register_prefix(tt.TT_THIS, self._parse_this_expression)
        self._register_prefix(tt.TT_FUNCTION, self._parse_function_expression)

        self._register_infix(tt.TT_PLUS, self._parse_infix_expression)
        self._register_infix(tt.TT_MINUS, self._parse_infix_expression)
        self._register_infix(tt.TT_SLASH, self._parse_infix_expression)
        self._register_infix(tt.TT_ASTERISK, self._parse_infix_expression)
        self._register_infix(tt.TT_MODULO, self._parse_infix_expression)
        self._register_infix(tt.TT_EXPONENT, self._parse_infix_expression)
        self._register_infix(tt.TT_NULL_COALESCE, self._parse_infix_expression)
        self._register_infix(tt.TT_BIT_AND, self._parse_infix_expression)
        self._register_infix(tt.TT_BIT_OR, self._parse_infix_expression)
        self._register_infix(tt.TT_BIT_XOR, self._parse_infix_expression)
        self._register_infix(tt.TT_BIT_SHL, self._parse_infix_expression)
        self._register_infix(tt.TT_BIT_SHR, self._parse_infix_expression)
        self._register_infix(tt.TT_EQ, self._parse_infix_expression)
        self._register_infix(tt.TT_NOT_EQ, self._parse_infix_expression)
        self._register_infix(tt.TT_LT, self._parse_infix_expression)
        self._register_infix(tt.TT_GT, self._parse_infix_expression)
        self._register_infix(tt.TT_LTE, self._parse_infix_expression)
        self._register_infix(tt.TT_GTE, self._parse_infix_expression)
        self._register_infix(tt.TT_AND, self._parse_infix_expression)
        self._register_infix(tt.TT_OR, self._parse_infix_expression)
        self._register_infix(tt.TT_RANGE, self._parse_range_expression)
        self._register_infix(tt.TT_LPAREN, self._parse_call_expression)
        self._register_infix(tt.TT_LBRACKET, self._parse_index_expression)
        self._register_infix(tt.TT_DOT, self._parse_dot_expression)

        # Prime tokens
        self.next_token()
        self.next_token()

    def _register_prefix(self, token_type: str, fn: Callable[[], Optional[Expression]]):
        self.prefix_parse_fns[token_type] = fn

    def _register_infix(self, token_type: str, fn: Callable[[Expression], Optional[Expression]]):
        self.infix_parse_fns[token_type] = fn

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def cur_token_is(self, token_type: str) -> bool:
        return self.cur_token.type == token_type

    def peek_token_is(self, token_type: str) -> bool:
        return self.peek_token.type == token_type

    def expect_peek(self, token_type: str) -> bool:
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        self.peek_error(token_type)
        return False

    def peek_error(self, token_type: str):
        msg = f"Line {self.peek_token.line}, Col {self.peek_token.column}: Expected next token to be '{token_type}', got '{self.peek_token.type}' ('{self.peek_token.literal}')"
        self.errors.append(msg)

    def cur_precedence(self) -> Precedence:
        return PRECEDENCES.get(self.cur_token.type, Precedence.LOWEST)

    def peek_precedence(self) -> Precedence:
        return PRECEDENCES.get(self.peek_token.type, Precedence.LOWEST)

    def parse_program(self) -> Program:
        program = Program()
        while not self.cur_token_is(tt.TT_EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.next_token()
        return program

    def parse_statement(self) -> Optional[Statement]:
        if self.cur_token_is(tt.TT_LET):
            return self.parse_let_statement()
        elif self.cur_token_is(tt.TT_CONST):
            return self.parse_const_statement()
        elif self.cur_token_is(tt.TT_RETURN):
            return self.parse_return_statement()
        elif self.cur_token_is(tt.TT_PRINT):
            return self.parse_print_statement()
        elif self.cur_token_is(tt.TT_IF):
            return self.parse_if_statement()
        elif self.cur_token_is(tt.TT_WHILE):
            return self.parse_while_statement()
        elif self.cur_token_is(tt.TT_FOR):
            return self.parse_for_in_statement()
        elif self.cur_token_is(tt.TT_FUNCTION):
            return self.parse_function_statement()
        elif self.cur_token_is(tt.TT_CLASS):
            return self.parse_class_statement()
        elif self.cur_token_is(tt.TT_IMPORT):
            return self.parse_import_statement()
        elif self.cur_token_is(tt.TT_TRY):
            return self.parse_try_catch_statement()
        elif self.cur_token_is(tt.TT_THROW):
            return self.parse_throw_statement()
        elif self.cur_token_is(tt.TT_LBRACE):
            return self.parse_braced_block_statement()
        elif self.cur_token_is(tt.TT_SEMICOLON):
            return None
        else:
            return self.parse_expression_statement()

    def parse_let_statement(self) -> Optional[Statement]:
        token = self.cur_token

        # List destructuring: let [a, b] = ...
        if self.peek_token_is(tt.TT_LBRACKET):
            return self._parse_destructure_statement(token, "list", is_const=False)

        # Dict destructuring: let {a, b} = ...
        if self.peek_token_is(tt.TT_LBRACE):
            return self._parse_destructure_statement(token, "dict", is_const=False)

        if not self.expect_peek(tt.TT_IDENTIFIER):
            return None

        name = Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(tt.TT_ASSIGN):
            return None

        self.next_token()
        value = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(tt.TT_SEMICOLON):
            self.next_token()

        return LetStatement(token, name, value)

    def parse_const_statement(self) -> Optional[Statement]:
        token = self.cur_token

        # List destructuring: const [a, b] = ...
        if self.peek_token_is(tt.TT_LBRACKET):
            return self._parse_destructure_statement(token, "list", is_const=True)

        # Dict destructuring: const {a, b} = ...
        if self.peek_token_is(tt.TT_LBRACE):
            return self._parse_destructure_statement(token, "dict", is_const=True)

        if not self.expect_peek(tt.TT_IDENTIFIER):
            return None

        name = Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(tt.TT_ASSIGN):
            return None

        self.next_token()
        value = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(tt.TT_SEMICOLON):
            self.next_token()

        return ConstStatement(token, name, value)

    def _parse_destructure_statement(self, token: Token, kind: str, is_const: bool) -> Optional[DestructureLetStatement]:
        close_token = tt.TT_RBRACKET if kind == "list" else tt.TT_RBRACE
        self.next_token() # consume '[' or '{'
        names = []

        if not self.peek_token_is(close_token):
            self.next_token()
            if not self.cur_token_is(tt.TT_IDENTIFIER):
                self.errors.append(f"Line {self.cur_token.line}: ޑީސްޓްރަކްޗަރިންގ ގައި ހުންނަންވާނީ ނަންތަކެވެ: {self.cur_token.literal}")
                return None
            names.append(Identifier(self.cur_token, self.cur_token.literal))

            while self.peek_token_is(tt.TT_COMMA):
                self.next_token()
                self.next_token()
                if not self.cur_token_is(tt.TT_IDENTIFIER):
                    self.errors.append(f"Line {self.cur_token.line}: ޑީސްޓްރަކްޗަރިންގ ގައި ހުންނަންވާނީ ނަންތަކެވެ: {self.cur_token.literal}")
                    return None
                names.append(Identifier(self.cur_token, self.cur_token.literal))

        if not self.expect_peek(close_token):
            return None

        if not self.expect_peek(tt.TT_ASSIGN):
            return None

        self.next_token()
        value = self.parse_expression(Precedence.LOWEST)
        if self.peek_token_is(tt.TT_SEMICOLON):
            self.next_token()

        return DestructureLetStatement(token, kind, names, value, is_const)

    def parse_return_statement(self) -> Optional[ReturnStatement]:
        token = self.cur_token
        self.next_token()

        if self.cur_token_is(tt.TT_SEMICOLON) or self.cur_token_is(tt.TT_END) or self.cur_token_is(tt.TT_RBRACE):
            return ReturnStatement(token, None)

        val = self.parse_expression(Precedence.LOWEST)
        if self.peek_token_is(tt.TT_SEMICOLON):
            self.next_token()

        return ReturnStatement(token, val)

    def parse_print_statement(self) -> Optional[PrintStatement]:
        token = self.cur_token
        self.next_token()

        values = []
        if self.cur_token_is(tt.TT_LPAREN):
            values = self.parse_call_arguments()
        else:
            first = self.parse_expression(Precedence.LOWEST)
            if first is not None:
                values.append(first)
            while self.peek_token_is(tt.TT_COMMA):
                self.next_token()
                self.next_token()
                nxt = self.parse_expression(Precedence.LOWEST)
                if nxt is not None:
                    values.append(nxt)

        if self.peek_token_is(tt.TT_SEMICOLON):
            self.next_token()

        first_val = values[0] if values else None
        return PrintStatement(token, first_val, values)

    def parse_expression_statement(self) -> Optional[Statement]:
        token = self.cur_token
        expr = self.parse_expression(Precedence.LOWEST)
        if expr is None:
            return None

        assignment_tokens = (
            tt.TT_ASSIGN,
            tt.TT_PLUS_ASSIGN,
            tt.TT_MINUS_ASSIGN,
            tt.TT_ASTERISK_ASSIGN,
            tt.TT_SLASH_ASSIGN,
            tt.TT_MODULO_ASSIGN,
        )
        if self.peek_token.type in assignment_tokens:
            self.next_token()
            op = self.cur_token.literal
            self.next_token()
            val = self.parse_expression(Precedence.LOWEST)
            if self.peek_token_is(tt.TT_SEMICOLON):
                self.next_token()

            if isinstance(expr, Identifier):
                return AssignmentStatement(token, expr, op, val)
            elif isinstance(expr, IndexExpression):
                return IndexAssignmentStatement(token, expr.left, expr.index, op, val)
            elif isinstance(expr, DotExpression):
                return DotAssignmentStatement(token, expr.left, expr.property_name, op, val)
            else:
                self.errors.append(f"Line {token.line}, Col {token.column}: އަގު ބަދަލު ނުކުރެވޭނެ އެއްޗެއް: {expr}")
                return None

        if self.peek_token_is(tt.TT_SEMICOLON):
            self.next_token()
        return ExpressionStatement(token, expr)

    def parse_block_statement(self, stop_tokens=(tt.TT_END, tt.TT_EOF)) -> BlockStatement:
        token = self.cur_token
        block = BlockStatement(token, [])

        while not any(self.cur_token_is(t) for t in stop_tokens):
            stmt = self.parse_statement()
            if stmt is not None:
                block.statements.append(stmt)
            self.next_token()

        return block

    def parse_braced_block_statement(self) -> BlockStatement:
        token = self.cur_token
        block = BlockStatement(token, [])
        self.next_token() # consume '{'

        while not self.cur_token_is(tt.TT_RBRACE) and not self.cur_token_is(tt.TT_EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                block.statements.append(stmt)
            self.next_token()

        return block

    def parse_if_statement(self) -> Optional[IfStatement]:
        token = self.cur_token
        self.next_token() # consume 'ނަމަ'

        condition = self.parse_expression(Precedence.LOWEST)
        if condition is None:
            return None

        if self.peek_token_is(tt.TT_LBRACE):
            self.next_token()
            consequence = self.parse_braced_block_statement()
            alternative = None
            if self.peek_token_is(tt.TT_ELSE):
                self.next_token()
                if self.peek_token_is(tt.TT_LBRACE):
                    self.next_token()
                    alternative = self.parse_braced_block_statement()
            return IfStatement(token, condition, consequence, alternative)
        else:
            self.next_token()
            consequence = self.parse_block_statement(stop_tokens=(tt.TT_END, tt.TT_ELSE, tt.TT_EOF))
            alternative = None

            if self.cur_token_is(tt.TT_ELSE):
                self.next_token()
                alternative = self.parse_block_statement(stop_tokens=(tt.TT_END, tt.TT_EOF))

            return IfStatement(token, condition, consequence, alternative)

    def parse_while_statement(self) -> Optional[WhileStatement]:
        token = self.cur_token
        self.next_token() # consume 'ހިނދު'

        condition = self.parse_expression(Precedence.LOWEST)
        if condition is None:
            return None

        if self.peek_token_is(tt.TT_LBRACE):
            self.next_token()
            body = self.parse_braced_block_statement()
        else:
            self.next_token()
            body = self.parse_block_statement(stop_tokens=(tt.TT_END, tt.TT_EOF))

        return WhileStatement(token, condition, body)

    def parse_for_in_statement(self) -> Optional[ForInStatement]:
        token = self.cur_token
        if not self.expect_peek(tt.TT_IDENTIFIER):
            return None

        item = Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(tt.TT_IN):
            return None

        self.next_token()
        iterable = self.parse_expression(Precedence.LOWEST)
        if iterable is None:
            return None

        if self.peek_token_is(tt.TT_LBRACE):
            self.next_token()
            body = self.parse_braced_block_statement()
        else:
            self.next_token()
            body = self.parse_block_statement(stop_tokens=(tt.TT_END, tt.TT_EOF))

        return ForInStatement(token, item, iterable, body)

    def parse_function_statement(self) -> Optional[FunctionStatement]:
        token = self.cur_token
        if not self.expect_peek(tt.TT_IDENTIFIER):
            return None

        name = Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(tt.TT_LPAREN):
            return None

        parameters = self.parse_function_parameters()

        if self.peek_token_is(tt.TT_ARROW):
            self.next_token() # cur is '=>'
            arrow_tok = self.cur_token
            self.next_token() # advance to expression
            if self.cur_token_is(tt.TT_LBRACE):
                body = self.parse_braced_block_statement()
            else:
                expr = self.parse_expression(Precedence.LOWEST)
                if self.peek_token_is(tt.TT_SEMICOLON):
                    self.next_token()
                ret_stmt = ReturnStatement(arrow_tok, expr)
                body = BlockStatement(arrow_tok, [ret_stmt])
        elif self.peek_token_is(tt.TT_LBRACE):
            self.next_token()
            body = self.parse_braced_block_statement()
        else:
            self.next_token()
            body = self.parse_block_statement(stop_tokens=(tt.TT_END, tt.TT_EOF))

        return FunctionStatement(token, name, parameters, body)

    def parse_class_statement(self) -> Optional[ClassStatement]:
        token = self.cur_token
        if not self.expect_peek(tt.TT_IDENTIFIER):
            return None

        name = Identifier(self.cur_token, self.cur_token.literal)
        super_class = None

        if self.peek_token_is(tt.TT_EXTENDS):
            self.next_token() # consume 'extends' / 'ދަރިކޮޅު'
            if not self.expect_peek(tt.TT_IDENTIFIER):
                return None
            super_class = Identifier(self.cur_token, self.cur_token.literal)

        methods: List[FunctionStatement] = []
        is_braced = self.peek_token_is(tt.TT_LBRACE)

        if is_braced:
            self.next_token() # cur is '{'
            while not self.peek_token_is(tt.TT_RBRACE) and not self.peek_token_is(tt.TT_EOF):
                self.next_token()
                if self.cur_token_is(tt.TT_SEMICOLON):
                    continue
                if self.cur_token_is(tt.TT_FUNCTION):
                    m = self.parse_function_statement()
                    if m is not None:
                        methods.append(m)
                else:
                    self.errors.append(f"Line {self.cur_token.line}: ކްލާހެއްގެ ތެރޭގައި ހުންނަންވާނީ ވަޒީފާތަކެވެ: {self.cur_token.literal}")
                    break
            if not self.expect_peek(tt.TT_RBRACE):
                return None
        else:
            while not self.peek_token_is(tt.TT_END) and not self.peek_token_is(tt.TT_EOF):
                self.next_token()
                if self.cur_token_is(tt.TT_SEMICOLON):
                    continue
                if self.cur_token_is(tt.TT_FUNCTION):
                    m = self.parse_function_statement()
                    if m is not None:
                        methods.append(m)
                else:
                    self.errors.append(f"Line {self.cur_token.line}: ކްލާހެއްގެ ތެރޭގައި ހުންނަންވާނީ ވަޒީފާތަކެވެ: {self.cur_token.literal}")
                    break
            if not self.expect_peek(tt.TT_END):
                return None

        return ClassStatement(token, name, super_class, methods)

    def _parse_single_parameter(self) -> Optional[Parameter]:
        is_variadic = False
        tok = self.cur_token
        if self.cur_token_is(tt.TT_ELLIPSIS):
            is_variadic = True
            self.next_token()
            tok = self.cur_token

        if not self.cur_token_is(tt.TT_IDENTIFIER):
            self.errors.append(f"Line {self.cur_token.line}, Col {self.cur_token.column}: ޕެރަމީޓަރުގެ ނަން ވާންވާނީ އައިޑެންޓިފަޔަރަކަށް: {self.cur_token.literal}")
            return None

        ident = Identifier(self.cur_token, self.cur_token.literal)
        default_expr = None

        if self.peek_token_is(tt.TT_ASSIGN):
            self.next_token() # cur is '='
            self.next_token() # advance to default expression
            default_expr = self.parse_expression(Precedence.LOWEST)

        return Parameter(tok, ident, default_expr, is_variadic)

    def parse_function_parameters(self) -> List[Parameter]:
        parameters: List[Parameter] = []

        if self.peek_token_is(tt.TT_RPAREN):
            self.next_token()
            return parameters

        self.next_token()
        param = self._parse_single_parameter()
        if param is not None:
            parameters.append(param)

        while self.peek_token_is(tt.TT_COMMA):
            self.next_token()
            self.next_token()
            param = self._parse_single_parameter()
            if param is not None:
                parameters.append(param)

        if not self.expect_peek(tt.TT_RPAREN):
            return []

        return parameters

    def parse_import_statement(self) -> Optional[ImportStatement]:
        token = self.cur_token
        if not self.expect_peek(tt.TT_STRING):
            return None

        path = self.cur_token.literal
        if self.peek_token_is(tt.TT_SEMICOLON):
            self.next_token()

        return ImportStatement(token, path)

    def parse_try_catch_statement(self) -> Optional[TryCatchStatement]:
        token = self.cur_token

        if self.peek_token_is(tt.TT_LBRACE):
            self.next_token()
            try_block = self.parse_braced_block_statement()
            if not self.expect_peek(tt.TT_CATCH):
                return None
            error_var = None
            if self.peek_token_is(tt.TT_IDENTIFIER):
                self.next_token()
                error_var = Identifier(self.cur_token, self.cur_token.literal)
            if not self.expect_peek(tt.TT_LBRACE):
                return None
            catch_block = self.parse_braced_block_statement()
            return TryCatchStatement(token, try_block, error_var, catch_block)
        else:
            self.next_token()
            try_block = self.parse_block_statement(stop_tokens=(tt.TT_CATCH, tt.TT_END, tt.TT_EOF))
            if not self.cur_token_is(tt.TT_CATCH):
                self.errors.append(f"Line {self.cur_token.line}: Expected 'ކުށެއް_ފެނިއްޖެނަމަ' after 'މަސައްކަތްކުރޭ'")
                return None

            error_var = None
            if self.peek_token_is(tt.TT_IDENTIFIER):
                self.next_token()
                error_var = Identifier(self.cur_token, self.cur_token.literal)

            self.next_token()
            catch_block = self.parse_block_statement(stop_tokens=(tt.TT_END, tt.TT_EOF))

            return TryCatchStatement(token, try_block, error_var, catch_block)

    def parse_throw_statement(self) -> Optional[ThrowStatement]:
        token = self.cur_token
        self.next_token()

        expr = self.parse_expression(Precedence.LOWEST)
        if expr is None:
            return None

        if self.peek_token_is(tt.TT_SEMICOLON):
            self.next_token()

        return ThrowStatement(token, expr)

    def parse_expression(self, precedence: Precedence) -> Optional[Expression]:
        prefix = self.prefix_parse_fns.get(self.cur_token.type)
        if prefix is None:
            self.errors.append(f"Line {self.cur_token.line}, Col {self.cur_token.column}: No prefix parse function for '{self.cur_token.literal}' ({self.cur_token.type})")
            return None

        left_exp = prefix()

        while not self.peek_token_is(tt.TT_SEMICOLON) and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.type)
            if infix is None:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)

        return left_exp

    def _parse_identifier(self) -> Expression:
        return Identifier(self.cur_token, self.cur_token.literal)

    def _parse_number_literal(self) -> Optional[Expression]:
        token = self.cur_token
        try:
            if '.' in token.literal:
                val = float(token.literal)
            else:
                val = int(token.literal)
            return NumberLiteral(token, val)
        except ValueError:
            self.errors.append(f"Line {token.line}: Could not parse '{token.literal}' as number")
            return None

    def _parse_string_literal(self) -> Expression:
        return StringLiteral(self.cur_token, self.cur_token.literal)

    def _parse_boolean_literal(self) -> Expression:
        return BooleanLiteral(self.cur_token, self.cur_token_is(tt.TT_TRUE))

    def _parse_null_literal(self) -> Expression:
        return NullLiteral(self.cur_token)

    def _parse_list_literal(self) -> Optional[Expression]:
        token = self.cur_token
        elements: List[Expression] = []

        if self.peek_token_is(tt.TT_RBRACKET):
            self.next_token()
            return ListLiteral(token, elements)

        self.next_token()
        exp = self.parse_expression(Precedence.LOWEST)
        if exp is not None:
            elements.append(exp)

        while self.peek_token_is(tt.TT_COMMA):
            self.next_token()
            self.next_token()
            exp = self.parse_expression(Precedence.LOWEST)
            if exp is not None:
                elements.append(exp)

        if not self.expect_peek(tt.TT_RBRACKET):
            return None

        return ListLiteral(token, elements)

    def _parse_dict_literal(self) -> Optional[Expression]:
        token = self.cur_token
        pairs: Dict[Expression, Expression] = {}

        if self.peek_token_is(tt.TT_RBRACE):
            self.next_token()
            return DictLiteral(token, pairs)

        while not self.peek_token_is(tt.TT_RBRACE) and not self.peek_token_is(tt.TT_EOF):
            self.next_token()
            key = self.parse_expression(Precedence.LOWEST)
            if not self.expect_peek(tt.TT_COLON):
                return None
            self.next_token()
            val = self.parse_expression(Precedence.LOWEST)
            pairs[key] = val

            if not self.peek_token_is(tt.TT_RBRACE):
                if not self.expect_peek(tt.TT_COMMA):
                    return None

        if not self.expect_peek(tt.TT_RBRACE):
            return None

        return DictLiteral(token, pairs)

    def _parse_index_expression(self, left: Expression) -> Optional[Expression]:
        token = self.cur_token
        self.next_token()
        index = self.parse_expression(Precedence.LOWEST)
        if not self.expect_peek(tt.TT_RBRACKET):
            return None
        return IndexExpression(token, left, index)

    def _parse_prefix_expression(self) -> Expression:
        token = self.cur_token
        operator = token.literal
        self.next_token()
        right = self.parse_expression(Precedence.PREFIX)
        return PrefixExpression(token, operator, right)

    def _save_state(self):
        return (
            self.lexer.position,
            self.lexer.read_position,
            self.lexer.ch,
            self.lexer.line,
            self.lexer.column,
            self.cur_token,
            self.peek_token,
            len(self.errors)
        )

    def _restore_state(self, state):
        (
            self.lexer.position,
            self.lexer.read_position,
            self.lexer.ch,
            self.lexer.line,
            self.lexer.column,
            self.cur_token,
            self.peek_token,
            err_len
        ) = state
        self.errors = self.errors[:err_len]

    def _parse_arrow_body(self, arrow_tok: Token, parameters: List[Any]) -> ArrowFunctionLiteral:
        if self.cur_token_is(tt.TT_LBRACE):
            body = self.parse_braced_block_statement()
        else:
            body = self.parse_expression(Precedence.LOWEST)
        return ArrowFunctionLiteral(arrow_tok, parameters, body)

    def _try_parse_parameters(self) -> Optional[List[Parameter]]:
        parameters: List[Parameter] = []
        if self.peek_token_is(tt.TT_RPAREN):
            self.next_token()
            return parameters

        self.next_token()
        param = self._parse_single_parameter()
        if param is None:
            return None
        parameters.append(param)

        while self.peek_token_is(tt.TT_COMMA):
            self.next_token()
            self.next_token()
            param = self._parse_single_parameter()
            if param is None:
                return None
            parameters.append(param)

        if not self.expect_peek(tt.TT_RPAREN):
            return None

        return parameters

    def _parse_grouped_expression(self) -> Optional[Expression]:
        lparen_tok = self.cur_token

        # 1. Quick check for () => ...
        if self.peek_token_is(tt.TT_RPAREN):
            self.next_token() # cur is ')'
            if self.peek_token_is(tt.TT_ARROW):
                self.next_token() # cur is '=>'
                arrow_tok = self.cur_token
                self.next_token() # start of body
                return self._parse_arrow_body(arrow_tok, [])
            self.errors.append(f"Line {lparen_tok.line}, Col {lparen_tok.column}: ހުސް ކައުސް () ބޭނުމެއް ނުކުރެވޭނެ")
            return None

        # 2. Try parsing as arrow function parameters
        state = self._save_state()
        params = self._try_parse_parameters()
        if params is not None and self.cur_token_is(tt.TT_RPAREN) and self.peek_token_is(tt.TT_ARROW):
            self.next_token() # cur is '=>'
            arrow_tok = self.cur_token
            self.next_token() # start of body
            return self._parse_arrow_body(arrow_tok, params)

        # 3. Fallback: normal grouped expression
        self._restore_state(state)
        self.next_token()
        exp = self.parse_expression(Precedence.LOWEST)
        if not self.expect_peek(tt.TT_RPAREN):
            return None
        return exp

    def _parse_function_expression(self) -> Optional[Expression]:
        token = self.cur_token
        name = None
        if self.peek_token_is(tt.TT_IDENTIFIER):
            self.next_token()
            name = Identifier(self.cur_token, self.cur_token.literal)

        if not self.expect_peek(tt.TT_LPAREN):
            return None

        parameters = self.parse_function_parameters()

        if self.peek_token_is(tt.TT_ARROW):
            self.next_token() # cur is '=>'
            arrow_tok = self.cur_token
            self.next_token()
            return self._parse_arrow_body(arrow_tok, parameters)

        if self.peek_token_is(tt.TT_LBRACE):
            self.next_token()
            body = self.parse_braced_block_statement()
        else:
            self.next_token()
            body = self.parse_block_statement(stop_tokens=(tt.TT_END, tt.TT_EOF))

        ident_name = name if name is not None else Identifier(token, "")
        return FunctionStatement(token, ident_name, parameters, body)

    def _parse_this_expression(self) -> Expression:
        return ThisExpression(self.cur_token)

    def _parse_dot_expression(self, left: Expression) -> Optional[Expression]:
        token = self.cur_token
        if not self.expect_peek(tt.TT_IDENTIFIER):
            return None
        property_name = Identifier(self.cur_token, self.cur_token.literal)
        return DotExpression(token, left, property_name)

    def _parse_range_expression(self, left: Expression) -> Optional[Expression]:
        token = self.cur_token
        precedence = self.cur_precedence()
        self.next_token()
        right = self.parse_expression(precedence)
        return RangeExpression(token, left, right)

    def _parse_infix_expression(self, left: Expression) -> Expression:
        token = self.cur_token
        operator = token.literal
        precedence = self.cur_precedence()
        self.next_token()
        if token.type == tt.TT_EXPONENT:
            right = self.parse_expression(precedence - 1)
        else:
            right = self.parse_expression(precedence)
        return InfixExpression(token, left, operator, right)

    def _parse_call_expression(self, function: Expression) -> Expression:
        token = self.cur_token
        args = self.parse_call_arguments()
        return CallExpression(token, function, args)

    def parse_call_arguments(self) -> List[Expression]:
        args: List[Expression] = []

        if self.peek_token_is(tt.TT_RPAREN):
            self.next_token()
            return args

        self.next_token()
        exp = self.parse_expression(Precedence.LOWEST)
        if exp is not None:
            args.append(exp)

        while self.peek_token_is(tt.TT_COMMA):
            self.next_token()
            self.next_token()
            exp = self.parse_expression(Precedence.LOWEST)
            if exp is not None:
                args.append(exp)

        if not self.expect_peek(tt.TT_RPAREN):
            return []

        return args
