<div align="center">

# 🇲🇻 DhiCode (ދިވެހި ކޯޑު)

**A modern, expressive programming language crafted for native Dhivehi (Thaana) speakers.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![C++: 17](https://img.shields.io/badge/C++-17-00599C.svg?logo=c%2B%2B&logoColor=white)](https://isocpp.org/)
[![LLVM Backend](https://img.shields.io/badge/Backend-LLVM-yellow.svg?logo=llvm&logoColor=white)](https://llvm.org/)
[![Tests](https://img.shields.io/badge/Tests-Passing_(13/13)-brightgreen.svg)]()
[![VS Code Extension](https://img.shields.io/badge/VS_Code-Supported-007ACC.svg?logo=visual-studio-code&logoColor=white)](vscode-dhicode/)
[![Web Playground](https://img.shields.io/badge/Playground-Live_WebAssembly-blueviolet.svg)](web/index.html)

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-web-playground">Web Playground</a> •
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-language-tour">Language Tour</a> •
  <a href="#-standard-library">Standard Library</a> •
  <a href="#-keywords--grammar">Keywords & Grammar</a> •
  <a href="#-vs-code-extension">VS Code Extension</a> •
  <a href="#-architecture">Architecture</a>
</p>

---

</div>

## 🌟 Features

- **🇲🇻 Native Thaana Unicode Support**: First-class handling of Thaana letters (`\u0780`–`\u07A5`), *fili* vowel diacritics (`\u07A6`–`\u07B0`), and *sukun* (`\u07B1`) across identifiers, strings, and operators.
- **⚡ Dual-Engine System**:
  - **Tree-Walk Interpreter & Interactive REPL**: Instant, zero-dependency execution in Python for rapid prototyping and education.
  - **LLVM Native Compiler**: Compiles DhiCode into optimized native machine code and object files (`.o`).
- **📊 Compound Data Structures**: Built-in support for **Lists** (`[1, 2, 3]`), negative indexing, **Dictionaries** (`{"ނަން": "ޢަލީ"}`), and collection utilities (`އަޅާ`, `ނަގާ`, `ތަޅުދަނޑިތައް`, `އަގުތައް`).
- **🔁 Rich Control Flow**: Conditionals (`ނަމަ` / `ނޫންނަމަ`), while loops (`ހިނދު`), and for-each iteration (`ކޮންމެ ... ތެރޭގައި`).
- **🛡️ Dhivehi Exception Handling**: Native try-catch recovery (`މަސައްކަތްކުރޭ` ... `ކުށެއް_ފެނިއްޖެނަމަ`) and custom error throwing (`އުކާލާ`).
- **📚 Modular Standard Library (`ގެނޭ`)**: Built-in modules for Math (`ހިސާބު`), File System (`ފައިލް`), Date & Time (`ވަގުތު`), and System (`ނިޒާމު`).
- **🌐 Interactive Web Playground**: Runs 100% in the web browser using WebAssembly (Pyodide), with sample programs and RTL toggle.
- **🎨 Official VS Code Extension**: Full syntax coloring, bracket matching, block folding, and auto-completion snippets for `.dhi` files.
- **🧪 Automated Test Suite**: 100% passing unit tests covering all core and advanced language features.

---

## 🌐 Web Playground (އިންޓަރނެޓް ޕްލޭގްރައުންޑް)

Run DhiCode directly in your browser with zero installation:
- **Location**: [`web/index.html`](web/index.html)
- **Features**: Live code editor with RTL/LTR toggle, example presets, and browser-side WebAssembly terminal.
- **Run locally**:
  ```bash
  python -m http.server 8000
  ```
  Then open `http://localhost:8000/web/` in your browser!

---

## 🚀 Quickstart

### 1. Run a DhiCode Program
```bash
python dhicode.py run main.dhi
python dhicode.py run examples/advanced.dhi
```

### 2. Interactive REPL (ކޯޑު ޝެލް)
```bash
python dhicode.py repl
```

```text
========================================
 DhiCode (ދިވެހި ކޯޑު) REPL v0.3.0
 Type Dhivehi code or 'exit' / 'ހުއްޓާ' to quit.
========================================
ދިވެހި> ކަނޑައަޅާ ލިސްޓު = ["މާލެ", "ހުޅުމާލެ"]
["މާލެ", "ހުޅުމާލެ"]
ދިވެހި> އަޅާ(ލިސްޓު, "ވިލިމާލެ")
["މާލެ", "ހުޅުމާލެ", "ވިލިމާލެ"]
ދިވެހި> ލިސްޓު[-1]
"ވިލިމާލެ"
```

### 3. Run Automated Tests
```bash
python tests/test_dhi.py
```
```text
.............
----------------------------------------------------------------------
Ran 13 tests in 0.002s

OK
```

---

## 📖 Language Tour

### 1. Variables & Types
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

### 2. Lists & Dictionaries (`ލިސްޓު` އަދި `ރަދީފު`)
```dhicode
// ލިސްޓު ހެދުމާއި އިންޑެކްސް ކުރުން
ކަނޑައަޅާ މޭވާތައް = ["އަނބު", "ކެޔޮ", "ޖަންބުރޯލު"]
އަޅާ(މޭވާތައް, "ފަޅޯ") // ލިސްޓަށް އިތުރުކުރުން
ދައްކާ މޭވާތައް[0]   // އަނބު
ދައްކާ މޭވާތައް[-1]  // ފަޅޯ

// ރަދީފު (Dictionary)
ކަނޑައަޅާ މީހާ = {"ނަން": "ޙަސަން", "ވަޒީފާ": "އިންޖިނޭރު"}
ދައްކާ މީހާ["ނަން"] // ޙަސަން
```

### 3. For-Each Loops (`ކޮންމެ ... ތެރޭގައި`)
```dhicode
ކަނޑައަޅާ އަދަދުތައް = [10, 20, 30]

ކޮންމެ އަދަދު ތެރޭގައި އަދަދުތައް
    ދައްކާ އަދަދު * 2
ނިމުނީ
```

### 4. Conditionals & While Loops
```dhicode
// ނަމަ ... ނޫންނަމަ ... ނިމުނީ
ނަމަ އުމުރު >= 18
    ދައްކާ "ބޮޑު މީހެއް"
ނޫންނަމަ
    ދައްކާ "ކުޑަކުއްޖެއް"
ނިމުނީ

// ހިނދު ... ނިމުނީ
ކަނޑައަޅާ ގުނާ = 1
ހިނދު ގުނާ <= 5
    ދައްކާ ގުނާ
    ކަނޑައަޅާ ގުނާ = ގުނާ + 1
ނިމުނީ
```

### 5. Functions & Recursion (`ވަޒީފާ` ... `ފޮނުވާ`)
```dhicode
ވަޒީފާ ފެކްޓޯރިއަލް(އަދަދު)
    ނަމަ އަދަދު <= 1
        ފޮނުވާ 1
    ނިމުނީ
    ފޮނުވާ އަދަދު * ފެކްޓޯރިއަލް(އަދަދު - 1)
ނިމުނީ

ދައްކާ ފެކްޓޯރިއަލް(5) // 120
```

### 6. Exception Handling (`މަސައްކަތްކުރޭ` / `ކުށެއް_ފެނިއްޖެނަމަ`)
```dhicode
މަސައްކަތްކުރޭ
    ކަނޑައަޅާ ޖަވާބު = 100 / 0
ކުށެއް_ފެނިއްޖެނަމަ މައްސަލަ
    ދައްކާ "ކުށެއް ސަލާމަތްކުރެވިއްޖެ: " + މައްސަލަ
ނިމުނީ
```

---

## 📚 Standard Library (`ގެނޭ`)

Import built-in standard library modules using `ގެނޭ "<module>"`:

### 1. `ހިސާބު` (Math)
```dhicode
ގެނޭ "ހިސާބު"

ދައްކާ ޖަޒުރު(100)        // Square Root: 10
ދައްކާ ބާރު(2, 5)          // Power: 32
ދައްކާ ކައިރި(9.7)          // Round: 10
ދައްކާ ޕައި                // 3.141592653589793
ދައްކާ އިއްތިފާޤު(1, 50)    // Random integer between 1 and 50
```

### 2. `ފައިލް` (File System)
```dhicode
ގެނޭ "ފައިލް"

ލިޔޭ("test.txt", "ސަލާމް ދިވެހިރާއްޖެ") // Write text to file
ކަނޑައަޅާ ލިޔުން = ކިޔާ("test.txt")    // Read text from file
ދައްކާ ލިޔުން
```

### 3. `ވަގުތު` (Time)
```dhicode
ގެނޭ "ވަގުތު"

ދައްކާ ތާރީޚް()   // Current date & time string
ހިނދުކޮޅު(2)      // Sleep for 2 seconds
```

### 4. `ނެޓްވޯކް` (Network, HTTP & JSON)
```dhicode
ގެނޭ "ނެޓްވޯކް"

// JSON serialization & deserialization
ކަނޑައަޅާ މީހާ = {"ނަން": "ޢަލީ", "އުމުރު": 28}
ކަނޑައަޅާ ޖޭސަން_ލިޔުން = ޖޭސަން_ހަދާ(މީހާ)
ކަނޑައަޅާ އަލުން = ޖޭސަން_ކިޔާ(ޖޭސަން_ލިޔުން)

// HTTP GET
ކަނޑައަޅާ ޖަވާބު = ނަގާ("https://api.github.com/users/siyamex")
ދައްކާ "ސްޓޭޓަސް ކޯޑު: " + ޖަވާބު["ކޯޑު"]
```

### 5. `ނަކަތް` (Maldivian Nakaiy Calendar)
```dhicode
ގެނޭ "ނަކަތް"

// މިއަދުގެ ނަކަތް
ކަނޑައަޅާ މިއަދު = މިއަދުގެ_ނަކަތް()
ދައްކާ "ނަކަތް: " + މިއަދު["ނަން"]
ދައްކާ "މޫސުން: " + މިއަދު["މޫސުން"] // ހުޅަނގު ނުވަތަ އިރުވައި
ދައްކާ "ސިފަ: " + މިއަދު["ސިފަ"]

// ވަކި ތާރީޚެއްގެ ނަކަތް ހޯދުން (މަސް, ދުވަސް)
ކަނޑައަޅާ ކެތި = ނަކަތް_ހޯދާ(5, 10)
```

### 6. `ނަމާދު` (Maldivian Prayer Times)
```dhicode
ގެނޭ "ނަމާދު"

ކަނޑައަޅާ ވަގުތު = މިއަދުގެ_ވަގުތު("މާލެ")
ދައްކާ "ފަތިސް: " + ވަގުތު["ފަތިސް"]
ދައްކާ "މެންދުރު: " + ވަގުތު["މެންދުރު"]
ދައްކާ "ޢަޞުރު: " + ވަގުތު["ޢަޞުރު"]
ދައްކާ "މަޣްރިބް: " + ވަގުތު["މަޣްރިބް"]
ދައްކާ "ޢިޝާ: " + ވަގުތު["ޢިޝާ"]

// ދެން އެންމެ އަވަހަށް އޮތް ނަމާދު
ކަނޑައަޅާ ދެން = ދެން_އޮތް_ނަމާދު("މާލެ")
ދައްކާ "ދެން އޮތީ: " + ދެން["ނަމާދު"] + " (" + ދެން["ބާކީ_މިނިޓް"] + " މިނިޓް)"
```

### 7. `ތާނަ_ހިސާބު` (Number-to-Words & Collation)
```dhicode
ގެނޭ "ތާނަ_ހިސާބު"

// އަދަދު ދިވެހި ބަހަށް ބަދަލުކުރުން
ދައްކާ އަދަދު_ބަހަށް(125)   // "ސަތޭކަ ފަންސަވީސް"
ދައްކާ އަދަދު_ބަހަށް(2026)  // "ދެހާސް ސައްބީސް"

// ތާނަ އަލިފުބާގެ ތަރުތީބުން އެތުރުން (ހ ށ ނ ރ ބ...)
ކަނޑައަޅާ ބަސްތައް = ["ރަށް", "ހަނދު", "ނަން", "ށީ"]
ދައްކާ ތާނަ_ތަރުތީބު(ބަސްތައް) // ["ހަނދު", "ށީ", "ނަން", "ރަށް"]
```

---

## 🛠️ CLI Tools & Packager

### 1. Build Standalone Executable Binary
Bundle your `.dhi` program and the entire DhiCode runtime into a self-contained executable file:
```bash
python dhicode.py build main.dhi -o dist/myapp
```
This generates `dist/myapp.pyz` (cross-platform standalone zipapp) and `dist/myapp.bat` (Windows launcher), executable directly with zero dependencies!

### 2. Code Formatter (`dhicode fmt`)
Format and standardize your Thaana code with canonical 4-space block indentation and clean operator spacing:
```bash
python dhicode.py fmt main.dhi --write
```

### 3. Language Server Protocol (`dhicode lsp`)
Launch the built-in JSON-RPC 2.0 Language Server providing diagnostics, hover documentation, and auto-completion for VS Code and other editors:
```bash
python dhicode.py lsp
```

---

## 🎓 Interactive Dhivehi Coding Academy
Learn DhiCode right in your browser with our step-by-step interactive course featuring live validation and progressive challenges:
👉 **[https://siyamex.github.io/DhiCode/tutorial.html](https://siyamex.github.io/DhiCode/tutorial.html)**

---

## 📚 Keywords & Grammar

| Category | Keyword | Transliteration | English Equivalent |
|:---|:---|:---|:---|
| **Declarations** | `ކަނޑައަޅާ` / `ބަހައްޓާ` | kanda'alhaa / bahattaa | `let` / `const` |
| **Functions** | `ވަޒީފާ` / `ފަންކް` | vazeefaa / fank | `function` |
| | `ފޮނުވާ` | fonuvaa | `return` |
| **Output** | `ދައްކާ` / `ލިޔޭ` | dhakkaa / liye | `print` / `write` |
| **Control Flow**| `ނަމަ` | nama | `if` |
| | `ނޫންނަމަ` | noonnama | `else` |
| | `ހިނދު` | hindhu | `while` |
| | `ކޮންމެ` | konme | `for` |
| | `ތެރޭގައި` | thereygai | `in` |
| | `ނިމުނީ` | nimunee | `end` |
| **Exceptions** | `މަސައްކަތްކުރޭ` | masakkaiy kurey | `try` |
| | `ކުށެއް_ފެނިއްޖެނަމަ` | kusheh fenijjenama | `catch` |
| | `އުކާލާ` | ukaalaa | `throw` |
| **Modules** | `ގެނޭ` | geney | `import` |
| **Booleans** | `އާން` | aan | `true` |
| | `ނޫން` | noon | `false` |
| **Logic** | `އަދި` | adhi | `and` (`&&`) |
| | `ނުވަތަ` | nuvatha | `or` (`\|\|`) |

---

## 🎨 Visual Studio Code Extension

Syntax highlighting, snippets, and editor support are packaged in [`vscode-dhicode/`](vscode-dhicode/).

### Installation (Windows PowerShell):
```powershell
Copy-Item -Recurse -Force "vscode-dhicode" "$env:USERPROFILE\.vscode\extensions\vscode-dhicode"
```

Restart VS Code, and `.dhi` files will immediately have syntax coloring and Dhivehi auto-completion snippets (`konme`, `trycatch`, `gene`, `vazeefaa`, `nama`, `hindhu`).

---

## 🏗️ Architecture

```
DhiCode/
├── dhicode.py              # CLI Runner, Builder, Formatter & REPL
├── lexer.py                # Python UTF-8 Thaana Lexer
├── parser.py               # Pratt Precedence Parser
├── ast_nodes.py            # AST Node Definitions
├── evaluator.py            # Tree-walk Evaluator & Runtime
├── formatter.py            # Canonical Thaana Code Formatter
├── lsp_server.py           # JSON-RPC 2.0 Language Server Protocol Server
├── stdlib.py               # Standard Library (Math, File, Time, Network, Nakaiy, Prayer, Thaana)
├── token_types.py          # Unified Token Definitions
│
├── web/                    # Modern Light-Theme Web Portal & Interactive Academy
│   ├── index.html          # Main Portal & Web Playground
│   ├── tutorial.html       # Interactive Dhivehi Coding Academy
│   ├── style.css           # Modern Developer Design System
│   ├── app.js              # Real-Time Syntax Highlighter & Wasm Runner
│   ├── tutorial.js         # Curriculum & Interactive Auto-Grader
│   └── examples.js         # Interactive Code Examples
│
├── .github/workflows/
│   └── deploy-pages.yml    # Automated GitHub Pages Deployment
│
├── vscode-dhicode/         # Visual Studio Code Extension (LSP, Hover, Snippets)
│
├── tests/
│   ├── test_dhi.py         # Core language unit test suite
│   └── test_stdlib_extended.py # Extended stdlib test suite (18 tests total)
├── examples/
│   └── advanced.dhi        # Advanced showcase script
├── main.dhi                # Sample script
└── example.dhi             # Function sample script
```

---

## 📜 License

Dedicated to the public domain under **[Creative Commons CC0 1.0 Universal](LICENSE)**.
