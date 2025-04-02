# lexer.py
import token_types as tt
import sys # Used for basic error handling later if needed

# --- Token Class ---
# Using dataclass for simplicity (requires Python 3.7+)
# If using older Python, define a regular class with __init__ and __repr__
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    literal: str # The actual characters (e.g., "ކަނޑައަޅާ", "ނަން", "123")

    def __repr__(self):
        return f"Token({self.type}, '{self.literal}')"

# --- Keyword Mapping ---
# Maps Dhivehi keyword strings to the KEYWORD token type
# IMPORTANT: Ensure these strings are EXACTLY as they appear in source code
KEYWORDS = {
    "ކަނޑައަޅާ": tt.TT_KEYWORD,
    "ނަމަ": tt.TT_KEYWORD,
    "ނޫންނަމަ": tt.TT_KEYWORD,
    "ހިނދު": tt.TT_KEYWORD,
    "ވަޒީފާ": tt.TT_KEYWORD,
    "ފޮނުވާ": tt.TT_KEYWORD,
    "ދައްކާ": tt.TT_KEYWORD,
    "ނިމުނީ": tt.TT_KEYWORD,
    "އާން": tt.TT_KEYWORD, # True
    "ނޫން": tt.TT_KEYWORD, # False
    "އަދި": tt.TT_KEYWORD, # And
    "ނުވަތަ": tt.TT_KEYWORD, # Or
}

# --- Helper Function for Thaana Letters ---
# Basic check using Unicode range for Thaana.
# NOTE: This is a SIMPLIFIED check. Full Unicode handling can be more complex.
# Thaana range: U+0780 to U+07B1
def is_thaana_letter(char):
    return char is not None and '\u0780' <= char <= '\u07B1'

# --- Lexer Class ---
class Lexer:
    def __init__(self, input_text):
        self.input = input_text
        self.position = 0 # current position in input (points to current char)
        self.read_position = 0 # current reading position (after current char)
        self.ch = None # current char under examination
        self._read_char() # Initialize self.ch

    # Read next character and advance position
    def _read_char(self):
        if self.read_position >= len(self.input):
            self.ch = None # Use None to signify EOF
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    # Peek at the next character without consuming it
    def _peek_char(self):
        if self.read_position >= len(self.input):
            return None
        else:
            return self.input[self.read_position]

    # Skip whitespace characters
    def _skip_whitespace(self):
        while self.ch is not None and self.ch.isspace():
            self._read_char()

    # Read an identifier (Thaana letters for now) or keyword
    def _read_identifier(self):
        start_pos = self.position
        # Keep reading as long as it's a Thaana letter
        while is_thaana_letter(self.ch):
            self._read_char()
        # Slice the identifier string from the input
        identifier = self.input[start_pos:self.position]

        # Check if it's a keyword
        token_type = KEYWORDS.get(identifier, tt.TT_IDENTIFIER)
        return Token(token_type, identifier)

    # Read a number (integers only for now)
    def _read_number(self):
        start_pos = self.position
        while self.ch is not None and self.ch.isdigit():
            self._read_char()
        literal = self.input[start_pos:self.position]
        return Token(tt.TT_NUMBER, literal)

    # Read a string literal enclosed in double quotes
    def _read_string(self):
        start_pos = self.position + 1 # Start after the opening quote
        self._read_char() # Consume opening "

        while self.ch is not None and self.ch != '"':
             # Basic version: doesn't handle escape sequences like \" yet
             self._read_char()

        if self.ch is None:
            # Reached EOF without finding closing quote - Error!
            # For now, return an ILLEGAL token or raise an error
             return Token(tt.TT_ILLEGAL, self.input[start_pos-1:self.position]) # Include opening quote

        literal = self.input[start_pos:self.position]
        self._read_char() # Consume closing "
        return Token(tt.TT_STRING, literal)


    # --- The Main Method ---
    # Looks at the current character and returns the next token
    def next_token(self):
        tok = None

        self._skip_whitespace() # Skip spaces, tabs, newlines

        # --- Check for single/multi-character tokens ---
        if self.ch is None:
            tok = Token(tt.TT_EOF, "")
        elif self.ch == '=':
            tok = Token(tt.TT_ASSIGN, self.ch)
        elif self.ch == '+':
            tok = Token(tt.TT_PLUS, self.ch)
        elif self.ch == '>':
            tok = Token(tt.TT_GT, self.ch)
        elif self.ch == '(':
            tok = Token(tt.TT_LPAREN, self.ch)
        elif self.ch == ')':
             tok = Token(tt.TT_RPAREN, self.ch)
        elif self.ch == '"':
             return self._read_string() # String reading handles its own advancement
        # --- Check for longer tokens ---
        elif is_thaana_letter(self.ch):
            # It's either a keyword or an identifier
            return self._read_identifier() # This handles its own advancement
        elif self.ch.isdigit():
            # It's a number
            return self._read_number() # This handles its own advancement
        else:
            # Character we don't recognize
            tok = Token(tt.TT_ILLEGAL, self.ch)

        # Move to the next character *after* processing the current one
        # (unless handled by read_identifier/read_number/read_string)
        if tok is not None: # Don't advance if handled internally by read_* methods
             self._read_char()

        return tok
    
    # --- Main execution for testing ---
if __name__ == "__main__":
    # Read the DhiCode source file
    # IMPORTANT: Ensure main.dhi is saved as UTF-8
    try:
        with open('main.dhi', 'r', encoding='utf-8') as f:
            input_code = f.read()
    except FileNotFoundError:
        print("Error: main.dhi not found. Create it in the same directory.")
        sys.exit(1)
    except Exception as e:
         print(f"Error reading main.dhi: {e}")
         sys.exit(1)

    print("--- Input Code ---")
    print(input_code)
    print("--- Tokens ---")

    lexer = Lexer(input_code)
    while True:
        token = lexer.next_token()
        if token is None: # Should not happen with current logic, but good practice
            print("Error: Received None token unexpectedly.")
            break
        print(token)
        if token.type == tt.TT_EOF:
            break
        elif token.type == tt.TT_ILLEGAL:
            print(f"Illegal character found: '{token.literal}'")
            # Optionally stop on illegal tokens, or try to continue