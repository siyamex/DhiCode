#include "Lexer.h"
#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <iostream>

std::string IdentifierStr;
std::string StringVal;
double NumVal;
FILE* SourceFile = nullptr;

static int nextChar() {
    return SourceFile ? fgetc(SourceFile) : getchar();
}

static bool isIdentifierStart(int c) {
    return isalpha(c) || c == '_' || (c & 0x80) != 0;
}

static bool isIdentifierPart(int c) {
    return isalnum(c) || c == '_' || (c & 0x80) != 0;
}

int gettok() {
    static int LastChar = ' ';

    while (1) {
        // Skip whitespace
        while (isspace(LastChar)) {
            LastChar = nextChar();
        }

        // Handle Comments
        if (LastChar == '/') {
            int peek = nextChar();
            if (peek == '/') {
                // Single line comment
                while (LastChar != EOF && LastChar != '\n') {
                    LastChar = nextChar();
                }
                continue;
            } else if (peek == '*') {
                // Block comment
                LastChar = nextChar();
                while (LastChar != EOF) {
                    if (LastChar == '*') {
                        int nextP = nextChar();
                        if (nextP == '/') {
                            LastChar = nextChar();
                            break;
                        }
                        LastChar = nextP;
                    } else {
                        LastChar = nextChar();
                    }
                }
                continue;
            } else {
                // Not a comment, it's division operator '/'
                int ret = LastChar;
                LastChar = peek;
                return ret;
            }
        }
        break;
    }

    // String literals
    if (LastChar == '"') {
        StringVal.clear();
        LastChar = nextChar();
        while (LastChar != EOF && LastChar != '"') {
            if (LastChar == '\\') {
                LastChar = nextChar();
                if (LastChar == 'n') StringVal += '\n';
                else if (LastChar == 't') StringVal += '\t';
                else if (LastChar == '"') StringVal += '"';
                else if (LastChar == '\\') StringVal += '\\';
                else if (LastChar != EOF) StringVal += (char)LastChar;
            } else {
                StringVal += (char)LastChar;
            }
            LastChar = nextChar();
        }
        if (LastChar == '"') {
            LastChar = nextChar(); // consume closing quote
        }
        return tok_string;
    }

    // Identifiers or Keywords (Including UTF-8 Thaana letters)
    if (isIdentifierStart(LastChar) && !isdigit(LastChar)) {
        IdentifierStr = (char)LastChar;
        while (1) {
            LastChar = nextChar();
            if (isIdentifierPart(LastChar)) {
                IdentifierStr += (char)LastChar;
            } else {
                break;
            }
        }

        // Keywords
        if (IdentifierStr == "ވަޒީފާ" || IdentifierStr == "ފަންކް") return tok_func;
        if (IdentifierStr == "ކަނޑައަޅާ" || IdentifierStr == "ބަހައްޓާ") return tok_declare;
        if (IdentifierStr == "ދައްކާ" || IdentifierStr == "ލިޔޭ") return tok_write;
        if (IdentifierStr == "ނަމަ") return tok_if;
        if (IdentifierStr == "ނޫންނަމަ") return tok_else;
        if (IdentifierStr == "ހިނދު") return tok_while;
        if (IdentifierStr == "ނިމުނީ") return tok_end;
        if (IdentifierStr == "ފޮނުވާ") return tok_return;
        if (IdentifierStr == "އާން") return tok_true;
        if (IdentifierStr == "ނޫން") return tok_false;
        if (IdentifierStr == "އަދި") return tok_and;
        if (IdentifierStr == "ނުވަތަ") return tok_or;
        if (IdentifierStr == "މައި") return tok_main;

        return tok_identifier;
    }

    // Numbers (Floating point & Integer)
    if (isdigit(LastChar)) {
        std::string NumStr;
        do {
            NumStr += (char)LastChar;
            LastChar = nextChar();
        } while (isdigit(LastChar) || LastChar == '.');

        NumVal = strtod(NumStr.c_str(), nullptr);
        return tok_number;
    }

    // Multi-character operators
    if (LastChar == '=') {
        LastChar = nextChar();
        if (LastChar == '=') {
            LastChar = nextChar();
            return tok_eq;
        }
        return '=';
    }
    if (LastChar == '!') {
        LastChar = nextChar();
        if (LastChar == '=') {
            LastChar = nextChar();
            return tok_ne;
        }
        return '!';
    }
    if (LastChar == '<') {
        LastChar = nextChar();
        if (LastChar == '=') {
            LastChar = nextChar();
            return tok_le;
        }
        return '<';
    }
    if (LastChar == '>') {
        LastChar = nextChar();
        if (LastChar == '=') {
            LastChar = nextChar();
            return tok_ge;
        }
        return '>';
    }

    // End of file
    if (LastChar == EOF)
        return tok_eof;

    // Single character tokens
    int ThisChar = LastChar;
    LastChar = nextChar();
    return ThisChar;
}
