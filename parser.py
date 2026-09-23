# parser.py
from enum import IntEnum
from typing import List, Optional, Callable, Dict
import token_types as tt
from lexer import Lexer, Token
from ast_nodes import (
    Program, Statement, Expression, LetStatement, ReturnStatement,
    PrintStatement, ExpressionStatement, BlockStatement, IfStatement,
    WhileStatement, ForInStatement, FunctionStatement, ImportStatement,
    TryCatchStatement, ThrowStatement, Identifier, NumberLiteral,
    StringLiteral, BooleanLiteral, ListLiteral, DictLiteral,
    IndexExpression, PrefixExpression, InfixExpression, CallExpression
)

class Precedence(IntEnum):
    LOWEST = 1
    LOGICAL = 2      # އަދި, ނުވަތަ
    EQUALS = 3       # ==, !=
    LESSGREATER = 4  # >, <, <=, >=
    SUM = 5          # +, -
    PRODUCT = 6      # *, /, %
    PREFIX = 7       # -X, !X
    CALL = 8         # func(X)
    INDEX = 9        # array[index]

PRECEDENCES: Dict[str, Precedence] = {
    tt.TT_AND: Precedence.LOGICAL,
    tt.TT_OR: Precedence.LOGICAL,
    tt.TT_EQ: Precedence.EQUALS,
    tt.TT_NOT_EQ: Precedence.EQUALS,
    tt.TT_LT: Precedence.LESSGREATER,
    tt.TT_GT: Precedence.LESSGREATER,
    tt.TT_LTE: Precedence.LESSGREATER,
    tt.TT_GTE: Precedence.LESSGREATER,
    tt.TT_PLUS: Precedence.SUM,
    tt.TT_MINUS: Precedence.SUM,
    tt.TT_ASTERISK: Precedence.PRODUCT,
    tt.TT_SLASH: Precedence.PRODUCT,
    tt.TT_MODULO: Precedence.PRODUCT,
    tt.TT_LPAREN: Precedence.CALL,
    tt.TT_LBRACKET: Precedence.INDEX,
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
        self._register_prefix(tt.TT_BANG, self._parse_prefix_expression)
        self._register_prefix(tt.TT_MINUS, self._parse_prefix_expression)
        self._register_prefix(tt.TT_LPAREN, self._parse_grouped_expression)
        self._register_prefix(tt.TT_LBRACKET, self._parse_list_literal)
        self._register_prefix(tt.TT_LBRACE, self._parse_dict_literal)

        self._register_infix(tt.TT_PLUS, self._parse_infix_expression)
        self._register_infix(tt.TT_MINUS, self._parse_infix_expression)
        self._register_infix(tt.TT_SLASH, self._parse_infix_expression)
        self._register_infix(tt.TT_ASTERISK, self._parse_infix_expression)
        self._register_infix(tt.TT_MODULO, self._parse_infix_expression)
        self._register_infix(tt.TT_EQ, self._parse_infix_expression)
        self._register_infix(tt.TT_NOT_EQ, self._parse_infix_expression)
        self._register_infix(tt.TT_LT, self._parse_infix_expression)
        self._register_infix(tt.TT_GT, self._parse_infix_expression)
        self._register_infix(tt.TT_LTE, self._parse_infix_expression)
        self._register_infix(tt.TT_GTE, self._parse_infix_expression)
        self._register_infix(tt.TT_AND, self._parse_infix_expression)
        self._register_infix(tt.TT_OR, self._parse_infix_expression)
        self._register_infix(tt.TT_LPAREN, self._parse_call_expression)
        self._register_infix(tt.TT_LBRACKET, self._parse_index_expression)

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

    def parse_let_statement(self) -> Optional[LetStatement]:
        token = self.cur_token
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

        value = self.parse_expression(Precedence.LOWEST)
        if self.peek_token_is(tt.TT_SEMICOLON):
            self.next_token()

        return PrintStatement(token, value)

    def parse_expression_statement(self) -> Optional[ExpressionStatement]:
        token = self.cur_token
        expr = self.parse_expression(Precedence.LOWEST)
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

        if self.peek_token_is(tt.TT_LBRACE):
            self.next_token()
            body = self.parse_braced_block_statement()
        else:
            self.next_token()
            body = self.parse_block_statement(stop_tokens=(tt.TT_END, tt.TT_EOF))

        return FunctionStatement(token, name, parameters, body)

    def parse_function_parameters(self) -> List[Identifier]:
        identifiers: List[Identifier] = []

        if self.peek_token_is(tt.TT_RPAREN):
            self.next_token()
            return identifiers

        self.next_token()
        identifiers.append(Identifier(self.cur_token, self.cur_token.literal))

        while self.peek_token_is(tt.TT_COMMA):
            self.next_token()
            self.next_token()
            identifiers.append(Identifier(self.cur_token, self.cur_token.literal))

        if not self.expect_peek(tt.TT_RPAREN):
            return []

        return identifiers

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

    def _parse_grouped_expression(self) -> Optional[Expression]:
        self.next_token()
        exp = self.parse_expression(Precedence.LOWEST)
        if not self.expect_peek(tt.TT_RPAREN):
            return None
        return exp

    def _parse_infix_expression(self, left: Expression) -> Expression:
        token = self.cur_token
        operator = token.literal
        precedence = self.cur_precedence()
        self.next_token()
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
