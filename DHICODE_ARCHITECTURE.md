# DHicode Architecture & Comprehensive System Audit

**Document Version:** 1.0.0  
**Language Identity:** DHicode (ދިވެހި ކޯޑު) — Production-grade, general-purpose programming language designed around the Dhivehi language and Thaana script.

---

## 1. System Overview & Dual-Engine Topology

DHicode currently operates as a dual-engine architecture:
1. **Host-Independent Interpreter & Tooling Engine (Python 3 / Pyodide WebAssembly)**:
   - Zero-external-dependency, cross-platform tree-walk interpreter, CLI, REPL, standalone binary packager, code formatter, and Language Server Protocol (LSP) server.
   - Powers the interactive web playground and Dhivehi Coding Academy via Pyodide WebAssembly.
2. **Native Compilation Engine (C++17 & LLVM)**:
   - Ahead-Of-Time (AOT) compiler targeting native object code (`.o`, `.exe`) and LLVM Intermediate Representation (IR).

```
                      ┌─────────────────────────────────────┐
                      │        DHicode Source (.dhi)        │
                      └──────────────────┬──────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
      ┌─────────────────────────┐                 ┌─────────────────────────┐
      │   Python / Wasm Engine  │                 │   Native LLVM Engine    │
      ├─────────────────────────┤                 ├─────────────────────────┤
      │ Lexer (lexer.py)        │                 │ Lexer (Lexer.cpp)       │
      │ Parser (parser.py)      │                 │ Parser (Parser.cpp)     │
      │ AST (ast_nodes.py)      │                 │ AST (AST.h)             │
      │ Evaluator (evaluator.py)│                 │ Codegen (Codegen.cpp)   │
      │ StdLib (stdlib.py)      │                 │ Runtime (runtime.cpp)   │
      └────────────┬────────────┘                 └────────────┬────────────┘
                   │                                           │
         ┌─────────┴─────────┐                                 ▼
         ▼                   ▼                         Native Binaries
  CLI / REPL / Wasm    Standalone .pyz / .bat              (.o / .exe)
```

---

## 2. In-Depth Audit of the 32 Architectural Areas

### 2.1 Current Lexer
- **Python / Wasm Implementation (`lexer.py`, `web/lexer.py`)**:
  - Handles UTF-8 encoded text directly.
  - Recognizes the full Thaana Unicode block (`\u0780` through `\u07BF`: 24 basic letters, extended Arabic letters, 11 fili vowel marks, and sukun).
  - Supports identifier continuation with alphanumeric characters, Thaana characters, and underscores (`_`).
  - Supports integer and floating-point literals (`123`, `99.5`).
  - Scans double-quoted strings with escape sequences (`\n`, `\t`, `\\`, `\"`).
  - Tokenizes single-line comments (`// ...`) and multi-line comments (`/* ... */`).
  - Tracks 1-indexed `line` and `column` numbers for error diagnostics.
- **C++ Native Implementation (`Lexer.h`, `Lexer.cpp`)**:
  - Scans UTF-8 byte streams from standard C file streams (`FILE*`).
  - Accumulates multi-byte UTF-8 sequences for Thaana identifiers into standard C++ strings.
  - Recognizes keywords, numerical values, and ASCII punctuation.

### 2.2 Current Parser
- **Python / Wasm Implementation (`parser.py`, `web/parser.py`)**:
  - Top-down Operator Precedence (Pratt Parser) for expressions combined with recursive descent for statements.
  - Precedence hierarchy:
    1. `LOWEST` (0)
    2. `OR` (1: `||`, `ނުވަތަ`)
    3. `AND` (2: `&&`, `އަދި`)
    4. `EQUALS` (3: `==`, `!=`)
    5. `LESSGREATER` (4: `<`, `>`, `<=`, `>=`)
    6. `SUM` (5: `+`, `-`)
    7. `PRODUCT` (6: `*`, `/`, `%`)
    8. `PREFIX` (7: `-`, `!`)
    9. `CALL` (8: `(...)`)
    10. `INDEX` (9: `[...]`)
  - Parses statements until end-of-statement delimiters (`\n`, `;`, or block keywords).
  - Robust parser error collection (`self.errors`) without immediate crashing.
- **C++ Native Implementation (`Parser.h`, `Parser.cpp`)**:
  - Pratt expression parsing using `CurTok` and operator precedence lookup.
  - Parses top-level and user-defined functions (`FunctionAST`), variable declarations, conditions, and while loops.

### 2.3 AST Implementation
- **Python (`ast_nodes.py`, `web/ast_nodes.py`)**:
  - Base classes: `Node`, `Statement`, `Expression`.
  - Statements: `Program`, `LetStatement`, `ReturnStatement`, `PrintStatement`, `ExpressionStatement`, `BlockStatement`, `IfStatement`, `WhileStatement`, `ForInStatement`, `FunctionStatement`, `ImportStatement`, `TryCatchStatement`, `ThrowStatement`.
  - Expressions: `Identifier`, `NumberLiteral`, `StringLiteral`, `BooleanLiteral`, `ListLiteral`, `DictLiteral`, `IndexExpression`, `PrefixExpression`, `InfixExpression`, `CallExpression`.
- **C++ (`AST.h`)**:
  - Polymorphic class hierarchy rooted at `ExprAST` and `StmtAST`: `NumberExprAST`, `VariableExprAST`, `BinaryExprAST`, `CallExprAST`, `FunctionAST`, `LetStmtAST`, `PrintStmtAST`, `IfStmtAST`, `WhileStmtAST`.
  - Direct code generation via virtual `codegen()` emitting `llvm::Value*`.

### 2.4 Current Grammar
- **Syntax Direction**: Right-to-Left (RTL) for Thaana text; neutral for punctuation/operators.
- **Statements**:
  - Variable assignment: `ކަނޑައަޅާ <name> = <expr>`
  - Function declaration: `ވަޒީފާ <name>(<params>) <body> ނިމުނީ`
  - Conditionals: `ނަމަ <condition> <then_block> [ނޫންނަމަ <else_block>] ނިމުނީ`
  - Loops:
    - While: `ހިނދު <condition> <body> ނިމުނީ`
    - For-In: `ކޮންމެ <item> ތެރޭގައި <list> <body> ނިމުނީ`
  - Error Handling: `މަސައްކަތްކުރޭ <try_block> ކުށެއް_ފެނިއްޖެނަމަ <var> <catch_block> ނިމުނީ`
  - Module import: `ގެނޭ "<module_or_path>"`
  - Print statement: `ދައްކާ <expr>`
  - Return: `ފޮނުވާ <expr>`
  - Throw: `އުކާލާ <expr>`

### 2.5 Token Definitions
- **Constants (`token_types.py`)**:
  - Literals: `TT_IDENTIFIER`, `TT_NUMBER`, `TT_STRING`
  - Operators: `=`, `+`, `-`, `*`, `/`, `%`, `!`, `==`, `!=`, `<`, `>`, `<=`, `>=`
  - Delimiters: `(`, `)`, `{`, `}`, `[`, `]`, `:`, `,`, `;`
  - Special: `TT_ILLEGAL`, `TT_EOF`
  - Keywords: `TT_LET`, `TT_FUNCTION`, `TT_RETURN`, `TT_PRINT`, `TT_IF`, `TT_ELSE`, `TT_WHILE`, `TT_END`, `TT_TRUE`, `TT_FALSE`, `TT_AND`, `TT_OR`, `TT_FOR`, `TT_IN`, `TT_IMPORT`, `TT_TRY`, `TT_CATCH`, `TT_THROW`.

### 2.6 Keyword Definitions
- **Official Dhivehi Keywords**:
  - Declarations: `ކަނޑައަޅާ` (let)
  - Functions: `ވަޒީފާ` (function), `ފޮނުވާ` (return)
  - I/O: `ދައްކާ` (print)
  - Control Flow: `ނަމަ` (if), `ނޫންނަމަ` (else), `ހިނދު` (while), `ކޮންމެ` (for), `ތެރޭގައި` (in), `ނިމުނީ` (end)
  - Logic/Boolean: `އާން` (true), `ނޫން` (false), `އަދި` (and), `ނުވަތަ` (or)
  - Exceptions: `މަސައްކަތްކުރޭ` (try), `ކުށެއް_ފެނިއްޖެނަމަ` (catch), `އުކާލާ` (throw)
  - Modules: `ގެނޭ` (import)
- **Compatibility Keywords**:
  - `ބަހައްޓާ` (alias for `ކަނޑައަޅާ`)
  - `ފަންކް` (alias for `ވަޒީފާ`)
  - `ލިޔޭ` (alias for `ދައްކާ`)

### 2.7 Type System
- **Current Dynamic Types (`evaluator.py`)**:
  - `DhicodeNumber`: Floating-point (IEEE 754) with integer inspection formatting.
  - `DhicodeString`: UTF-8 native string.
  - `DhicodeBoolean`: `އާން` (True) or `ނޫން` (False).
  - `DhicodeList`: Dynamically sized vector of `DhicodeObject` items.
  - `DhicodeDict`: Hash map of string keys to `DhicodeObject` items.
  - `DhicodeNull`: Singleton representing null/none (`ހުސް`).
  - `DhicodeFunction`: User function containing formal parameters, AST block, and lexical environment closure.
  - `DhicodeBuiltin`: Native host function wrapper.
  - `DhicodeReturnValue`: Wrapper for explicit function exit values.
  - `DhicodeError`: Error encapsulation containing human-readable Dhivehi message, line, and column.
- **Current Type Checking**: Dynamic checking during evaluation and infix evaluation (`_eval_numeric_infix`, `_is_equal`).
- **Static Typing Status**: Missing static type checker and type annotations.

### 2.8 Semantic Analyzer
- Handled implicitly during tree-walk evaluation via lexical `Environment` scopes (`get`, `set`).
- Missing dedicated semantic analysis pass (dead-code elimination, variable scope validation before execution, type checking).

### 2.9 Interpreter
- **Evaluator (`evaluator.py`)**:
  - Recursive evaluation dispatching on AST node types.
  - Lexical closures: Functions capture their declaring environment (`Environment(fn.env)`).
  - Pluggable `output_callback` supporting CLI stdout, test interceptors, and web terminal append calls.
  - Automatic `މައި` (main) function entry-point invocation if defined in script.

### 2.10 Compiler
- **C++ LLVM Backend (`Codegen.cpp`, `Codegen.h`, `runtime.cpp`, `main.cpp`)**:
  - Generates LLVM IR using `llvm::IRBuilder<>` and `llvm::LLVMContext`.
  - Targets native machine code emitting relocatable `.o` object files.
  - Links against native C runtime library for `printf`, `scanf`, and mathematical operations.
- **Standalone Binary Packager (`dhicode.py build`)**:
  - Packages source code and complete runtime into standalone `.pyz` executable zipapp and Windows `.bat` launchers.

### 2.11 Virtual Machine (VM)
- Currently absent. System executes via tree-walk evaluator (Python/Wasm) or native AOT machine code (LLVM). Bytecode VM is a key target architecture component.

### 2.12 Runtime
- **Python Runtime (`evaluator.py`, `stdlib.py`)**: Dynamic object lifecycle, garbage-collected by host Python VM.
- **Native Runtime (`runtime.cpp`)**: C runtime functions `print_num(double)`, `print_str(const char*)`, `input_num()`.
- **Wasm Runtime (`web/app.js`, `web/tutorial.js`)**: Pyodide WebAssembly runtime running in browser sandbox.

### 2.13 Standard Library
1. `ހިސާބު` (Math): `ޖަޒުރު` (sqrt), `ބާރު` (pow), `ކައިރި` (round), `ފްލޯރ` (floor), `ސީލް` (ceil), `އެންމެ_ބޮޑު` (max), `އެންމެ_ކުޑަ` (min), `އިއްތިފާޤު` (random), `ޕައި` (pi).
2. `ފައިލް` (File System): `ކިޔާ` (read), `ލިޔޭ` (write), `އިތުރުކުރޭ` (append), `ވޭތޯ` (exists).
3. `ވަގުތު` (Time): `މިހާރު` (timestamp), `ހިނދުކޮޅު` (sleep), `ތާރީޚް` (formatted date string).
4. `ނިޒާމު` (System): `އާގިއުމެންޓުތައް` (CLI args), `ހުއްޓާ` (exit), `އެންވައިރޮންމެންޓް` (getenv).
5. `ނެޓްވޯކް` (Network & JSON): `ނަގާ` (HTTP GET), `ފޮނުވާ` (HTTP POST), `ޖޭސަން_ކިޔާ` (JSON parse), `ޖޭސަން_ހަދާ` (JSON stringify), `ޔޫއާރްއެލް_އެންކޯޑް`, `ޔޫއާރްއެލް_ޑީކޯޑް`.
6. `ނަކަތް` (Maldivian Nakaiy Calendar): 27 Nakaiy database with date boundaries, climate characteristics, `މިއަދުގެ_ނަކަތް()`, `ނަކަތް_ހޯދާ(މަސް, ދުވަސް)`, `ހުރިހާ_ނަކަތް()`.
7. `ނަމާދު` (Maldivian Prayer Times): Solar astronomical calculations for all atolls with Fajr, Sunrise, Dhuhr, Asr (Shafi'i), Maghrib, Isha, and `ދެން_އޮތް_ނަމާދު()`.
8. `ތާނަ_ހިސާބު` (Number-to-Words & Collation): `އަދަދު_ބަހަށް` (converts integers to Maldivian words), `ތާނަ_ތަރުތީބު` (alphabetical Thaana collation), `ތާނަ_އަކުރުތައް`.
9. Global Builtins: `ދިގުމިން` (len), `ބާވަތް` (type), `އަޅާ` (append), `ނަގާ` (pop), `ތަޅުދަނޑިތައް` (keys), `އަގުތައް` (values), `އަހާ` (input).

### 2.14 Package Manager
- Currently missing. The project needs `dhpm` with `dhicode.toml` package manifest support.

### 2.15 Command-Line Interface (CLI)
- `dhicode.py` provides:
  - `dhicode.py run <file.dhi>`: Executes script.
  - `dhicode.py build <file.dhi> [-o name]`: Compiles standalone binary bundle.
  - `dhicode.py fmt <file.dhi> [--write|--check]`: Formats source code.
  - `dhicode.py lsp`: Launches Language Server Protocol.
  - `dhicode.py repl`: Launches interactive shell.

### 2.16 REPL (Interactive Read-Eval-Print Loop)
- Terminal REPL with UTF-8 Windows terminal encoding auto-reconfiguration, line-by-line parsing, and persistent execution environment.

### 2.17 Error Handling
- Visual diagnostic formatter (`format_diagnostic`) with file location, line number, column number, source line display, and caret indicator (`^^^^`).
- Language constructs: `މަސައްކަތްކުރޭ` (try), `ކުށެއް_ފެނިއްޖެނަމަ` (catch), `އުކާލާ` (throw).

### 2.18 Testing Infrastructure
- `tests/test_dhi.py`: 13 core language unit tests.
- `tests/test_stdlib_extended.py`: 5 extended standard library tests.
- Fully runnable via `python -m unittest discover tests`.

### 2.19 Documentation
- `README.md`: Complete language guide, installation, and grammar cheat-sheet.
- `vscode-dhicode/README.md`: VS Code setup instructions.
- Online interactive documentation and keywords reference on GitHub Pages.

### 2.20 Examples
- `main.dhi`, `example.dhi`, `examples/advanced.dhi`.
- 8 interactive web examples in `web/examples.js`.
- 8 guided lessons in `web/tutorial.js`.

### 2.21 Existing Dhivehi Keywords
- 18 core keywords + 3 compatibility aliases (enumerated in section 2.6).

### 2.22 Existing English Aliases
- Documented in specification and partially mapped in TextMate grammar. Needs uniform lexer-level token mapping for dual English/Dhivehi keyword support.

### 2.23 Existing Unicode Support
- Unicode-first lexer recognizing `\u0780` - `\u07BF`. UTF-8 encoding enforced on Windows console stdout/stderr.

### 2.24 Existing Modules
- 8 standard library modules + relative/absolute `.dhi` file importing via `ގެނޭ`.

### 2.25 Existing Functions
- First-class lexical closures, multiple arguments, return values, recursion.

### 2.26 Existing Classes
- Not yet implemented. Data structures currently modeled using dictionaries (`DhicodeDict`) and closures.

### 2.27 Existing Object Model
- `DhicodeObject` polymorphic base with `type_str()` and `inspect()`.

### 2.28 Existing Memory Management
- Host runtime automatic garbage collection.

### 2.29 Existing Async Support
- Synchronous execution currently. Async/await and event loop abstractions are not yet implemented.

### 2.30 Existing Networking
- Basic HTTP client (GET, POST), JSON parse/serialize, URL encode/decode via `ނެޓްވޯކް` module. Sockets, WebSockets, and HTTP server are targets.

### 2.31 Existing Database Support
- Currently absent. SQLite, Postgres, Redis, and Key-Value abstractions are planned.

### 2.32 Existing AI Functionality
- Currently absent. Tensors, local model inference (GGUF/ONNX), embeddings, and agent framework are planned.
