#include "Lexer.h"
#include "Parser.h"
#include "Codegen.h"
#include <iostream>
#include <string>

extern FILE* SourceFile;

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: dhic <source file> [-o <output.o>] [--emit-ir]\n";
        return 1;
    }

    std::string SourcePath = argv[1];
    std::string OutFile = "output.o";
    bool emitIR = false;

    for (int i = 2; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--emit-ir") {
            emitIR = true;
        } else if (arg == "-o" && i + 1 < argc) {
            OutFile = argv[++i];
        }
    }

    SourceFile = fopen(SourcePath.c_str(), "r");
    if (!SourceFile) {
        std::cerr << "Could not open file: " << SourcePath << "\n";
        return 1;
    }

    std::cout << "Compiling " << SourcePath << "...\n";

    InitializeModule();

    Parser parser;
    auto ast = parser.ParseProgram();

    bool hasError = false;
    for (auto& fn : ast) {
        if (!fn->codegen()) {
            std::cerr << "Error generating IR for function: " << fn->getName() << "\n";
            hasError = true;
        }
    }

    if (!hasError) {
        if (emitIR) {
            std::cout << "\n--- LLVM IR Output ---\n";
            DumpLLVMIR();
            std::cout << "-----------------------\n";
        }
        CompileToObjectFile(OutFile);
        std::cout << "Compilation complete: " << OutFile << "\n";
    }

    fclose(SourceFile);
    return hasError ? 1 : 0;
}
