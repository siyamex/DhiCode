<div align="center">

# 🇲🇻 DhiCode (ދިވެހި ކޯޑު)

**A modern, general-purpose programming language designed around the Dhivehi language and Thaana script.**

[![Version: 0.4.0](https://img.shields.io/badge/Version-0.4.0-0284c7.svg)](https://github.com/siyamex/DhiCode/releases)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Unit Tests](https://img.shields.io/badge/Tests-76%2F76_Passing_(100%25)-059669.svg)]()
[![Web Playground](https://img.shields.io/badge/Playground-Live_WebAssembly-7c3aed.svg)](https://siyamex.github.io/DhiCode/)
[![Academy](https://img.shields.io/badge/Academy-Interactive_Course-d97706.svg)](https://siyamex.github.io/DhiCode/tutorial.html)
[![VS Code Extension](https://img.shields.io/badge/VS_Code-Supported-007ACC.svg?logo=visual-studio-code&logoColor=white)](vscode-dhicode/)

<p align="center">
  <a href="https://siyamex.github.io/DhiCode/">🌐 Live Web Playground</a> •
  <a href="https://siyamex.github.io/DhiCode/tutorial.html">🎓 Interactive Academy</a> •
  <a href="#-quickstart">🚀 Quickstart</a> •
  <a href="#-features">✨ Features</a> •
  <a href="#-language-tour">📖 Language Tour</a> •
  <a href="#-standard-library">📚 Standard Library</a> •
  <a href="#-keywords-reference">📑 Keywords Reference</a> •
  <a href="#-tooling--developer-ecosystem">🛠️ Tooling</a>
</p>

---

</div>

## 🌟 Overview

**DhiCode** is a production-capable, dual-syntax programming language that bridges **native Dhivehi (Thaana script)** and **modern English technical keywords**. It is designed for general-purpose application development, web APIs, systems scripting, data science, and Maldivian cultural computing.

Whether you write in authentic Thaana or standard English keywords, DhiCode executes natively with full Unicode fidelity:

```dhicode
// 1. Pure Dhivehi Syntax (ދިވެހި ބަސް)
ގެނޭ "ޑޭޓާބޭސް"
ކަނޑައަޅާ ޑީބީ = ހުޅުވާ(":memory:")
ޑީބީ.ހިންގާ("CREATE TABLE islands (name TEXT, pop INTEGER);")
ޑީބީ.ހިންގާ("INSERT INTO islands VALUES (?, ?);", ["މާލެ", 215000])
ކަނޑައަޅާ ރަށްތައް = ޑީބީ.ހޯދާ("SELECT * FROM islands;")
ދައްކާ "ރަށް:", ރަށްތައް[0].name
```

```dhicode
// 2. Dual English Syntax
import "db";
let db = open(":memory:");
db.execute("CREATE TABLE islands (name TEXT, pop INTEGER);");
db.execute("INSERT INTO islands VALUES (?, ?);", ["Male'", 215000]);
let islands = db.query("SELECT * FROM islands;");
print("Island:", islands[0].name);
```

---

## ✨ Features

- **🇲🇻 Unicode-First & Native Thaana Script**: Native lexing of Thaana letters (`\u0780`–`\u07A5`), *fili* vowel diacritics (`\u07A6`–`\u07B0`), *sukun* (`\u07B1`), and international identifiers.
- **⚡ Dual-Syntax Equality**: Every keyword and stdlib function is symmetrically available in both Dhivehi (`ކަނޑައަޅާ`, `ވަޒީފާ`, `ނަމަ`, `ކްލާސް`) and English (`let`, `fn`, `if`, `class`).
- **🏛️ Modern Object-Oriented Programming (OOP)**: Classes (`class` / `ކްލާސް`), constructors (`constructor` / `ހަދާ_ވަޒީފާ`), instance methods, prototype inheritance (`extends` / `ދަރިކޮޅު`), and `this` / `މި`.
- **🗄️ Embedded SQLite Database Engine**: Pure zero-dependency database abstraction (`db` / `ޑޭޓާބޭސް`) with parameterized queries (`?`), dictionary row mapping, batch inserts, and transaction rollback/commit.
- **🚀 Native HTTP Web Server & Router**: Build high-performance REST APIs directly in DhiCode with `net.serve` / `ސާވަރު`, route dispatchers (`create_router` / `ރައުޓަރ_ހަދާ`), query parameter parsing, and JSON/HTML response builders.
- **🌙 Maldivian Cultural Computing Modules**:
  - **Nakaiy Calendar (`ނަކަތް` / `nakaiy`)**: 27 Maldivian Nakaiy, monsoon classification (Hulhangu / Iruvai), and daily climate traits.
  - **Prayer Times (`ނަމާދު` / `prayer`)**: Exact solar calculations for all Maldivian atolls, next prayer countdown, and Hijri converter.
  - **Thaana Words & Collation (`ތާނަ` / `thaana`)**: Dynamic number-to-Dhivehi words, currency formatting (MVR), and authentic Thaana alphabetical sorting.
- **🔒 Extended Standard Library**: High-speed Cryptography (SHA-256, SHA-512, HMAC, Base64), Unicode-aware Regular Expressions (`regex` / `ރެގެކްސް`), File System (`file` / `ފައިލް`), and Math (`math` / `ހިސާބު`).
- **🎛️ Modern Syntax Primitives**: Arrow functions `(x) => x * 2`, variadic rest parameters `...args`, default parameters, range operator `1..10`, list/dict destructuring, compound assignments (`+=`, `-=`), and null coalescing (`??`).
- **🌐 Interactive Web Playground & Academy**: Runs 100% in-browser via WebAssembly / Pyodide, with syntax highlighting, live execution, and a step-by-step interactive course.
- **🛠️ Production Developer Tooling**: Built-in canonical code formatter (`dhicode fmt`), Language Server Protocol server (`dhicode lsp`), and standalone binary packager (`dhicode build`).

---

## 🚀 Quickstart

### Installation & Requirements

DhiCode requires Python 3.8+ with zero external third-party dependencies:

```bash
git clone https://github.com/siyamex/DhiCode.git
cd DhiCode
```

### 1. Run a DhiCode File
```bash
python dhicode.py run main.dhi
python dhicode.py examples/backend_and_db_demo.dhi
```

### 2. Interactive REPL (ކޯޑު ޝެލް)
Launch the interactive shell with live expression evaluation:
```bash
python dhicode.py repl
```
```text
========================================
 DhiCode (ދިވެހި ކޯޑު) REPL v0.4.0
 Type Dhivehi/English code or 'exit' / 'ހުއްޓާ' to quit.
========================================
ދިވެހި> ކަނޑައަޅާ ރަށްތައް = ["މާލެ", "ހުޅުމާލެ"]
["މާލެ", "ހުޅުމާލެ"]
ދިވެހި> އަޅާ(ރަށްތައް, "ވިލިމާލެ")
["މާލެ", "ހުޅުމާލެ", "ވިލިމާލެ"]
ދިވެހި> 1..5
[1, 2, 3, 4, 5]
```

### 3. Canonical Code Formatter
Format `.dhi` code files to canonical style:
```bash
python dhicode.py fmt main.dhi
python dhicode.py fmt --check main.dhi
```

### 4. Language Server Protocol (LSP)
Run the LSP server for VS Code and other editors:
```bash
python dhicode.py lsp
```

### 5. Run the Automated Test Suite
Run all 76 unit tests covering core syntax, OOP, standard library, database, and web server:
```bash
python -m unittest discover tests
```
```text
............................................................................
----------------------------------------------------------------------
Ran 76 tests in 1.602s

OK
```

---

## 📖 Language Tour

### 1. Variables & Constants (ވެރިއަބަލްތައް)

```dhicode
// Mutable variable
ކަނޑައަޅާ އަގު = 100;
let count = 100;

// Immutable constant
ދާއިމީ ޕައި = 3.14159;
const PI = 3.14159;

// List and Dictionary Destructuring
let [first, second] = ["Male'", "Addu"];
let {name, atoll} = {"name": "Kulhudhuffushi", "atoll": "HDh"};
```

### 2. Functions & Arrow Functions (ފަންކްޝަންތައް)

```dhicode
// Standard function with default parameter
ވަޒީފާ ސަލާމް(ނަން = "ރަޙުމަތްތެރިޔާ")
    އަނބުރާ "އައްސަލާމް ޢަލައިކުމް، " + ނަން
ނިމުނީ

// Variadic rest arguments (...args)
fn sum(...numbers) {
    let total = 0;
    for n in numbers {
        total += n;
    }
    return total;
}

// Arrow function
let double = (x) => x * 2;
print(double(21)); // 42
```

### 3. Object-Oriented Classes & Inheritance (ކްލާސްތައް)

```dhicode
ކްލާސް އިންސާނާ
    ވަޒީފާ ހަދާ_ވަޒީފާ(ނަން, އުމުރު = 18)
        މި.ނަން = ނަން
        މި.އުމުރު = އުމުރު
    ނިމުނީ

    ވަޒީފާ ތަޢާރަފް()
        އަނބުރާ "އަހަންނަކީ " + މި.ނަން + "، އުމުރަކީ " + މި.އުމުރު
    ނިމުނީ
ނިމުނީ

// Inheritance (ދަރިކޮޅު)
ކްލާސް ޑޮކްޓަރު ދަރިކޮޅު އިންސާނާ
    ވަޒީފާ ހަދާ_ވަޒީފާ(ނަން, އުމުރު, ހޮސްޕިޓަލް)
        މި.ނަން = ނަން
        މި.އުމުރު = އުމުރު
        މި.ހޮސްޕިޓަލް = ހޮސްޕިޓަލް
    ނިމުނީ

    ވަޒީފާ ފަރުވާ_ދީ(ބަލިމީހާ)
        އަނބުރާ "ޑރ. " + މި.ނަން + " ފަރުވާ ދެނީ " + ބަލިމީހާ + " އަށް"
    ނިމުނީ
ނިމުނީ

ކަނޑައަޅާ ޑރ = ޑޮކްޓަރު("އަޙްމަދު", 35, "އައިޖީއެމްއެޗް");
ދައްކާ ޑރ.ތަޢާރަފް();
ދައްކާ ޑރ.ފަރުވާ_ދީ("ޢަލީ");
```

### 4. Control Flow & Loops (ޝަރުޠުތަކާއި ލޫޕްތައް)

```dhicode
// If - Else
ނަމަ އުމުރު >= 18
    ދައްކާ "ބޮޑު މީހެއް"
ނޫންނަމަ
    ދައްކާ "ކުޑަކުއްޖެއް"
ނިމުނީ

// For-in loop with range operator (..)
for i in 1..5 {
    print("Count:", i);
}

// For-each over lists and dicts
ކަނޑައަޅާ ރަށްތައް = ["މާލެ", "ހުޅުމާލެ", "ވިލިމާލެ"];
ކޮންމެ ރަށް ތެރޭގައި ރަށްތައް
    ދައްކާ "• " + ރަށް
ނިމުނީ
```

### 5. Embedded SQLite Database (ޑޭޓާބޭސް)

```dhicode
import "db";

// Open in-memory or file database
let conn = open("app.db");

conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, role TEXT);");
conn.execute("INSERT INTO users (name, role) VALUES (?, ?);", ["Aishath", "Engineer"]);

// Query with parameter binding
let rows = conn.query("SELECT * FROM users WHERE role = ?;", ["Engineer"]);
for user in rows {
    print("User:", user.name, "| Role:", user.role);
}

// Transactions with rollback & commit
conn.begin();
conn.execute("UPDATE users SET role = 'Lead' WHERE id = 1;");
conn.commit();

conn.close();
```

### 6. Native HTTP Web Server & Router (ސާވަރު)

```dhicode
import "net";

let router = create_router();

router.get("/api/greet", fn(req) {
    let name = req.query ? req.query["name"] : "World";
    return response_json({
        "status": "success",
        "message": "Hello, " + name + "!",
        "timestamp": 2026
    });
});

router.post("/api/echo", fn(req) {
    return response_json({"received": req.json}, 201);
});

// Run server in background daemon thread
let server = serve(8080, router, {"background": true});
print("Server listening on port:", server.port);

// Call with native HTTP client
let res = get("http://127.0.0.1:8080/api/greet?name=Ali");
print("Response:", res.body);

server.close();
```

### 7. Maldivian Cultural Computing (ދިވެހި ޘަޤާފީ މޮޑިއުލްތައް)

```dhicode
// 1. Nakaiy Calendar (ނަކަތް)
ގެނޭ "ނަކަތް";
ކަނޑައަޅާ މިއަދު = މިއަދުގެ_ނަކަތް();
ދައްކާ "މިއަދުގެ ނަކަތް:", މިއަދު["ނަން"], "| މޫސުން:", މިއަދު["މޫސުން"];

// 2. Solar Prayer Times (ނަމާދު)
ގެނޭ "ނަމާދު";
ކަނޑައަޅާ ވަގުތު = މިއަދުގެ_ވަގުތު("މާލެ");
ދައްކާ "މަޣްރިބް ވަގުތު:", ވަގުތު["މަޣްރިބް"];

// 3. Thaana Number-to-Words & Collation (ތާނަ)
ގެނޭ "ތާނަ_ހިސާބު";
ދައްކާ އަދަދު_ބަހަށް(125); // "ސަތޭކަ ފަންސަވީސް"

ކަނޑައަޅާ ތަރުތީބު = ތާނަ_ތަރުތީބު(["ރަށް", "ހަނދު", "ނަން", "ށީ"]);
ދައްކާ ތަރުތީބު; // ["ހަނދު", "ށީ", "ނަން", "ރަށް"]
```

---

## 📚 Standard Library

| Module (Dhivehi) | Module (English) | Description | Key Functions / APIs |
| :--- | :--- | :--- | :--- |
| **`ޑޭޓާބޭސް`** | **`db`** / **`sqlite`** | Embedded SQLite Database Engine | `open`, `execute`, `query`, `query_one`, `execute_many`, `begin`, `commit`, `rollback`, `tables`, `close` |
| **`ނެޓްވޯކް`** | **`net`** / **`http`** | HTTP Server & Web Client | `serve`, `create_router`, `response_json`, `response_html`, `get`, `post`, `put`, `delete`, `parse_json`, `stringify_json` |
| **`ނަކަތް`** | **`nakaiy`** | Maldivian Nakaiy Calendar | `މިއަދުގެ_ނަކަތް()`, `ނަކަތް_ހޯދާ(މަސް, ދުވަސް)` |
| **`ނަމާދު`** | **`prayer`** | Solar Prayer Times for all Atolls | `މިއަދުގެ_ވަގުތު(ރަށް)`, `ދެން_އޮތް_ނަމާދު(ރަށް)`, `ހިޖުރީ_ތާރީޚް()` |
| **`ތާނަ_ހިސާބު`** | **`thaana`** | Thaana Words & Collation | `އަދަދު_ބަހަށް(n)`, `ފައިސާ_ބަހަށް(n)`, `ތާނަ_ތަރުތީބު(list)`, `ފިލި_ފޮހޭ(text)` |
| **`ކްރިޕްޓޯ`** | **`crypto`** | Cryptography & Hashing | `sha256`, `sha512`, `md5`, `hmac_sha256`, `base64_encode`, `base64_decode`, `random_token` |
| **`ރެގެކްސް`** | **`regex`** | Regular Expressions | `match`, `search`, `replace`, `split`, `ދިމާވޭތޯ`, `ހޯދާ`, `ބަދަލުކުރޭ` |
| **`ފައިލް`** | **`file`** / **`fs`** | File System & Directories | `read`, `write`, `append`, `exists`, `delete`, `mkdir`, `list_dir`, `size` |
| **`ވަގުތު`** | **`time`** | Date, Time & Sleep | `now`, `time`, `sleep`, `format`, `parse` |
| **`ހިސާބު`** | **`math`** | Mathematical Operations | `sqrt`, `pow`, `round`, `floor`, `ceil`, `min`, `max`, `random`, `abs`, `sin`, `cos`, `tan`, `log`, `pi`, `e` |
| **`ނިޒާމު`** | **`os`** / **`sys`** | System Environment & CLI | `args`, `env`, `platform`, `cwd`, `exit` |

---

## 📑 Keywords Reference

| Thaana Keyword | English Keyword | Category | Usage / Example |
| :--- | :--- | :--- | :--- |
| `ކަނޑައަޅާ` / `ބަހައްޓާ` | `let` / `var` | Declaration | `ކަނޑައަޅާ ނަން = "ޢަލީ"` |
| `ދާއިމީ` | `const` | Declaration | `ދާއިމީ ޕައި = 3.14159` |
| `ވަޒީފާ` / `ފަންކް` | `fn` / `function` | Functions | `ވަޒީފާ ގުނާ(x) ... ނިމުނީ` |
| `ފޮނުވާ` / `އަނބުރާ` | `return` | Functions | `އަނބުރާ ނަތީޖާ` |
| `ދައްކާ` / `ލިޔޭ` | `print` | I/O | `ދައްކާ "މަރުޙަބާ"` |
| `ނަމަ` | `if` | Control Flow | `ނަމަ x > 0 ... ނިމުނީ` |
| `ނޫންނަމަ` | `else` | Control Flow | `ނޫންނަމަ ... ނިމުނީ` |
| `ހިނދު` | `while` | Loops | `ހިނދު x < 10 ... ނިމުނީ` |
| `ކޮންމެ` | `for` | Loops | `ކޮންމެ އައިޓަމް ތެރޭގައި ލިސްޓު` |
| `ތެރޭގައި` | `in` | Loops | `for item in items` |
| `ނިމުނީ` | `end` | Delimiter | Block termination |
| `ކްލާސް` | `class` | OOP | `ކްލާސް ކާރު ... ނިމުނީ` |
| `ދަރިކޮޅު` | `extends` | OOP | `ކްލާސް ވެހިކަލް ދަރިކޮޅު އުޅަނދު` |
| `މި` | `this` / `self` | OOP | `މި.ނަން = ނަން` |
| `ގެނޭ` | `import` | Modules | `ގެނޭ "ޑޭޓާބޭސް"` |
| `މަސައްކަތްކުރޭ` | `try` | Error Handling | `މަސައްކަތްކުރޭ ... ކުށެއް_ފެނިއްޖެނަމަ` |
| `ކުށެއް_ފެނިއްޖެނަމަ` | `catch` | Error Handling | `ކުށެއް_ފެނިއްޖެނަމަ ކުށް` |
| `އުކާލާ` | `throw` | Error Handling | `އުކާލާ "މައްސަލައެއް"` |
| `އާން` / `ނޫން` | `true` / `false` | Literals | Boolean true and false |
| `ހުސް` / `ބާޠިލް` | `null` / `nil` | Literals | Null reference |

---

## 🛠️ Tooling & Developer Ecosystem

### VS Code Extension
Syntax highlighting, bracket auto-closing, block folding, and Thaana code snippets:
- Directory: [`vscode-dhicode/`](vscode-dhicode/)
- Package and install:
  ```bash
  cd vscode-dhicode
  npm install -g @vscode/vsce
  vsce package
  code --install-extension dhicode-0.3.0.vsix
  ```

### WebAssembly Browser Playground
The entire DhiCode runtime runs inside WebAssembly via Pyodide:
- **Online**: [https://siyamex.github.io/DhiCode/](https://siyamex.github.io/DhiCode/)
- **Academy**: [https://siyamex.github.io/DhiCode/tutorial.html](https://siyamex.github.io/DhiCode/tutorial.html)
- Run locally:
  ```bash
  python -m http.server 8000
  ```
  Open `http://localhost:8000/web/` in your browser.

---

## 📄 License & Community

DhiCode is free, open source, and dedicated to the public domain under the **Creative Commons CC0 1.0 Universal** license. Anyone is free to use, modify, distribute, and build commercial or educational software with DhiCode without restriction.

Made with ❤️ for the Maldives 🇲🇻 by [siyamex](https://github.com/siyamex).
