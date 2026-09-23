#include "AST.h"
#include "Lexer.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Verifier.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/Host.h"
#include "llvm/Support/TargetRegistry.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Target/TargetMachine.h"
#include "llvm/Target/TargetOptions.h"
#include "llvm/IR/LegacyPassManager.h"
#include <map>
#include <iostream>

// LLVM Global State Context
static llvm::LLVMContext TheContext;
static llvm::IRBuilder<> Builder(TheContext);
static std::unique_ptr<llvm::Module> TheModule;
static std::map<std::string, llvm::AllocaInst*> NamedValues;

// Helper to create alloca instructions in entry block
static llvm::AllocaInst *CreateEntryBlockAlloca(llvm::Function *TheFunction, const std::string &VarName, llvm::Type* type) {
    llvm::IRBuilder<> TmpB(&TheFunction->getEntryBlock(), TheFunction->getEntryBlock().begin());
    return TmpB.CreateAlloca(type, nullptr, VarName);
}

// 1. Number Literal
llvm::Value* NumberExprAST::codegen() {
    return llvm::ConstantFP::get(TheContext, llvm::APFloat(Val));
}

// 2. String Literal
llvm::Value* StringExprAST::codegen() {
    return Builder.CreateGlobalStringPtr(Val, "str_literal");
}

// 3. Boolean Literal
llvm::Value* BoolExprAST::codegen() {
    return llvm::ConstantInt::get(llvm::Type::getInt1Ty(TheContext), Val ? 1 : 0);
}

// 4. Variable Access
llvm::Value* VariableExprAST::codegen() {
    llvm::AllocaInst *Alloca = NamedValues[Name];
    if (!Alloca) {
        std::cerr << "Unknown variable referenced: " << Name << "\n";
        return nullptr;
    }
    return Builder.CreateLoad(Alloca->getAllocatedType(), Alloca, Name.c_str());
}

// 5. Variable Declaration
llvm::Value* VariableDeclAST::codegen() {
    llvm::Function *TheFunction = Builder.GetInsertBlock()->getParent();
    
    llvm::Value *InitVal = Init ? Init->codegen() : nullptr;
    if (!InitVal) {
        InitVal = llvm::ConstantFP::get(TheContext, llvm::APFloat(0.0));
    }

    llvm::AllocaInst *Alloca = CreateEntryBlockAlloca(TheFunction, Name, InitVal->getType());
    Builder.CreateStore(InitVal, Alloca);
    
    NamedValues[Name] = Alloca;
    return InitVal;
}

// 6. Binary Operators
llvm::Value* BinaryExprAST::codegen() {
    llvm::Value *L = LHS->codegen();
    llvm::Value *R = RHS->codegen();
    if (!L || !R) return nullptr;

    // Check if either side is a string pointer (for concatenation)
    if (L->getType()->isPointerTy() || R->getType()->isPointerTy()) {
        if (Op == '+') {
            llvm::FunctionType *ConcatType = llvm::FunctionType::get(
                llvm::Type::getInt8PtrTy(TheContext),
                {llvm::Type::getInt8PtrTy(TheContext), llvm::Type::getInt8PtrTy(TheContext)},
                false
            );
            llvm::FunctionCallee ConcatFunc = TheModule->getOrInsertFunction("dhicode_concat_str", ConcatType);
            return Builder.CreateCall(ConcatFunc, {L, R}, "concat_tmp");
        }
    }

    // Convert integer/boolean to double if operating with float
    if (L->getType()->isIntegerTy() && R->getType()->isFloatingPointTy()) {
        L = Builder.CreateSIToFP(L, llvm::Type::getDoubleTy(TheContext), "castL");
    } else if (L->getType()->isFloatingPointTy() && R->getType()->isIntegerTy()) {
        R = Builder.CreateSIToFP(R, llvm::Type::getDoubleTy(TheContext), "castR");
    }

    // Floating point operations
    if (L->getType()->isFloatingPointTy() && R->getType()->isFloatingPointTy()) {
        switch (Op) {
            case '+': return Builder.CreateFAdd(L, R, "addtmp");
            case '-': return Builder.CreateFSub(L, R, "subtmp");
            case '*': return Builder.CreateFMul(L, R, "multmp");
            case '/': return Builder.CreateFDiv(L, R, "divtmp");
            case '<': return Builder.CreateFCmpULT(L, R, "cmptmp");
            case '>': return Builder.CreateFCmpUGT(L, R, "cmptmp");
            case tok_le: return Builder.CreateFCmpULE(L, R, "cmptmp");
            case tok_ge: return Builder.CreateFCmpUGE(L, R, "cmptmp");
            case tok_eq:
            case '=': return Builder.CreateFCmpUEQ(L, R, "cmptmp");
            case tok_ne: return Builder.CreateFCmpUNE(L, R, "cmptmp");
            default: break;
        }
    }

    // Boolean logical operations
    if (Op == tok_and) {
        return Builder.CreateAnd(L, R, "andtmp");
    }
    if (Op == tok_or) {
        return Builder.CreateOr(L, R, "ortmp");
    }

    std::cerr << "Invalid binary operator: " << Op << "\n";
    return nullptr;
}

// 7. Function Call
llvm::Value* CallExprAST::codegen() {
    llvm::Function *CalleeF = TheModule->getFunction(Callee);
    if (!CalleeF) {
        std::cerr << "Unknown function referenced: " << Callee << "\n";
        return nullptr;
    }

    if (CalleeF->arg_size() != Args.size()) {
        std::cerr << "Incorrect number of arguments passed to function " << Callee << "\n";
        return nullptr;
    }

    std::vector<llvm::Value*> ArgsV;
    for (auto &arg : Args) {
        llvm::Value *ArgVal = arg->codegen();
        if (!ArgVal) return nullptr;
        ArgsV.push_back(ArgVal);
    }

    return Builder.CreateCall(CalleeF, ArgsV, "calltmp");
}

// 8. Write Statement
llvm::Value* WriteStmtAST::codegen() {
    llvm::Value *ExprVal = Expr->codegen();
    if (!ExprVal) return nullptr;

    if (ExprVal->getType()->isPointerTy()) {
        llvm::FunctionType *PrintType = llvm::FunctionType::get(
            llvm::Type::getVoidTy(TheContext),
            {llvm::Type::getInt8PtrTy(TheContext)},
            false
        );
        llvm::FunctionCallee PrintFunc = TheModule->getOrInsertFunction("dhicode_print_str", PrintType);
        return Builder.CreateCall(PrintFunc, {ExprVal});
    } else if (ExprVal->getType()->isIntegerTy()) {
        llvm::FunctionType *PrintType = llvm::FunctionType::get(
            llvm::Type::getVoidTy(TheContext),
            {llvm::Type::getInt32Ty(TheContext)},
            false
        );
        llvm::FunctionCallee PrintFunc = TheModule->getOrInsertFunction("dhicode_print_bool", PrintType);
        llvm::Value *Int32Val = Builder.CreateZExtOrTrunc(ExprVal, llvm::Type::getInt32Ty(TheContext));
        return Builder.CreateCall(PrintFunc, {Int32Val});
    } else {
        llvm::FunctionType *PrintType = llvm::FunctionType::get(
            llvm::Type::getVoidTy(TheContext),
            {llvm::Type::getDoubleTy(TheContext)},
            false
        );
        llvm::FunctionCallee PrintFunc = TheModule->getOrInsertFunction("dhicode_print_num", PrintType);
        return Builder.CreateCall(PrintFunc, {ExprVal});
    }
}

// 9. Return Statement
llvm::Value* ReturnStmtAST::codegen() {
    if (Val) {
        llvm::Value *RetVal = Val->codegen();
        if (!RetVal) return nullptr;
        return Builder.CreateRet(RetVal);
    }
    return Builder.CreateRetVoid();
}

// 10. Block Statement
llvm::Value* BlockAST::codegen() {
    llvm::Value *LastVal = nullptr;
    for (auto &Stmt : Statements) {
        LastVal = Stmt->codegen();
        if (!LastVal) return nullptr;
    }
    return LastVal ? LastVal : llvm::ConstantInt::get(TheContext, llvm::APInt(32, 0));
}

// 11. If Statement
llvm::Value* IfStmtAST::codegen() {
    llvm::Value *CondV = Cond->codegen();
    if (!CondV) return nullptr;

    // Convert condition to bool (i1)
    if (CondV->getType()->isFloatingPointTy()) {
        CondV = Builder.CreateFCmpONE(CondV, llvm::ConstantFP::get(TheContext, llvm::APFloat(0.0)), "ifcond");
    } else if (CondV->getType()->isIntegerTy() && CondV->getType() != llvm::Type::getInt1Ty(TheContext)) {
        CondV = Builder.CreateICmpNE(CondV, llvm::ConstantInt::get(CondV->getType(), 0), "ifcond");
    }

    llvm::Function *TheFunction = Builder.GetInsertBlock()->getParent();

    llvm::BasicBlock *ThenBB = llvm::BasicBlock::Create(TheContext, "then", TheFunction);
    llvm::BasicBlock *ElseBB = Else ? llvm::BasicBlock::Create(TheContext, "else") : nullptr;
    llvm::BasicBlock *MergeBB = llvm::BasicBlock::Create(TheContext, "ifcont");

    if (Else) {
        Builder.CreateCondBr(CondV, ThenBB, ElseBB);
    } else {
        Builder.CreateCondBr(CondV, ThenBB, MergeBB);
    }

    // Emit ThenBB
    Builder.SetInsertPoint(ThenBB);
    if (!Then->codegen()) return nullptr;
    if (!Builder.GetInsertBlock()->getTerminator()) {
        Builder.CreateBr(MergeBB);
    }

    // Emit ElseBB if present
    if (Else) {
        TheFunction->insert(TheFunction->end(), ElseBB);
        Builder.SetInsertPoint(ElseBB);
        if (!Else->codegen()) return nullptr;
        if (!Builder.GetInsertBlock()->getTerminator()) {
            Builder.CreateBr(MergeBB);
        }
    }

    // Emit MergeBB
    TheFunction->insert(TheFunction->end(), MergeBB);
    Builder.SetInsertPoint(MergeBB);

    return llvm::ConstantInt::get(TheContext, llvm::APInt(32, 0));
}

// 12. While Loop Statement
llvm::Value* WhileStmtAST::codegen() {
    llvm::Function *TheFunction = Builder.GetInsertBlock()->getParent();

    llvm::BasicBlock *CondBB = llvm::BasicBlock::Create(TheContext, "whilecond", TheFunction);
    llvm::BasicBlock *LoopBB = llvm::BasicBlock::Create(TheContext, "whilebody", TheFunction);
    llvm::BasicBlock *AfterBB = llvm::BasicBlock::Create(TheContext, "whileafter", TheFunction);

    Builder.CreateBr(CondBB);

    // CondBB
    Builder.SetInsertPoint(CondBB);
    llvm::Value *CondV = Cond->codegen();
    if (!CondV) return nullptr;

    if (CondV->getType()->isFloatingPointTy()) {
        CondV = Builder.CreateFCmpONE(CondV, llvm::ConstantFP::get(TheContext, llvm::APFloat(0.0)), "whilecond");
    }

    Builder.CreateCondBr(CondV, LoopBB, AfterBB);

    // LoopBB
    Builder.SetInsertPoint(LoopBB);
    if (!Body->codegen()) return nullptr;
    if (!Builder.GetInsertBlock()->getTerminator()) {
        Builder.CreateBr(CondBB);
    }

    // AfterBB
    Builder.SetInsertPoint(AfterBB);

    return llvm::ConstantInt::get(TheContext, llvm::APInt(32, 0));
}

// 13. Function Statement
llvm::Value* FunctionAST::codegen() {
    bool isMain = (Name == "main");
    llvm::Type *RetTy = isMain ? llvm::Type::getInt32Ty(TheContext) : llvm::Type::getDoubleTy(TheContext);

    std::vector<llvm::Type*> ParamTypes(Args.size(), llvm::Type::getDoubleTy(TheContext));
    llvm::FunctionType *FT = llvm::FunctionType::get(RetTy, ParamTypes, false);
    llvm::Function *F = llvm::Function::Create(FT, llvm::Function::ExternalLinkage, Name, TheModule.get());

    // Set argument names
    unsigned Idx = 0;
    for (auto &Arg : F->args()) {
        Arg.setName(Args[Idx++]);
    }

    llvm::BasicBlock *BB = llvm::BasicBlock::Create(TheContext, "entry", F);
    Builder.SetInsertPoint(BB);

    NamedValues.clear();

    // Allocate arguments in entry block
    for (auto &Arg : F->args()) {
        llvm::AllocaInst *Alloca = CreateEntryBlockAlloca(F, std::string(Arg.getName()), Arg.getType());
        Builder.CreateStore(&Arg, Alloca);
        NamedValues[std::string(Arg.getName())] = Alloca;
    }

    if (Body->codegen() != nullptr) {
        if (!Builder.GetInsertBlock()->getTerminator()) {
            if (isMain) {
                Builder.CreateRet(llvm::ConstantInt::get(TheContext, llvm::APInt(32, 0)));
            } else {
                Builder.CreateRet(llvm::ConstantFP::get(TheContext, llvm::APFloat(0.0)));
            }
        }

        llvm::verifyFunction(*F);
        return F;
    }

    F->eraseFromParent();
    return nullptr;
}

// Module initialization
void InitializeModule() {
    TheModule = std::make_unique<llvm::Module>("Dhicode_Module", TheContext);
}

void DumpLLVMIR() {
    if (TheModule) {
        TheModule->print(llvm::errs(), nullptr);
    }
}

void CompileToObjectFile(const std::string& Filename) {
    auto TargetTriple = llvm::sys::getDefaultTargetTriple();

    llvm::InitializeAllTargetInfos();
    llvm::InitializeAllTargets();
    llvm::InitializeAllTargetMCs();
    llvm::InitializeAllAsmParsers();
    llvm::InitializeAllAsmPrinters();

    std::string Error;
    auto Target = llvm::TargetRegistry::lookupTarget(TargetTriple, Error);
    if (!Target) {
        llvm::errs() << Error;
        return;
    }

    auto CPU = "generic";
    auto Features = "";
    llvm::TargetOptions opt;
    auto TheTargetMachine = Target->createTargetMachine(
        TargetTriple, CPU, Features, opt, llvm::Reloc::PIC_);

    TheModule->setDataLayout(TheTargetMachine->createDataLayout());
    TheModule->setTargetTriple(TargetTriple);

    std::error_code EC;
    llvm::raw_fd_ostream dest(Filename, EC, llvm::sys::fs::OF_None);

    if (EC) {
        llvm::errs() << "Could not open file: " << EC.message();
        return;
    }

    llvm::legacy::PassManager pass;
    if (TheTargetMachine->addPassesToEmitFile(
            pass, dest, nullptr, llvm::CGFT_ObjectFile)) {
        llvm::errs() << "TheTargetMachine can't emit a file of this type";
        return;
    }

    pass.run(*TheModule);
    dest.flush();

    llvm::outs() << "Wrote " << Filename << "\n";
}
