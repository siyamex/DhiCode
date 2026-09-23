#ifndef LEXER_H
#define LEXER_H

#include <string>
#include <cstdio>

// Tokens
enum Token {
    tok_eof = -1,
    tok_func = -2,        // ވަޒީފާ / ފަންކް
    tok_identifier = -3,
    tok_number = -4,
    tok_declare = -5,     // ކަނޑައަޅާ / ބަހައްޓާ
    tok_write = -6,       // ދައްކާ / ލިޔޭ
    tok_if = -7,          // ނަމަ
    tok_main = -8,        // މައި
    tok_else = -9,        // ނޫންނަމަ
    tok_while = -10,      // ހިނދު
    tok_end = -11,        // ނިމުނީ
    tok_return = -12,     // ފޮނުވާ
    tok_true = -13,       // އާން
    tok_false = -14,      // ނޫން
    tok_and = -15,        // އަދި
    tok_or = -16,         // ނުވަތަ
    tok_string = -17,     // "..."
    tok_eq = -18,         // ==
    tok_ne = -19,         // !=
    tok_le = -20,         // <=
    tok_ge = -21          // >=
};

extern std::string IdentifierStr; // Filled in if tok_identifier
extern std::string StringVal;     // Filled in if tok_string
extern double NumVal;             // Filled in if tok_number

extern FILE* SourceFile;          // Input file pointer

int gettok();

#endif
