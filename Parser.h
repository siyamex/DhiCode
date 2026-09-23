#ifndef PARSER_H
#define PARSER_H

#include "AST.h"
#include <memory>
#include <vector>

class Parser {
    int CurTok;
    int getNextToken();
    int getTokPrecedence();

    std::unique_ptr<ExprAST> ParseNumberExpr();
    std::unique_ptr<ExprAST> ParseStringExpr();
    std::unique_ptr<ExprAST> ParseBoolExpr();
    std::unique_ptr<ExprAST> ParseIdentifierOrCallExpr();
    std::unique_ptr<ExprAST> ParseParenExpr();
    std::unique_ptr<ExprAST> ParsePrimary();
    std::unique_ptr<ExprAST> ParseBinOpRHS(int ExprPrec, std::unique_ptr<ExprAST> LHS);
    std::unique_ptr<ExprAST> ParseExpression();

    std::unique_ptr<VariableDeclAST> ParseVariableDecl();
    std::unique_ptr<WriteStmtAST> ParseWriteStmt();
    std::unique_ptr<ReturnStmtAST> ParseReturnStmt();
    std::unique_ptr<IfStmtAST> ParseIfStmt();
    std::unique_ptr<WhileStmtAST> ParseWhileStmt();
    std::unique_ptr<ASTNode> ParseStatement();
    std::unique_ptr<BlockAST> ParseBlock(bool stopOnElse = false);
    std::unique_ptr<FunctionAST> ParseFunction();

public:
    Parser();
    std::vector<std::unique_ptr<FunctionAST>> ParseProgram();
};

#endif
