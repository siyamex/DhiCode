# token_types.py

# Special Tokens
TT_ILLEGAL = 'ILLEGAL'  # Token/character we don't recognize
TT_EOF     = 'EOF'      # End Of File

# Identifiers & Literals
TT_IDENTIFIER = 'IDENTIFIER' # e.g., ނަން, އުމުރު
TT_NUMBER     = 'NUMBER'     # e.g., 123, 45
TT_STRING     = 'STRING'     # e.g., "މަރުޙަބާ"

# Operators
TT_ASSIGN   = '='
TT_PLUS     = '+'
TT_GT       = '>' # Greater than
# Add other operators later (-, *, /, <, ==, etc.)

# Keywords (we'll map specific strings to this type later)
TT_KEYWORD = 'KEYWORD'

# Delimiters (example, add more as needed)
TT_LPAREN   = '('
TT_RPAREN   = ')'
TT_DQUOTE   = '"' # Double Quote for strings

# Potentially add: TT_SEMICOLON, TT_COMMA, etc. if your language uses them