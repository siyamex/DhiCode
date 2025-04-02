# DhiCode
Dhivehi Programming Language
# DhiCode Interpreter

An experimental interpreter for **DhiCode**, a concept programming language using the Dhivehi (Thaana) script for keywords and identifiers.

## Project Goal

To explore the feasibility and challenges of creating a programming language tailored for native Dhivehi speakers, aiming for readability and educational value.

## Current Status (As of [Date])

*   **Lexer:** Implemented, recognizes basic keywords, Thaana identifiers, numbers, strings, operators (`=`, `+`, `>`), and parentheses/commas for calls.
*   **Parser:** Implemented, builds an Abstract Syntax Tree (AST) for:
    *   Variable assignment (`ކަނޑައަޅާ`)
    *   Basic infix expressions (`+`, `>`)
    *   Function calls (`ދައްކާ(...)`)
*   **Interpreter/Evaluator:** Not yet started.
*   **Supported Syntax:** See `main.dhi` for examples the parser currently handles.

## How to Run (Current State - Parser Test)

1.  Ensure you have Python 3.7+ installed.
2.  Clone this repository: `git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git`
3.  Navigate to the directory: `cd YOUR_REPOSITORY_NAME`
4.  Create/modify the `main.dhi` file with DhiCode syntax supported by the current parser.
5.  Run the parser test: `python parser.py`
6.  Observe the output for Parser Errors and the generated AST structure.

## Next Steps

*   Implement the Evaluator/Interpreter to actually execute the AST.
*   Add parsing support for control flow (`ނަމަ`, `ނޫންނަމަ`, `ހިނދު`).
*   Add parsing support for function definitions (`ވަޒީފާ`).
*   Expand operator support.
*   Improve error handling and reporting.

## Challenges

*   Handling Right-to-Left (RTL) Thaana script in tooling (editor, terminal).
*   Unicode handling in lexing/parsing.
*   Choosing natural and unambiguous Dhivehi keywords for programming concepts.

## Contributing

(Optional: Add guidelines later if you want contributions)
