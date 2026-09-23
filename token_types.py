# token_types.py

# Special Tokens
TT_ILLEGAL = 'ILLEGAL'
TT_EOF     = 'EOF'

# Identifiers & Literals
TT_IDENTIFIER = 'IDENTIFIER'
TT_NUMBER     = 'NUMBER'
TT_STRING     = 'STRING'

# Operators
TT_ASSIGN   = '='
TT_PLUS     = '+'
TT_MINUS    = '-'
TT_ASTERISK = '*'
TT_SLASH    = '/'
TT_MODULO   = '%'
TT_BANG     = '!'
TT_EQ       = '=='
TT_NOT_EQ   = '!='
TT_LT       = '<'
TT_GT       = '>'
TT_LTE      = '<='
TT_GTE      = '>='

# Delimiters
TT_LPAREN   = '('
TT_RPAREN   = ')'
TT_LBRACE   = '{'
TT_RBRACE   = '}'
TT_LBRACKET = '['
TT_RBRACKET = ']'
TT_COLON    = ':'
TT_COMMA    = ','
TT_SEMICOLON= ';'

# Specific Keywords
TT_LET      = 'LET'       # ކަނޑައަޅާ / ބަހައްޓާ
TT_FUNCTION = 'FUNCTION'  # ވަޒީފާ / ފަންކް
TT_RETURN   = 'RETURN'    # ފޮނުވާ
TT_PRINT    = 'PRINT'     # ދައްކާ / ލިޔޭ
TT_IF       = 'IF'        # ނަމަ
TT_ELSE     = 'ELSE'      # ނޫންނަމަ
TT_WHILE    = 'WHILE'     # ހިނދު
TT_END      = 'END'       # ނިމުނީ
TT_TRUE     = 'TRUE'      # އާން
TT_FALSE    = 'FALSE'     # ނޫން
TT_AND      = 'AND'       # އަދި
TT_OR       = 'OR'        # ނުވަތަ

# Advanced Keywords
TT_FOR      = 'FOR'       # ކޮންމެ
TT_IN       = 'IN'        # ތެރޭގައި
TT_IMPORT   = 'IMPORT'    # ގެނޭ
TT_TRY      = 'TRY'       # މަސައްކަތްކުރޭ
TT_CATCH    = 'CATCH'     # ކުށެއް_ފެނިއްޖެނަމަ
TT_THROW    = 'THROW'     # އުކާލާ