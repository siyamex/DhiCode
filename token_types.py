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
TT_EXPONENT = '**'
TT_BANG     = '!'
TT_EQ       = '=='
TT_NOT_EQ   = '!='
TT_LT       = '<'
TT_GT       = '>'
TT_LTE      = '<='
TT_GTE      = '>='
TT_NULL_COALESCE = '??'

# Compound Assignment Operators
TT_PLUS_ASSIGN     = '+='
TT_MINUS_ASSIGN    = '-='
TT_ASTERISK_ASSIGN = '*='
TT_SLASH_ASSIGN    = '/='
TT_MODULO_ASSIGN   = '%='

# Bitwise Operators
TT_BIT_AND = '&'
TT_BIT_OR  = '|'
TT_BIT_XOR = '^'
TT_BIT_NOT = '~'
TT_BIT_SHL = '<<'
TT_BIT_SHR = '>>'

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
TT_LET      = 'LET'       # ކަނޑައަޅާ / ބަހައްޓާ / let / var
TT_CONST    = 'CONST'     # ދާއިމީ / const
TT_FUNCTION = 'FUNCTION'  # ވަޒީފާ / ފަންކް / fn / function
TT_RETURN   = 'RETURN'    # ފޮނުވާ / return
TT_PRINT    = 'PRINT'     # ދައްކާ / ލިޔޭ / print
TT_IF       = 'IF'        # ނަމަ / if
TT_ELSE     = 'ELSE'      # ނޫންނަމަ / else
TT_WHILE    = 'WHILE'     # ހިނދު / while
TT_END      = 'END'       # ނިމުނީ / end
TT_TRUE     = 'TRUE'      # އާން / true
TT_FALSE    = 'FALSE'     # ނޫން / false
TT_NULL     = 'NULL'      # ހުސް / ބާޠިލް / null / nil
TT_AND      = 'AND'       # އަދި / and / &&
TT_OR       = 'OR'        # ނުވަތަ / or / ||

# Advanced Keywords
TT_FOR      = 'FOR'       # ކޮންމެ / for
TT_IN       = 'IN'        # ތެރޭގައި / in
TT_IMPORT   = 'IMPORT'    # ގެނޭ / import
TT_TRY      = 'TRY'       # މަސައްކަތްކުރޭ / try
TT_CATCH    = 'CATCH'     # ކުށެއް_ފެނިއްޖެނަމަ / catch
TT_THROW    = 'THROW'     # އުކާލާ / throw