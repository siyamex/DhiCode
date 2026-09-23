# formatter.py - Canonical Code Formatter for DhiCode
import sys
import os
import re

BLOCK_OPENERS = {
    "ވަޒީފާ", "ފަންކް", "ނަމަ", "ހިނދު", "ކޮންމެ", "މަސައްކަތްކުރޭ"
}

BLOCK_MIDDLES = {
    "ނޫންނަމަ", "ކުށެއް_ފެނިއްޖެނަމަ"
}

BLOCK_CLOSERS = {
    "ނިމުނީ"
}

def format_line_spacing(line: str) -> str:
    """Format spaces around operators and commas outside of string literals."""
    if not line.strip() or line.strip().startswith("//"):
        return line.strip()

    # Preserve strings
    parts = []
    in_string = False
    quote_char = None
    cur = []

    i = 0
    while i < len(line):
        ch = line[i]
        if not in_string:
            if ch in ('"', "'"):
                if cur:
                    parts.append(('code', "".join(cur)))
                    cur = []
                in_string = True
                quote_char = ch
                cur.append(ch)
            elif ch == '/' and i + 1 < len(line) and line[i+1] == '/':
                # Rest is comment
                if cur:
                    parts.append(('code', "".join(cur)))
                    cur = []
                parts.append(('comment', line[i:]))
                break
            else:
                cur.append(ch)
        else:
            cur.append(ch)
            if ch == quote_char and (i == 0 or line[i-1] != '\\'):
                parts.append(('string', "".join(cur)))
                cur = []
                in_string = False
                quote_char = None
        i += 1

    if cur:
        parts.append(('string' if in_string else 'code', "".join(cur)))

    # Process code parts
    result = []
    for kind, val in parts:
        if kind == 'code':
            # Space out binary operators
            # Operators: ==, !=, <=, >=, =, +, -, *, /, %
            s = val
            s = re.sub(r'\s*([=+\-*/%<>!]=)\s*', r' \1 ', s)
            s = re.sub(r'(?<![=+\-*/%<>!])\s*([=+\-*/%<>])\s*(?![=+\-*/%<>!])', r' \1 ', s)
            # Normalize commas
            s = re.sub(r'\s*,\s*', r', ', s)
            # Remove multiple spaces
            s = re.sub(r'[ \t]+', ' ', s)
            # Fix parenthesis spacing: f( a ) -> f(a)
            s = re.sub(r'\(\s+', '(', s)
            s = re.sub(r'\s+\)', ')', s)
            s = re.sub(r'\[\s+', '[', s)
            s = re.sub(r'\s+\]', ']', s)
            result.append(s)
        else:
            result.append(val)

    return "".join(result).strip()

def format_code(source: str) -> str:
    """Format full DhiCode source with canonical 4-space indentation and clean spacing."""
    lines = source.splitlines()
    formatted_lines = []
    indent_level = 0
    blank_line_count = 0

    for raw_line in lines:
        stripped = raw_line.strip()

        # Handle empty lines
        if not stripped:
            blank_line_count += 1
            if blank_line_count <= 1 and formatted_lines:
                formatted_lines.append("")
            continue

        blank_line_count = 0

        # Check first token for block nesting
        first_word = stripped.split()[0] if stripped.split() else ""

        is_closer = first_word in BLOCK_CLOSERS
        is_middle = first_word in BLOCK_MIDDLES
        is_opener = first_word in BLOCK_OPENERS

        # De-indent closers and middle keywords
        current_indent = indent_level
        if is_closer or is_middle:
            current_indent = max(0, indent_level - 1)

        formatted_content = format_line_spacing(stripped)
        indent_str = "    " * current_indent
        formatted_lines.append(f"{indent_str}{formatted_content}")

        # Adjust indent level for subsequent lines
        if is_opener:
            indent_level += 1
        elif is_closer:
            indent_level = max(0, indent_level - 1)
        elif is_middle:
            # Middle stays at same indent for its block
            pass

    return "\n".join(formatted_lines).rstrip() + "\n"

def format_file(filepath: str, write: bool = False, check: bool = False) -> int:
    if not os.path.exists(filepath):
        print(f"Error: File not found: '{filepath}'", file=sys.stderr)
        return 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
        return 1

    formatted = format_code(original)

    if check:
        if original != formatted:
            print(f"Would reformat: {filepath}")
            return 1
        print(f"Already formatted: {filepath}")
        return 0

    if write:
        if original != formatted:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(formatted)
                print(f"Formatted: {filepath}")
            except Exception as e:
                print(f"Error writing to '{filepath}': {e}", file=sys.stderr)
                return 1
        else:
            print(f"Unchanged: {filepath}")
        return 0

    # Print to stdout
    sys.stdout.write(formatted)
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python formatter.py <file.dhi> [--write] [--check]")
        sys.exit(1)

    target = sys.argv[1]
    is_write = "--write" in sys.argv or "-w" in sys.argv
    is_check = "--check" in sys.argv or "-c" in sys.argv
    sys.exit(format_file(target, write=is_write, check=is_check))
