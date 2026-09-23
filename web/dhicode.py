#!/usr/bin/env python3
# dhicode.py - Command-line interface and REPL for DhiCode
import sys
import os

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

from lexer import Lexer
from parser import Parser
from evaluator import Evaluator, Environment, DhicodeError, DhicodeFunction, NULL_OBJ
from ast_nodes import CallExpression, Identifier

def format_diagnostic(source: str, filename: str, error: DhicodeError) -> str:
    lines = source.splitlines()
    res = [
        "==================== [ކުށުގެ ތަފްޞީލް / Error Diagnostic] ====================",
        f"ފައިލް: {filename}" + (f" | ލައިން: {error.line} | ކޮލަމް: {error.column}" if error.line > 0 else "")
    ]

    if 1 <= error.line <= len(lines):
        err_line = lines[error.line - 1]
        res.append("")
        res.append(f"  {error.line:>4} | {err_line}")
        col_pad = " " * max(0, error.column - 1) if error.column > 0 else ""
        res.append(f"       | {col_pad}^^^")
        res.append("")

    res.append(f"ކުށް: {error.message}")
    res.append("========================================================================")
    return "\n".join(res)

def run_source(source: str, filename: str = "<stdin>", env: Environment = None, base_path: str = ".") -> int:
    if env is None:
        env = Environment()

    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()

    if parser.errors:
        print("--- Parser Errors (ޕާސަރ ކުށްތައް) ---", file=sys.stderr)
        for err in parser.errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    evaluator = Evaluator(base_path=base_path)
    result = evaluator.eval(program, env)

    if isinstance(result, DhicodeError):
        print(format_diagnostic(source, filename, result), file=sys.stderr)
        return 1

    # If an entry function 'މައި' (main) was defined, execute it
    main_fn = env.get("މައި")
    if isinstance(main_fn, DhicodeFunction):
        main_res = evaluator.eval(CallExpression(None, Identifier(None, "މައި"), []), env)
        if isinstance(main_res, DhicodeError):
            print(format_diagnostic(source, filename, main_res), file=sys.stderr)
            return 1

    return 0

def run_file(filepath: str) -> int:
    if not os.path.exists(filepath):
        print(f"Error: File not found: '{filepath}'", file=sys.stderr)
        return 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
        return 1

    base_dir = os.path.dirname(os.path.abspath(filepath))
    return run_source(source, filename=os.path.basename(filepath), base_path=base_dir)

def start_repl():
    print("========================================")
    print(" DhiCode (ދިވެހި ކޯޑު) REPL v0.3.0")
    print(" Type Dhivehi code or 'exit' / 'ހުއްޓާ' to quit.")
    print("========================================")

    env = Environment()
    evaluator = Evaluator(base_path=".")

    while True:
        try:
            line = input("ދިވެހި> ")
        except (EOFError, KeyboardInterrupt):
            print("\nބަޔާން ނިމުނީ.")
            break

        line = line.strip()
        if not line:
            continue
        if line in ("exit", "quit", "ހުއްޓާ"):
            print("ބަޔާން ނިމުނީ.")
            break

        lexer = Lexer(line)
        parser = Parser(lexer)
        program = parser.parse_program()

        if parser.errors:
            for err in parser.errors:
                print(f"  {err}", file=sys.stderr)
            continue

        result = evaluator.eval(program, env)
        if isinstance(result, DhicodeError):
            print(format_diagnostic(line, "<repl>", result), file=sys.stderr)
        elif result and result is not NULL_OBJ:
            print(result.inspect())

def main():
    if len(sys.argv) < 2:
        start_repl()
        return

    cmd = sys.argv[1]
    if cmd in ("-h", "--help", "help"):
        print("Usage:")
        print("  python dhicode.py run <file.dhi>    Run a DhiCode source file")
        print("  python dhicode.py repl              Start interactive REPL")
        print("  python dhicode.py                   Start interactive REPL")
        return

    if cmd == "repl":
        start_repl()
    elif cmd == "run":
        if len(sys.argv) < 3:
            print("Error: Please provide a .dhi file to run.", file=sys.stderr)
            sys.exit(1)
        sys.exit(run_file(sys.argv[2]))
    else:
        if os.path.exists(cmd):
            sys.exit(run_file(cmd))
        else:
            print(f"Unknown command or file: '{cmd}'", file=sys.stderr)
            print("Run 'python dhicode.py --help' for usage.")
            sys.exit(1)

if __name__ == "__main__":
    main()
