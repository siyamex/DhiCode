<div align="center">

# 🇲🇻 DhiCode (ދިވެހި ކޯޑު)

**A modern, expressive programming language crafted for native Dhivehi (Thaana) speakers.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![C++: 17](https://img.shields.io/badge/C++-17-00599C.svg?logo=c%2B%2B&logoColor=white)](https://isocpp.org/)
[![LLVM Backend](https://img.shields.io/badge/Backend-LLVM-yellow.svg?logo=llvm&logoColor=white)](https://llvm.org/)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()
[![VS Code Extension](https://img.shields.io/badge/VS_Code-Supported-007ACC.svg?logo=visual-studio-code&logoColor=white)](vscode-dhicode/)

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-language-tour">Language Tour</a> •
  <a href="#-keywords--grammar">Keywords & Grammar</a> •
  <a href="#-vs-code-extension">VS Code Extension</a> •
  <a href="#-native-compiler">Native Compiler</a> •
  <a href="#-architecture">Architecture</a>
</p>

---

</div>

## 🌟 Features

- **🇲🇻 Native Thaana Unicode Support**: First-class handling of Thaana letters (`\u0780`–`\u07A5`), *fili* vowel diacritics (`\u07A6`–`\u07B0`), and *sukun* (`\u07B1`) across identifiers, strings, and operators.
- **⚡ Dual-Engine System**:
  - **Tree-Walk Interpreter & Interactive REPL**: Instant, zero-dependency execution in Python for rapid prototyping and education.
  - **LLVM Native Compiler**: Compiles DhiCode into optimized native machine code and object files (`.o`).
- **🧠 Complete Pratt Expression Parser**: Supports operator precedence climbing for arithmetic (`+`, `-`, `*`, `/`, `%`), comparisons (`==`, `!=`, `<`, `>`, `<=`, `>=`), and logical operators (`އަދި`, `ނުވަތަ`).
- **🔁 Full Control Flow**: Structured conditionals (`ނަމަ` / `ނޫންނަމަ` / `ނިމުނީ`) and loops (`ހިނދު` ... `ނިމުނީ`).
- **📦 First-Class Functions**: Parameters, recursion, return statements (`ފޮނުވާ`), and lexical closures.
- **🎨 Official VS Code Extension**: Full syntax coloring, bracket matching, block folding, and auto-completion snippets for `.dhi` files.
- **🧪 Built-in Test Suite**: 100% test coverage across core language constructs.

---

## 🚀 Quickstart

### Prerequisites
- **Python 3.8+** (for interpreter and REPL)
- *(Optional)* **CMake & LLVM 10+** (only needed for native compilation to binary)

### 1. Run a DhiCode Program
Clone the repository and run any `.dhi` file directly:

```bash
git clone https://github.com/your-username/DhiCode.git
cd DhiCode
python dhicode.py run main.dhi
```

**Output:**
```text
އަޙްމަދު އަކީ ބޮޑު މީހެއް
```

---

### 2. Interactive REPL (ކޯޑު ޝެލް)

Launch the interactive Dhivehi shell with Windows UTF-8 terminal support:

```bash
python dhicode.py repl
```

```text
========================================
 DhiCode (ދިވެހި ކޯޑު) REPL v0.2.0
 Type Dhivehi code or 'exit' / 'ހުއްޓާ' to quit.
========================================
ދިވެހި> ކަނޑައަޅާ އަގު1 = 40
40
ދިވެހި> ކަނޑައަޅާ އަގު2 = 2
42
ދިވެހި> އަގު1 + އަގު2
42
ދިވެހި> "މަރުޙަބާ " + "ދިވެހިރާއްޖެ"
"މަރުޙަބާ ދިވެހިރާއްޖެ"
```

---

### 3. Run Automated Tests

Execute the comprehensive test suite:

```bash
python tests/test_dhi.py
```

```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```

---

## 📖 Language Tour

### Variables & Data Types
```dhicode
// ނަންބަރު (Numbers)
ކަނޑައަޅާ އުމުރު = 25
ކަނޑައަޅާ އަގު = 99.5

// ލިޔުން (Strings)
ކަނޑައަޅާ ނަން = "ޢަލީ"

// ބޫލިއަން (Booleans)
ކަނޑައަޅާ ތެދު = އާން
ކަނޑައަޅާ ދޮގު = ނޫން
```

### Conditionals (`ނަމަ` ... `ނޫންނަމަ` ... `ނިމުނީ`)
```dhicode
ނަމަ އުމުރު >= 18
    ދައްކާ ނަން + " އަކީ ބޮޑު މީހެއް"
ނޫންނަމަ
    ދައްކާ ނަން + " އަކީ ކުޑަކުއްޖެއް"
ނިމުނީ
```

### Loops (`ހިނދު` ... `ނިމުނީ`)
```dhicode
ކަނޑައަޅާ ޖުމްލަ = 0
ކަނޑައަޅާ ގުނާ = 1

ހިނދު ގުނާ <= 10
    ކަނޑައަޅާ ޖުމްލަ = ޖުމްލަ + ގުނާ
    ކަނޑައަޅާ ގުނާ = ގުނާ + 1
ނިމުނީ

ދައްކާ "1 އިން 10 އަށް އެއްކުރުމުން: " + ޖުމްލަ
```

### Functions & Recursion (`ވަޒީފާ` ... `ފޮނުވާ` ... `ނިމުނީ`)
```dhicode
ވަޒީފާ ފެކްޓޯރިއަލް(އަދަދު)
    ނަމަ އަދަދު <= 1
        ފޮނުވާ 1
    ނިމުނީ
    ފޮނުވާ އަދަދު * ފެކްޓޯރިއަލް(އަދަދު - 1)
ނިމުނީ

ކަނޑައަޅާ ނަތީޖާ = ފެކްޓޯރިއަލް(5)
ދައްކާ "5 ގެ ފެކްޓޯރިއަލް = " + ނަތީޖާ // 120
```

### Built-in Functions
- `ދައްކާ(...)` / `ލިޔޭ(...)`: Output any value to console.
- `އަހާ(...)`: Prompt user for console input.
- `ދިގުމިން(...)`: Returns the length of a string.
- `ބާވަތް(...)`: Returns the type name (`ނަންބަރު`, `ލިޔުން`, `ބޫލިއަން`).

---

## 📚 Keywords & Grammar

| Category | DhiCode Keyword | Transliteration | English Equivalent | Description |
|:---|:---|:---|:---|:---|
| **Declarations** | `ކަނޑައަޅާ` / `ބަހައްޓާ` | kanda'alhaa / bahattaa | `let` / `const` | Variable declaration |
| **Functions** | `ވަޒީފާ` / `ފަންކް` | vazeefaa / fank | `function` | Function definition |
| | `ފޮނުވާ` | fonuvaa | `return` | Return from function |
| **Output** | `ދައްކާ` / `ލިޔޭ` | dhakkaa / liye | `print` / `write` | Output to console |
| **Control Flow**| `ނަމަ` | nama | `if` | Conditional branch |
| | `ނޫންނަމަ` | noonnama | `else` | Alternative branch |
| | `ހިނދު` | hindhu | `while` | Loop while true |
| | `ނިމުނީ` | nimunee | `end` | End of block |
| **Booleans** | `އާން` | aan | `true` | Boolean true |
| | `ނޫން` | noon | `false` | Boolean false |
| **Logic** | `އަދި` | adhi | `and` (`&&`) | Logical AND |
| | `ނުވަތަ` | nuvatha | `or` (`\|\|`) | Logical OR |

> **Note on Syntax Compatibility**: DhiCode supports both natural keyword-delimited blocks (`ނަމަ ... ނިމުނީ`) and C-style braces (`{ ... }`).

---

## 🎨 Visual Studio Code Extension

Syntax highlighting, snippets, and editor support are packaged in [`vscode-dhicode/`](vscode-dhicode/).

### Installation

#### Windows (PowerShell):
```powershell
Copy-Item -Recurse -Force "vscode-dhicode" "$env:USERPROFILE\.vscode\extensions\vscode-dhicode"
```

#### macOS / Linux:
```bash
cp -r vscode-dhicode ~/.vscode/extensions/vscode-dhicode
```

### Extension Features
- **Syntax Highlighting**: Oniguruma TextMate grammar with Unicode lookarounds specifically tuned for Thaana script.
- **Snippets**: Auto-complete common blocks by typing:
  - `vazeefaa` ➔ Function definition block
  - `nama` / `namanoon` ➔ If / If-Else conditionals
  - `hindhu` ➔ While loop
  - `kanda` ➔ Variable declaration
  - `dhakkaa` ➔ Print statement
- **Auto-Closing & Formatting**: Auto-pairs for `""`, `()`, `{}`, and code folding between keywords and `ނިމުނީ`.

---

## ⚙️ Native Compiler (C++ / LLVM)

For high-performance standalone executables, DhiCode includes an LLVM front-end and runtime:

```
Source (.dhi) ➔ C++ Lexer & Pratt Parser ➔ LLVM IR Generation ➔ Machine Code (.o / .exe)
```

### Building the Compiler (`dhic`):

```bash
mkdir build && cd build
cmake ..
cmake --build . --config Release
```

### Compiling to Native Object:
```bash
./dhic ../main.dhi -o output.o --emit-ir
```

---

## 🏗️ Architecture

```
DhiCode/
├── dhicode.py              # CLI Runner & Interactive REPL
├── lexer.py                # Python UTF-8 Thaana Lexer & Tokenizer
├── parser.py               # Python Pratt Operator Precedence Parser
├── ast_nodes.py            # AST Node Definitions
├── evaluator.py            # Tree-walk Evaluator & Runtime Environment
├── token_types.py          # Unified Token Definitions
│
├── Lexer.h / Lexer.cpp     # C++ UTF-8 Lexer
├── Parser.h / Parser.cpp   # C++ Pratt Parser
├── AST.h                   # C++ AST Node Hierarchy
├── Codegen.h / Codegen.cpp # LLVM IR & Target Machine Emitter
├── runtime.cpp             # C Runtime (string concat, I/O, numbers)
├── main.cpp                # Native compiler driver (dhic)
├── CMakeLists.txt          # LLVM build configuration
│
├── vscode-dhicode/         # Visual Studio Code Extension
│   ├── package.json
│   ├── language-configuration.json
│   ├── syntaxes/dhicode.tmLanguage.json
│   └── snippets/dhicode.json
│
├── tests/
│   └── test_dhi.py         # Automated unit test suite
├── main.dhi                # Sample DhiCode script
└── example.dhi             # Function sample script
```

---

## 🗺️ Roadmap

- [x] Full Thaana Unicode support and tokenization
- [x] Pratt parser for expressions and binary operators
- [x] Control flow: `ނަމަ`, `ނޫންނަމަ`, `ހިނދު`, `ނިމުނީ`
- [x] First-class functions and recursion
- [x] Tree-walk interpreter and interactive REPL
- [x] VS Code syntax highlighting and snippets extension
- [x] C++ Pratt parser & LLVM IR generator
- [ ] Standard Library: File I/O (`ފައިލް`), Math (`ހިސާބު`), DateTime (`ވަގުތު`)
- [ ] Language Server Protocol (LSP) for hover documentation and diagnostics
- [ ] WebAssembly (Wasm) Playground for running DhiCode in modern web browsers

---

## 🤝 Contributing

Contributions, feedback, and language design suggestions from native Dhivehi speakers and the open-source community are warmly welcomed! Feel free to open an issue or submit a pull request.

---

## 📜 License

This project is dedicated to the public domain under the **[Creative Commons CC0 1.0 Universal](LICENSE)** license. You are free to copy, modify, distribute, and perform the work, even for commercial purposes, all without asking permission.
