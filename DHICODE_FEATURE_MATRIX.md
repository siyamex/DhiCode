# DHicode Comprehensive Feature Matrix

**Status Key:**
- **Existing (✅)**: Fully implemented, tested, and actively functional.
- **Partial (🟡)**: Implemented in prototype form, partially supported in one engine, or requires expansion.
- **Missing (❌)**: Not yet implemented in the codebase.
- **Target**: Intended target milestone / architectural goal.

---

## 1. Core Language & Syntax

| Feature | Existing | Partial | Missing | Target |
| :--- | :---: | :---: | :---: | :--- |
| **Dhivehi / Thaana Syntax** | ✅ | | | Core language design with native Thaana characters |
| **Dual English Keywords** | ✅ | | | Full lexer & parser mapping for English keywords (`if`, `let`, `fn`, `const`, etc.) |
| **Unicode-First Identifiers** | ✅ | | | Support for Thaana, Latin, Arabic, and international scripts |
| **Comments (Line & Block)** | ✅ | | | `//` single-line and `/* ... */` multi-line |
| **Mutable Variables (`ކަނޑައަޅާ` / `let`)** | ✅ | | | Dynamic assignment, re-assignment, and compound assignment |
| **Constants / Immutable (`ދާއިމީ` / `const`)** | ✅ | | | Immutable variable declarations with runtime protection |
| **Multiple Assignment & Destructuring** | ✅ | | | `ކަނޑައަޅާ [a, b] = [1, 2]`, `let {name, age} = user` |
| **Static Type Annotations** | | | ❌ | Optional typing: `އުމުރު: Integer = 25` |
| **Type Inference Engine** | | 🟡 | | Dynamic type inference at runtime; target static inference |
| **First-Class Functions (`ވަޒީފާ` / `fn`)** | ✅ | | | Lexical closures, higher-order functions, recursion |
| **Default & Named Parameters** | ✅ | | | `ވަޒީފާ ހަދާ(ނަން, އުމުރު = 18)`, `fn greet(name, title = "Mr.")` |
| **Variadic Arguments (`...args`)** | ✅ | | | Variable-length function argument lists (`...args`, `...އާގްސް`) |
| **Anonymous Functions / Lambdas** | ✅ | | | Lightweight arrow syntax `(x) => x * 2`, `(a, b) => a + b` |
| **Pipeline Operator (`\|>`)** | | | ❌ | Functional pipeline `data \|> filter(...) \|> map(...)` |
| **Object-Oriented Classes** | ✅ | | | `class` / `ކްލާސް`, `constructor` / `ހަދާ_ވަޒީފާ`, `methods`, `inheritance` (`extends` / `ދަރިކޮޅު`), `this` / `މި` |
| **Structs / Records** | | | ❌ | Lightweight typed data structures |
| **Enums with Associated Values** | | | ❌ | Tagged unions / enums |
| **Generics (`List<T>`)** | | | ❌ | Generic functions, structs, and interfaces |
| **Pattern Matching (`match`)** | | | ❌ | Structural pattern matching with guards |
| **Exception Handling (`try/catch/throw`)**| ✅ | | | `މަސައްކަތްކުރޭ`, `ކުށެއް_ފެނިއްޖެނަމަ`, `އުކާލާ` |
| **Result & Option Monads** | | | ❌ | `Result<T, E>` and `Option<T>` for zero-crash safety |

---

## 2. Operators & Expressions

| Feature | Existing | Partial | Missing | Target |
| :--- | :---: | :---: | :---: | :--- |
| **Arithmetic (`+`, `-`, `*`, `/`, `%`)** | ✅ | | | Standard numeric operations with Pratt parser |
| **Exponentiation (`**`)** | ✅ | | | Infix `**` with right-associativity and `ބާރު()` stdlib |
| **Comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`)** | ✅ | | | Value and identity equality |
| **Logical (`އަދި` / `&&` / `and`, `ނުވަތަ` / `\|\|` / `or`, `!` / `not`)** | ✅ | | | Short-circuit evaluation with dual keywords |
| **Bitwise (`&`, `\|`, `^`, `~`, `<<`, `>>`)** | ✅ | | | Low-level bitwise manipulation |
| **Compound Assignment (`+=`, `-=`, `*=`, `/=`, `%=`)** | ✅ | | | Inplace mutation on variables and collection indices |
| **Null Coalescing (`??`)** | ✅ | | | Safe fallback for `ހުސް` / `null` with short-circuiting |
| **Optional Chaining (`?.`)** | | | ❌ | Safe nested property traversal |
| **Range Operator (`..`)** | ✅ | | | Range generation for expressions and loops: `1..10` |

---

## 3. Data Types & Collections

| Feature | Existing | Partial | Missing | Target |
| :--- | :---: | :---: | :---: | :--- |
| **Integers & Floats** | ✅ | | | `DhicodeNumber` (unified 64-bit precision) |
| **Strings (UTF-8 Native)** | ✅ | | | Unicode strings with escape sequences |
| **String Interpolation** | ✅ | | | `"މަރުޙަބާ {ނަން}"` runtime expressions inside strings |
| **Booleans (`އާން` / `ނޫން`)** | ✅ | | | Native truthy/falsy evaluation |
| **Null Type (`ހުސް`)** | ✅ | | | Native null representation |
| **Dynamic Lists (`[...]`)** | ✅ | | | Indexing, negative indexing, append, pop, len |
| **Hash Dictionaries (`{...}`)** | ✅ | | | Key-value pairs with string indexing |
| **Sets & HashSets** | | | ❌ | Unique collections with set algebra |
| **Tuples** | | | ❌ | Fixed-size heterogeneous sequences |
| **Queues, Deques & Stacks** | | 🟡 | | Array-based append/pop; target dedicated stdlib types |
| **BigInteger & Decimal** | | | ❌ | Arbitrary precision arithmetic |

---

## 4. Standard Library Modules

| Feature | Existing | Partial | Missing | Target |
| :--- | :---: | :---: | :---: | :--- |
| **Math (`ހިސާބު` / `math`)** | ✅ | | | Sqrt, pow, round, floor, ceil, min, max, random, pi, sin, cos, tan, abs, log, e |
| **File System (`ފައިލް` / `file`)** | ✅ | | | Read, write, append, exists, delete, size |
| **Directory Operations** | ✅ | | | Directory create (`mkdir`), list (`list_dir`), delete (`delete`) |
| **Time & Date (`ވަގުތު` / `time`)** | ✅ | | | Timestamp, sleep, formatted date strings, date parsing |
| **System Info & Env (`ނިޒާމު` / `os`)** | ✅ | | | CLI arguments, exit, getenv, platform, cwd |
| **Network & HTTP Client (`ނެޓްވޯކް` / `net`)** | ✅ | | | HTTP GET, POST, PUT, DELETE, JSON parse/stringify, URL codec |
| **HTTP Web Server (`ނެޓްވޯކް.ސާވަރު` / `http.serve`)** | ✅ | | | Native micro-framework for REST APIs, request routing, JSON & HTML responses |
| **WebSocket Client & Server** | | | ❌ | Real-time bidirectional socket communication |
| **Nakaiy Calendar (`ނަކަތް` / `nakaiy`)** | ✅ | | | 27 Nakaiy database, daily lookup, climate traits, monsoon determination, day counter |
| **Prayer Times (`ނަމާދު` / `prayer`)** | ✅ | | | Solar calculation for all Maldivian atolls, next prayer, Hijri calendar converter |
| **Thaana Words & Collation (`ތާނަ` / `thaana`)** | ✅ | | | Number-to-words, Thaana collation, fili stripping, currency MVR, Latin transliteration |
| **Regular Expressions (`ރެގެކްސް` / `regex`)** | ✅ | | | Unicode-aware pattern matching, searching, replacement, and splitting |
| **Cryptography (`ކްރިޕްޓޯ` / `crypto`)** | ✅ | | | SHA-256, SHA-512, MD5, HMAC-SHA256, Base64 encode/decode, secure random token |
| **Database Abstraction (`ޑޭޓާބޭސް` / `db`)** | ✅ | | | Embedded SQLite database, parameterized queries, transactions, commit & rollback |
| **AI & Machine Learning (`އޭއައި`)** | | | ❌ | Tensors, GGUF/ONNX inference, embeddings, agents |

---

## 5. Execution Backends & Runtimes

| Feature | Existing | Partial | Missing | Target |
| :--- | :---: | :---: | :---: | :--- |
| **Tree-Walk Interpreter** | ✅ | | | Fast prototyping, development, scripting |
| **Bytecode Compiler & VM** | | | ❌ | Fast, portable bytecode VM with opcode dispatch |
| **LLVM Native Compiler (AOT)** | | 🟡 | | C++ LLVM backend generates `.o` for core arithmetic/functions |
| **WebAssembly Runtime (WASM)** | ✅ | | | Pyodide in-browser runtime for web playground |
| **Standalone Executable Packager** | ✅ | | | `dhicode build` generates standalone `.pyz` & `.bat` |
| **Async / Await Event Loop** | | | ❌ | Non-blocking asynchronous I/O |
| **Multi-threading / Worker Tasks** | | | ❌ | Concurrency, thread pools, channels |

---

## 6. Developer Tooling & Ecosystem

| Feature | Existing | Partial | Missing | Target |
| :--- | :---: | :---: | :---: | :--- |
| **CLI Runner (`dhicode run`)** | ✅ | | | Command-line file execution |
| **Interactive REPL (`dhicode repl`)** | ✅ | | | Interactive Dhivehi shell with UTF-8 support |
| **Code Formatter (`dhicode fmt`)** | ✅ | | | Canonical 4-space indentation and spacing |
| **Language Server Protocol (`dhicode lsp`)**| ✅ | | | Diagnostics, hover docs, completions, format-on-save |
| **VS Code Extension** | ✅ | | | Syntax highlighting, snippets, hover, formatter, runner |
| **Package Manager (`dhpm`)** | | | ❌ | Dependency management, `dhicode.toml` manifest |
| **Interactive Web Playground** | ✅ | | | Live in-browser dual-layer syntax-highlighted IDE |
| **Dhivehi Coding Academy** | ✅ | | | 8-lesson interactive self-grading curriculum |
| **Test Runner (`dhicode test`)** | | 🟡 | | Python unittest runner exists; target native `dhicode test` CLI |
| **Linter (`dhicode lint`)** | | | ❌ | Static analysis for unused variables and code smells |
| **Documentation Generator (`dhicode doc`)**| | | ❌ | Automated HTML/Markdown doc generation from source |
