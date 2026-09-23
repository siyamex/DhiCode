# lexer.py
from dataclasses import dataclass
import token_types as tt

@dataclass
class Token:
    type: str
    literal: str
    line: int = 1
    column: int = 1

    def __repr__(self):
        return f"Token({self.type}, '{self.literal}', line={self.line}, col={self.column})"

KEYWORDS = {
    # Official keywords
    "ކަނޑައަޅާ": tt.TT_LET,
    "ވަޒީފާ": tt.TT_FUNCTION,
    "ފޮނުވާ": tt.TT_RETURN,
    "ދައްކާ": tt.TT_PRINT,
    "ނަމަ": tt.TT_IF,
    "ނޫންނަމަ": tt.TT_ELSE,
    "ހިނދު": tt.TT_WHILE,
    "ނިމުނީ": tt.TT_END,
    "އާން": tt.TT_TRUE,
    "ނޫން": tt.TT_FALSE,
    "އަދި": tt.TT_AND,
    "ނުވަތަ": tt.TT_OR,

    # Advanced keywords
    "ކޮންމެ": tt.TT_FOR,
    "ތެރޭގައި": tt.TT_IN,
    "ގެނޭ": tt.TT_IMPORT,
    "މަސައްކަތްކުރޭ": tt.TT_TRY,
    "ކުށެއް_ފެނިއްޖެނަމަ": tt.TT_CATCH,
    "އުކާލާ": tt.TT_THROW,

    # Compatibility keywords
    "ބަހައްޓާ": tt.TT_LET,
    "ފަންކް": tt.TT_FUNCTION,
    "ލިޔޭ": tt.TT_PRINT,
}

def is_thaana_char(char):
    """Check if character is in Thaana Unicode block (letters, fili, sukun)."""
    return char is not None and '\u0780' <= char <= '\u07BF'

def is_ident_start(char):
    """Check if character can start an identifier."""
    if char is None:
        return False
    return is_thaana_char(char) or char.isalpha() or char == '_'

def is_ident_part(char):
    """Check if character can be part of an identifier."""
    if char is None:
        return False
    return is_thaana_char(char) or char.isalnum() or char == '_'

class Lexer:
    def __init__(self, input_text):
        self.input = input_text
        self.position = 0
        self.read_position = 0
        self.ch = None
        self.line = 1
        self.column = 0
        self._read_char()

    def _read_char(self):
        if self.read_position >= len(self.input):
            self.ch = None
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1
        self.column += 1

    def _peek_char(self):
        if self.read_position >= len(self.input):
            return None
        return self.input[self.read_position]

    def _skip_whitespace_and_comments(self):
        while self.ch is not None:
            if self.ch == '\n':
                self.line += 1
                self.column = 0
                self._read_char()
            elif self.ch.isspace():
                self._read_char()
            elif self.ch == '/' and self._peek_char() == '/':
                # Line comment
                while self.ch is not None and self.ch != '\n':
                    self._read_char()
            elif self.ch == '/' and self._peek_char() == '*':
                # Block comment
                self._read_char() # consume '/'
                self._read_char() # consume '*'
                while self.ch is not None:
                    if self.ch == '\n':
                        self.line += 1
                        self.column = 0
                    if self.ch == '*' and self._peek_char() == '/':
                        self._read_char() # consume '*'
                        self._read_char() # consume '/'
                        break
                    self._read_char()
            else:
                break

    def _read_identifier(self):
        start_col = self.column
        start_pos = self.position
        while is_ident_part(self.ch):
            self._read_char()
        literal = self.input[start_pos:self.position]
        token_type = KEYWORDS.get(literal, tt.TT_IDENTIFIER)
        return Token(token_type, literal, self.line, start_col)

    def _read_number(self):
        start_col = self.column
        start_pos = self.position
        has_dot = False
        while self.ch is not None and (self.ch.isdigit() or (self.ch == '.' and not has_dot and self._peek_char() and self._peek_char().isdigit())):
            if self.ch == '.':
                has_dot = True
            self._read_char()
        literal = self.input[start_pos:self.position]
        return Token(tt.TT_NUMBER, literal, self.line, start_col)

    def _read_string(self):
        start_col = self.column
        self._read_char() # consume opening quote
        chars = []
        while self.ch is not None and self.ch != '"':
            if self.ch == '\\':
                self._read_char()
                if self.ch == 'n':
                    chars.append('\n')
                elif self.ch == 't':
                    chars.append('\t')
                elif self.ch == '"':
                    chars.append('"')
                elif self.ch == '\\':
                    chars.append('\\')
                elif self.ch is not None:
                    chars.append(self.ch)
            else:
                if self.ch == '\n':
                    self.line += 1
                    self.column = 0
                chars.append(self.ch)
            self._read_char()

        if self.ch is None:
            return Token(tt.TT_ILLEGAL, "".join(chars), self.line, start_col)

        self._read_char() # consume closing quote
        return Token(tt.TT_STRING, "".join(chars), self.line, start_col)

    def next_token(self):
        self._skip_whitespace_and_comments()

        if self.ch is None:
            return Token(tt.TT_EOF, "", self.line, self.column)

        col = self.column

        # Identifiers & Keywords
        if is_ident_start(self.ch):
            return self._read_identifier()

        # Numbers
        if self.ch.isdigit():
            return self._read_number()

        # Strings
        if self.ch == '"':
            return self._read_string()

        # Multi-char operators
        if self.ch == '=':
            if self._peek_char() == '=':
                self._read_char()
                self._read_char()
                return Token(tt.TT_EQ, "==", self.line, col)
            self._read_char()
            return Token(tt.TT_ASSIGN, "=", self.line, col)
        elif self.ch == '!':
            if self._peek_char() == '=':
                self._read_char()
                self._read_char()
                return Token(tt.TT_NOT_EQ, "!=", self.line, col)
            self._read_char()
            return Token(tt.TT_BANG, "!", self.line, col)
        elif self.ch == '<':
            if self._peek_char() == '=':
                self._read_char()
                self._read_char()
                return Token(tt.TT_LTE, "<=", self.line, col)
            self._read_char()
            return Token(tt.TT_LT, "<", self.line, col)
        elif self.ch == '>':
            if self._peek_char() == '=':
                self._read_char()
                self._read_char()
                return Token(tt.TT_GTE, ">=", self.line, col)
            self._read_char()
            return Token(tt.TT_GT, ">", self.line, col)

        # Single-character tokens & Delimiters
        elif self.ch == '+':
            self._read_char()
            return Token(tt.TT_PLUS, "+", self.line, col)
        elif self.ch == '-':
            self._read_char()
            return Token(tt.TT_MINUS, "-", self.line, col)
        elif self.ch == '*':
            self._read_char()
            return Token(tt.TT_ASTERISK, "*", self.line, col)
        elif self.ch == '/':
            self._read_char()
            return Token(tt.TT_SLASH, "/", self.line, col)
        elif self.ch == '%':
            self._read_char()
            return Token(tt.TT_MODULO, "%", self.line, col)
        elif self.ch == '(':
            self._read_char()
            return Token(tt.TT_LPAREN, "(", self.line, col)
        elif self.ch == ')':
            self._read_char()
            return Token(tt.TT_RPAREN, ")", self.line, col)
        elif self.ch == '{':
            self._read_char()
            return Token(tt.TT_LBRACE, "{", self.line, col)
        elif self.ch == '}':
            self._read_char()
            return Token(tt.TT_RBRACE, "}", self.line, col)
        elif self.ch == '[':
            self._read_char()
            return Token(tt.TT_LBRACKET, "[", self.line, col)
        elif self.ch == ']':
            self._read_char()
            return Token(tt.TT_RBRACKET, "]", self.line, col)
        elif self.ch == ':':
            self._read_char()
            return Token(tt.TT_COLON, ":", self.line, col)
        elif self.ch == ',':
            self._read_char()
            return Token(tt.TT_COMMA, ",", self.line, col)
        elif self.ch == ';':
            self._read_char()
            return Token(tt.TT_SEMICOLON, ";", self.line, col)
        else:
            ch = self.ch
            self._read_char()
            return Token(tt.TT_ILLEGAL, ch, self.line, col)