#include "Parser.h"
#include "Lexer.h"
#include <iostream>

Parser::Parser() {
    getNextToken(); // Load the first token
}

int Parser::getNextToken() {
    return CurTok = gettok();
}

int Parser::getTokPrecedence() {
    switch (CurTok) {
        case tok_or:
        case tok_and:
            return 10;
        case tok_eq:
        case tok_ne:
            return 20;
        case '<':
        case '>':
        case tok_le:
        case tok_ge:
            return 30;
        case '+':
        case '-':
            return 40;
        case '*':
        case '/':
        case '%':
            return 50;
        default:
            return -1;
    }
}

std::unique_ptr<ExprAST> Parser::ParseNumberExpr() {
    auto Result = std::make_unique<NumberExprAST>(NumVal);
    getNextToken(); // consume the number
    return std::move(Result);
}

std::unique_ptr<ExprAST> Parser::ParseStringExpr() {
    auto Result = std::make_unique<StringExprAST>(StringVal);
    getNextToken(); // consume the string
    return std::move(Result);
}

std::unique_ptr<ExprAST> Parser::ParseBoolExpr() {
    auto Result = std::make_unique<BoolExprAST>(CurTok == tok_true);
    getNextToken(); // consume boolean
    return std::move(Result);
}

std::unique_ptr<ExprAST> Parser::ParseIdentifierOrCallExpr() {
    std::string IdName = (CurTok == tok_main) ? "main" : IdentifierStr;
    getNextToken(); // consume identifier

    // If followed by '(', it's a function call
    if (CurTok == '(') {
        getNextToken(); // consume '('
        std::vector<std::unique_ptr<ExprAST>> Args;
        if (CurTok != ')') {
            while (1) {
                if (auto Arg = ParseExpression()) {
                    Args.push_back(std::move(Arg));
                } else {
                    return nullptr;
                }

                if (CurTok == ')') break;

                if (CurTok != ',') {
                    std::cerr << "Expected ')' or ',' in argument list\n";
                    return nullptr;
                }
                getNextToken(); // consume ','
            }
        }
        getNextToken(); // consume ')'
        return std::make_unique<CallExprAST>(IdName, std::move(Args));
    }

    return std::make_unique<VariableExprAST>(IdName);
}

std::unique_ptr<ExprAST> Parser::ParseParenExpr() {
    getNextToken(); // consume '('
    auto V = ParseExpression();
    if (!V) return nullptr;

    if (CurTok != ')') {
        std::cerr << "Expected ')'\n";
        return nullptr;
    }
    getNextToken(); // consume ')'
    return V;
}

std::unique_ptr<ExprAST> Parser::ParsePrimary() {
    switch (CurTok) {
        case tok_number:
            return ParseNumberExpr();
        case tok_string:
            return ParseStringExpr();
        case tok_true:
        case tok_false:
            return ParseBoolExpr();
        case tok_identifier:
        case tok_main:
            return ParseIdentifierOrCallExpr();
        case '(':
            return ParseParenExpr();
        default:
            std::cerr << "Expected expression, unexpected token: " << CurTok << "\n";
            return nullptr;
    }
}

std::unique_ptr<ExprAST> Parser::ParseBinOpRHS(int ExprPrec, std::unique_ptr<ExprAST> LHS) {
    while (1) {
        int TokPrec = getTokPrecedence();

        // If this operator binds less tightly with RHS than the current operator, we're done
        if (TokPrec < ExprPrec)
            return LHS;

        int BinOp = CurTok;
        getNextToken(); // consume binop

        auto RHS = ParsePrimary();
        if (!RHS) return nullptr;

        int NextPrec = getTokPrecedence();
        if (TokPrec < NextPrec) {
            RHS = ParseBinOpRHS(TokPrec + 1, std::move(RHS));
            if (!RHS) return nullptr;
        }

        LHS = std::make_unique<BinaryExprAST>(BinOp, std::move(LHS), std::move(RHS));
    }
}

std::unique_ptr<ExprAST> Parser::ParseExpression() {
    auto LHS = ParsePrimary();
    if (!LHS) return nullptr;
    return ParseBinOpRHS(0, std::move(LHS));
}

std::unique_ptr<VariableDeclAST> Parser::ParseVariableDecl() {
    getNextToken(); // consume 'ކަނޑައަޅާ' or 'ބަހައްޓާ'

    if (CurTok != tok_identifier) {
        std::cerr << "Expected identifier after variable declaration keyword\n";
        return nullptr;
    }
    std::string VarName = IdentifierStr;
    getNextToken(); // consume identifier

    if (CurTok == '=') {
        getNextToken(); // consume '='
    }

    auto InitExpr = ParseExpression();
    if (CurTok == ';') getNextToken(); // optional semicolon
    return std::make_unique<VariableDeclAST>(VarName, std::move(InitExpr));
}

std::unique_ptr<WriteStmtAST> Parser::ParseWriteStmt() {
    getNextToken(); // consume 'ދައްކާ' or 'ލިޔޭ'
    auto Expr = ParseExpression();
    if (CurTok == ';') getNextToken(); // optional semicolon
    return std::make_unique<WriteStmtAST>(std::move(Expr));
}

std::unique_ptr<ReturnStmtAST> Parser::ParseReturnStmt() {
    getNextToken(); // consume 'ފޮނުވާ'
    std::unique_ptr<ExprAST> Val = nullptr;
    if (CurTok != ';' && CurTok != tok_end && CurTok != '}' && CurTok != tok_eof) {
        Val = ParseExpression();
    }
    if (CurTok == ';') getNextToken();
    return std::make_unique<ReturnStmtAST>(std::move(Val));
}

std::unique_ptr<IfStmtAST> Parser::ParseIfStmt() {
    getNextToken(); // consume 'ނަމަ'

    bool hasParen = (CurTok == '(');
    if (hasParen) getNextToken();

    auto Cond = ParseExpression();
    if (!Cond) return nullptr;

    if (hasParen) {
        if (CurTok == ')') getNextToken();
    }

    auto Then = ParseBlock(true); // stop on 'ނޫންނަމަ' if keyword block
    std::unique_ptr<BlockAST> Else = nullptr;

    if (CurTok == tok_else) {
        getNextToken(); // consume 'ނޫންނަމަ'
        Else = ParseBlock(false);
    }

    if (CurTok == tok_end) {
        getNextToken(); // consume 'ނިމުނީ'
    }

    return std::make_unique<IfStmtAST>(std::move(Cond), std::move(Then), std::move(Else));
}

std::unique_ptr<WhileStmtAST> Parser::ParseWhileStmt() {
    getNextToken(); // consume 'ހިނދު'

    bool hasParen = (CurTok == '(');
    if (hasParen) getNextToken();

    auto Cond = ParseExpression();
    if (!Cond) return nullptr;

    if (hasParen) {
        if (CurTok == ')') getNextToken();
    }

    auto Body = ParseBlock(false);

    if (CurTok == tok_end) {
        getNextToken(); // consume 'ނިމުނީ'
    }

    return std::make_unique<WhileStmtAST>(std::move(Cond), std::move(Body));
}

std::unique_ptr<ASTNode> Parser::ParseStatement() {
    switch (CurTok) {
        case tok_declare:
            return ParseVariableDecl();
        case tok_write:
            return ParseWriteStmt();
        case tok_return:
            return ParseReturnStmt();
        case tok_if:
            return ParseIfStmt();
        case tok_while:
            return ParseWhileStmt();
        case '{':
            return ParseBlock(false);
        case ';':
            getNextToken();
            return nullptr;
        default:
            return ParseExpression();
    }
}

std::unique_ptr<BlockAST> Parser::ParseBlock(bool stopOnElse) {
    std::vector<std::unique_ptr<ASTNode>> Statements;

    // Braced block style: { ... }
    if (CurTok == '{') {
        getNextToken(); // consume '{'
        while (CurTok != '}' && CurTok != tok_eof) {
            if (auto Stmt = ParseStatement()) {
                Statements.push_back(std::move(Stmt));
            } else {
                getNextToken();
            }
        }
        if (CurTok == '}') getNextToken(); // consume '}'
        return std::make_unique<BlockAST>(std::move(Statements));
    }

    // Keyword-delimited block style: until 'ނިމުނީ' or 'ނޫންނަމަ'
    while (CurTok != tok_end && CurTok != tok_eof) {
        if (stopOnElse && CurTok == tok_else) {
            break;
        }
        if (auto Stmt = ParseStatement()) {
            Statements.push_back(std::move(Stmt));
        } else {
            getNextToken();
        }
    }

    return std::make_unique<BlockAST>(std::move(Statements));
}

std::unique_ptr<FunctionAST> Parser::ParseFunction() {
    getNextToken(); // consume 'ވަޒީފާ' or 'ފަންކް'

    std::string FnName;
    if (CurTok == tok_identifier || CurTok == tok_main) {
        FnName = (CurTok == tok_main) ? "main" : IdentifierStr;
    } else {
        std::cerr << "Expected function name\n";
        return nullptr;
    }
    getNextToken(); // consume name

    if (CurTok != '(') {
        std::cerr << "Expected '(' in function declaration\n";
        return nullptr;
    }
    getNextToken(); // consume '('

    std::vector<std::string> Args;
    while (CurTok == tok_identifier) {
        Args.push_back(IdentifierStr);
        getNextToken();
        if (CurTok == ',') {
            getNextToken();
        }
    }

    if (CurTok != ')') {
        std::cerr << "Expected ')' in function declaration\n";
        return nullptr;
    }
    getNextToken(); // consume ')'

    auto Body = ParseBlock(false);
    if (!Body) return nullptr;

    if (CurTok == tok_end) {
        getNextToken(); // consume 'ނިމުނީ'
    }

    return std::make_unique<FunctionAST>(FnName, std::move(Args), std::move(Body));
}

std::vector<std::unique_ptr<FunctionAST>> Parser::ParseProgram() {
    std::vector<std::unique_ptr<FunctionAST>> Functions;
    std::vector<std::unique_ptr<ASTNode>> TopLevelStatements;

    while (CurTok != tok_eof) {
        if (CurTok == tok_func) {
            if (auto Fn = ParseFunction()) {
                Functions.push_back(std::move(Fn));
            } else {
                getNextToken();
            }
        } else {
            if (auto Stmt = ParseStatement()) {
                TopLevelStatements.push_back(std::move(Stmt));
            } else {
                getNextToken();
            }
        }
    }

    // If top-level statements were present, wrap them in synthetic 'main' entrypoint
    if (!TopLevelStatements.empty()) {
        auto MainBody = std::make_unique<BlockAST>(std::move(TopLevelStatements));
        Functions.push_back(std::make_unique<FunctionAST>("main", std::vector<std::string>{}, std::move(MainBody)));
    }

    return Functions;
}
