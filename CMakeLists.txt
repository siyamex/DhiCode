cmake_minimum_required(VERSION 3.10)
project(Dhicode)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find LLVM package
find_package(LLVM REQUIRED CONFIG)
message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")

include_directories(${LLVM_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})

# Setup building the compiler itself
add_executable(dhic
    main.cpp
    Lexer.cpp
    Parser.cpp
    Codegen.cpp
    runtime.cpp
)

# Link against the necessary LLVM libraries for code generation and parsing
llvm_map_components_to_libnames(llvm_libs core native nativecodegen irreader support target)

target_link_libraries(dhic PRIVATE ${llvm_libs})
