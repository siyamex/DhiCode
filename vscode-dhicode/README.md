# DhiCode for Visual Studio Code

Language support, syntax highlighting, and snippets for **DhiCode** (ދިވެހި ކޯޑު), the programming language designed for native Dhivehi (Thaana) speakers.

---

## Features

- **Syntax Highlighting**:
  - Full support for Thaana script Unicode ranges (`\u0780`–`\u07BF`) including letters and *fili* vowel diacritics.
  - Highlights control keywords: `ނަމަ` (if), `ނޫންނަމަ` (else), `ހިނދު` (while), `ނިމުނީ` (end), `ފޮނުވާ` (return).
  - Highlights declaration keywords: `ކަނޑައަޅާ` / `ބަހައްޓާ` (let), `ވަޒީފާ` / `ފަންކް` (function).
  - Highlights built-ins & I/O: `ދައްކާ` / `ލިޔޭ` (print/write), `މައި` (main).
  - Highlights booleans (`އާން` / `ނޫން`) and logical operators (`އަދި` / `ނުވަތަ`).
  - Numbers, double-quoted strings, comments (`//` and `/* ... */`), and operators (`+`, `-`, `*`, `/`, `>`, `<`, `==`, `!=`).
- **Language Configuration**:
  - Auto-closing quotes, braces (`{ }`), brackets (`[ ]`), and parentheses (`( )`).
  - Code folding for `ނަމަ ... ނިމުނީ`, `ވަޒީފާ ... ނިމުނީ`, `ހިނދު ... ނިމުނީ`, and `{ ... }`.
  - Automatic indentation rules.
- **Snippets**:
  - `vazeefaa`: Function declaration with `ވަޒީފާ`
  - `fank`: C++ style function declaration with `ފަންކް`
  - `kanda`: Variable declaration with `ކަނޑައަޅާ`
  - `bahattaa`: Variable declaration with `ބަހައްޓާ`
  - `nama`: If statement
  - `namanoon`: If-Else statement
  - `hindhu`: While loop
  - `dhakkaa`: Print statement
  - `liye`: Write statement
  - `fonuvaa`: Return statement

---

## Installation

### Option 1: Direct Copy into VS Code Extensions (Easiest)

#### Windows (PowerShell):
```powershell
Copy-Item -Recurse -Force "d:\projects\DhiCode-main\vscode-dhicode" "$env:USERPROFILE\.vscode\extensions\vscode-dhicode"
```

#### macOS / Linux:
```bash
cp -r /path/to/DhiCode-main/vscode-dhicode ~/.vscode/extensions/vscode-dhicode
```

Then reload or restart VS Code. Open any `.dhi` file (such as `main.dhi` or `example.dhi`) and the language mode will automatically switch to **DhiCode**.

---

### Option 2: Test via Extension Development Host

1. Open the `vscode-dhicode` folder in VS Code:
   ```bash
   code d:\projects\DhiCode-main\vscode-dhicode
   ```
2. Press `F5` (or run **Debug: Start Debugging**).
3. A new "Extension Development Host" window will open.
4. Open your `.dhi` files in that window to test syntax highlighting and snippets immediately.

---

### Option 3: Package into a `.vsix` File

To create a shareable `.vsix` installer:

```bash
cd d:\projects\DhiCode-main\vscode-dhicode
npx @vscode/vsce package
```

Then install the generated `dhicode-0.1.0.vsix` via:
- VS Code Extensions view (`Ctrl+Shift+X` / `Cmd+Shift+X`) -> `...` menu -> **Install from VSIX...**
- Or command line: `code --install-extension dhicode-0.1.0.vsix`
