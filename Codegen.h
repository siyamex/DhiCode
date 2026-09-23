#ifndef CODEGEN_H
#define CODEGEN_H

#include <string>

void InitializeModule();
void DumpLLVMIR();
void CompileToObjectFile(const std::string& Filename);

#endif
