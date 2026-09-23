#ifndef AST_H
#define AST_H

#include <string>
#include <memory>
#include <vector>

namespace llvm {
    class Value;
}

// Base AST Node
class ASTNode {
public:
    virtual ~ASTNode() = default;
    virtual llvm::Value* codegen() = 0;
};

// Expression Base Node
class ExprAST : public ASTNode {
public:
    virtual ~ExprAST() = default;
};

// Number Literal Expression
class NumberExprAST : public ExprAST {
    double Val;
public:
    NumberExprAST(double Val) : Val(Val) {}
    double getValue() const { return Val; }
    llvm::Value* codegen() override;
};

// String Literal Expression
class StringExprAST : public ExprAST {
    std::string Val;
public:
    StringExprAST(const std::string& Val) : Val(Val) {}
    const std::string& getValue() const { return Val; }
    llvm::Value* codegen() override;
};

// Boolean Literal Expression
class BoolExprAST : public ExprAST {
    bool Val;
public:
    BoolExprAST(bool Val) : Val(Val) {}
    bool getValue() const { return Val; }
    llvm::Value* codegen() override;
};

// Variable Reference Expression
class VariableExprAST : public ExprAST {
    std::string Name;
public:
    VariableExprAST(const std::string& Name) : Name(Name) {}
    const std::string& getName() const { return Name; }
    llvm::Value* codegen() override;
};

// Binary Operator Expression (+, -, *, /, <, >, ==, etc.)
class BinaryExprAST : public ExprAST {
    int Op;
    std::unique_ptr<ExprAST> LHS, RHS;
public:
    BinaryExprAST(int Op, std::unique_ptr<ExprAST> LHS, std::unique_ptr<ExprAST> RHS)
        : Op(Op), LHS(std::move(LHS)), RHS(std::move(RHS)) {}
    int getOp() const { return Op; }
    ExprAST* getLHS() const { return LHS.get(); }
    ExprAST* getRHS() const { return RHS.get(); }
    llvm::Value* codegen() override;
};

// Function Call Expression
class CallExprAST : public ExprAST {
    std::string Callee;
    std::vector<std::unique_ptr<ExprAST>> Args;
public:
    CallExprAST(const std::string& Callee, std::vector<std::unique_ptr<ExprAST>> Args)
        : Callee(Callee), Args(std::move(Args)) {}
    const std::string& getCallee() const { return Callee; }
    const std::vector<std::unique_ptr<ExprAST>>& getArgs() const { return Args; }
    llvm::Value* codegen() override;
};

// Variable Declaration / Assignment Statement (ކަނޑައަޅާ / ބަހައްޓާ)
class VariableDeclAST : public ASTNode {
    std::string Name;
    std::unique_ptr<ExprAST> Init;
public:
    VariableDeclAST(const std::string& Name, std::unique_ptr<ExprAST> Init)
        : Name(Name), Init(std::move(Init)) {}
    const std::string& getName() const { return Name; }
    ExprAST* getInit() const { return Init.get(); }
    llvm::Value* codegen() override;
};

// Write / Print Statement (ދައްކާ / ލިޔޭ)
class WriteStmtAST : public ASTNode {
    std::unique_ptr<ExprAST> Expr;
public:
    WriteStmtAST(std::unique_ptr<ExprAST> Expr) : Expr(std::move(Expr)) {}
    ExprAST* getExpr() const { return Expr.get(); }
    llvm::Value* codegen() override;
};

// Return Statement (ފޮނުވާ)
class ReturnStmtAST : public ASTNode {
    std::unique_ptr<ExprAST> Val;
public:
    ReturnStmtAST(std::unique_ptr<ExprAST> Val) : Val(std::move(Val)) {}
    ExprAST* getVal() const { return Val.get(); }
    llvm::Value* codegen() override;
};

// Block of Statements
class BlockAST : public ASTNode {
    std::vector<std::unique_ptr<ASTNode>> Statements;
public:
    BlockAST(std::vector<std::unique_ptr<ASTNode>> Statements)
        : Statements(std::move(Statements)) {}
    const std::vector<std::unique_ptr<ASTNode>>& getStatements() const { return Statements; }
    llvm::Value* codegen() override;
};

// If-Else Conditional Statement (ނަމަ ... ނޫންނަމަ ... ނިމުނީ)
class IfStmtAST : public ASTNode {
    std::unique_ptr<ExprAST> Cond;
    std::unique_ptr<BlockAST> Then;
    std::unique_ptr<BlockAST> Else;
public:
    IfStmtAST(std::unique_ptr<ExprAST> Cond, std::unique_ptr<BlockAST> Then, std::unique_ptr<BlockAST> Else = nullptr)
        : Cond(std::move(Cond)), Then(std::move(Then)), Else(std::move(Else)) {}
    ExprAST* getCond() const { return Cond.get(); }
    BlockAST* getThen() const { return Then.get(); }
    BlockAST* getElse() const { return Else.get(); }
    llvm::Value* codegen() override;
};

// While Loop Statement (ހިނދު ... ނިމުނީ)
class WhileStmtAST : public ASTNode {
    std::unique_ptr<ExprAST> Cond;
    std::unique_ptr<BlockAST> Body;
public:
    WhileStmtAST(std::unique_ptr<ExprAST> Cond, std::unique_ptr<BlockAST> Body)
        : Cond(std::move(Cond)), Body(std::move(Body)) {}
    ExprAST* getCond() const { return Cond.get(); }
    BlockAST* getBody() const { return Body.get(); }
    llvm::Value* codegen() override;
};

// Function Statement (ވަޒީފާ / ފަންކް)
class FunctionAST : public ASTNode {
    std::string Name;
    std::vector<std::string> Args;
    std::unique_ptr<BlockAST> Body;
public:
    FunctionAST(const std::string& Name, std::vector<std::string> Args, std::unique_ptr<BlockAST> Body)
        : Name(Name), Args(std::move(Args)), Body(std::move(Body)) {}
    const std::string& getName() const { return Name; }
    const std::vector<std::string>& getArgs() const { return Args; }
    BlockAST* getBody() const { return Body.get(); }
    llvm::Value* codegen() override;
};

#endif
