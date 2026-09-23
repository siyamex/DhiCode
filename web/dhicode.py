#!/usr/bin/env python3
# dhicode.py - Command-line interface, REPL, Packager, Formatter & LSP Launcher for DhiCode
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

# =============================================================================
# Standalone Binary & Package Builder [Option 3]
# =============================================================================
def build_standalone(source_file: str, output_path: str = None) -> int:
    import zipapp
    import tempfile
    import shutil

    if not os.path.exists(source_file):
        print(f"Error: Source file not found: '{source_file}'", file=sys.stderr)
        return 1

    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            user_source = f.read()
    except Exception as e:
        print(f"Error reading '{source_file}': {e}", file=sys.stderr)
        return 1

    base_name = os.path.splitext(os.path.basename(source_file))[0]
    if not output_path:
        output_path = f"{base_name}.pyz"

    if not output_path.endswith('.pyz'):
        pyz_target = f"{output_path}.pyz"
    else:
        pyz_target = output_path

    # Ensure target output directory exists
    out_dir = os.path.dirname(pyz_target)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        root_dir = os.path.dirname(os.path.abspath(__file__))

        # Core runtime files to bundle
        runtime_files = [
            "token_types.py", "lexer.py", "ast_nodes.py",
            "parser.py", "stdlib.py", "evaluator.py", "dhicode.py"
        ]

        for fname in runtime_files:
            src = os.path.join(root_dir, fname)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(temp_dir, fname))

        # Embedded standalone __main__.py
        main_py = os.path.join(temp_dir, "__main__.py")
        with open(main_py, 'w', encoding='utf-8') as f:
            f.write(f'''#!/usr/bin/env python3
# Standalone DhiCode Executable Application
# Generated from {os.path.basename(source_file)}
import sys
import os

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

from dhicode import run_source

SOURCE = {repr(user_source)}

def main():
    sys.exit(run_source(SOURCE, filename="{os.path.basename(source_file)}"))

if __name__ == "__main__":
    main()
''')

        # Package into standalone zipapp (since __main__.py is present, main arg is not needed)
        zipapp.create_archive(
            temp_dir,
            target=pyz_target,
            interpreter="/usr/bin/env python3"
        )

    # Windows batch launcher
    cmd_path = os.path.splitext(pyz_target)[0] + ".bat"
    if sys.platform == "win32":
        with open(cmd_path, 'w', encoding='utf-8') as f:
            f.write(f'@echo off\npython "%~dp0{os.path.basename(pyz_target)}" %*\n')

    size_kb = round(os.path.getsize(pyz_target) / 1024, 1)
    print(f"✅ Standalone executable built successfully!")
    print(f"📦 Archive: {pyz_target} ({size_kb} KB)")
    if sys.platform == "win32":
        print(f"⚡ Windows Launcher: {cmd_path}")
    print(f"🚀 To run: python {pyz_target}")
    return 0

def main():
    if len(sys.argv) < 2:
        start_repl()
        return

    cmd = sys.argv[1]
    if cmd in ("-h", "--help", "help"):
        print("DhiCode (ދިވެހި ކޯޑު) CLI - Modern Dhivehi Programming Language")
        print("\nCommands:")
        print("  python dhicode.py run <file.dhi>          Run a DhiCode source file")
        print("  python dhicode.py build <file.dhi> [-o]   Build standalone executable package")
        print("  python dhicode.py fmt <file.dhi> [-w|-c]  Format Dhivehi source code")
        print("  python dhicode.py lsp                     Launch Language Server Protocol (LSP)")
        print("  python dhicode.py repl                    Start interactive REPL")
        print("  python dhicode.py                         Start interactive REPL")
        return

    if cmd == "repl":
        start_repl()

    elif cmd == "run":
        if len(sys.argv) < 3:
            print("Error: Please provide a .dhi file to run.", file=sys.stderr)
            sys.exit(1)
        sys.exit(run_file(sys.argv[2]))

    elif cmd == "build":
        if len(sys.argv) < 3:
            print("Error: Please provide a .dhi file to build.", file=sys.stderr)
            print("Usage: python dhicode.py build <file.dhi> [-o output_name]")
            sys.exit(1)
        target_file = sys.argv[2]
        output = None
        if len(sys.argv) > 3:
            if sys.argv[3] in ("-o", "--output") and len(sys.argv) > 4:
                output = sys.argv[4]
            else:
                output = sys.argv[3]
        sys.exit(build_standalone(target_file, output_path=output))

    elif cmd == "fmt":
        if len(sys.argv) < 3:
            print("Error: Please provide a .dhi file to format.", file=sys.stderr)
            print("Usage: python dhicode.py fmt <file.dhi> [--write] [--check]")
            sys.exit(1)
        import formatter
        target_file = sys.argv[2]
        is_write = "--write" in sys.argv or "-w" in sys.argv
        is_check = "--check" in sys.argv or "-c" in sys.argv
        sys.exit(formatter.format_file(target_file, write=is_write, check=is_check))

    elif cmd == "lsp":
        from lsp_server import DhiCodeLspServer
        server = DhiCodeLspServer()
        server.run()

    else:
        if os.path.exists(cmd):
            sys.exit(run_file(cmd))
        else:
            print(f"Unknown command or file: '{cmd}'", file=sys.stderr)
            print("Run 'python dhicode.py --help' for usage.")
            sys.exit(1)

if __name__ == "__main__":
    main()
