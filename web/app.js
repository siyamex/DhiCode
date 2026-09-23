// web/app.js - DhiCode Live Web Playground Controller with Real-Time Syntax Highlighting
let pyodide = null;
let isReady = false;

// DOM Elements
const editor = document.getElementById("code-editor");
const highlight = document.getElementById("code-highlight");
const highlightContent = document.getElementById("code-highlight-content");
const terminal = document.getElementById("terminal-output");
const statusIndicator = document.getElementById("runtime-status");
const btnRun = document.getElementById("btn-run");
const btnClear = document.getElementById("btn-clear");
const btnDir = document.getElementById("btn-dir");
const btnTheme = document.getElementById("btn-theme");
const themeIcon = document.getElementById("theme-icon");
const btnCopyCmd = document.getElementById("btn-copy-cmd");
const btnCopyCode = document.getElementById("btn-copy-code");
const execTimeBadge = document.getElementById("exec-time");
const exampleTabs = document.querySelectorAll("#example-tabs .ide-tab");

// =============================================================================
// 1. Theme Management (Light Theme Default + Dark Mode Switcher)
// =============================================================================
function initTheme() {
  const savedTheme = localStorage.getItem("dhicode-theme") || "light";
  applyTheme(savedTheme);
}

function applyTheme(theme) {
  if (theme === "dark") {
    document.documentElement.setAttribute("data-theme", "dark");
    if (themeIcon) themeIcon.textContent = "☀️";
    if (btnTheme) btnTheme.setAttribute("title", "އަލި ތީމަށް ބަދަލުކުރޭ (Switch to Light)");
  } else {
    document.documentElement.removeAttribute("data-theme");
    if (themeIcon) themeIcon.textContent = "🌙";
    if (btnTheme) btnTheme.setAttribute("title", "އަނދިރި ތީމަށް ބަދަލުކުރޭ (Switch to Dark)");
  }
  localStorage.setItem("dhicode-theme", theme);
}

if (btnTheme) {
  btnTheme.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    const nextTheme = currentTheme === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
  });
}

// =============================================================================
// 2. Syntax Highlighting Engine for DhiCode (Thaana & English)
// =============================================================================
const DHI_KEYWORDS = new Set([
  // Core control & declaration keywords (Thaana)
  "ކަނޑައަޅާ", "ބަހައްޓާ", "ދާއިމީ", "ވަޒީފާ", "ފަންކް", "ފޮނުވާ", "އަނބުރާ", "ދައްކާ", "ލިޔޭ",
  "ނަމަ", "ނޫންނަމަ", "ހިނދު", "ނިމުނީ", "ކޮންމެ", "ތެރޭގައި", "ގެނޭ",
  "މަސައްކަތްކުރޭ", "ކުށެއް_ފެނިއްޖެނަމަ", "އުކާލާ", "ހުއްޓާ", "ކުރިއަށް",
  "ކްލާސް", "ދަރިކޮޅު", "މި",
  // English keywords
  "let", "var", "const", "fn", "func", "function", "return", "print",
  "if", "else", "while", "end", "for", "in", "import", "try", "catch", "throw", "and", "or", "not",
  "class", "extends", "this", "self"
]);

const DHI_BOOLEANS = new Set([
  "އާން", "ނޫން", "ބާޠިލް", "ހުސް", "true", "false", "null", "nil"
]);

const DHI_BUILTINS = new Set([
  // Standard library functions & built-in tags
  "ދިގުމިން", "ބާވަތް", "އަޅާ", "ނަގާ", "ތަޅުދަނޑިތައް", "އަގުތައް", "އަހާ",
  "ޖަޒުރު", "ބާރު", "ކައިރި", "ތިރި", "މަތި", "ޕައި", "އިއްތިފާޤު",
  "ހުޅުވާ", "ގުޅާ", "ސާވަރު", "ރައުޓަރ_ހަދާ", "ރައުޓަރ", "ޖޭސަން_ޖަވާބު", "އެޗްޓީއެމްއެލް_ޖަވާބު", "ލިޔުން_ޖަވާބު",
  "މިއަދުގެ_ނަކަތް", "ނަކަތް_ހޯދާ", "މިއަދުގެ_ވަގުތު", "ދެން_އޮތް_ނަމާދު", "އަދަދު_ބަހަށް", "ތާނަ_ތަރުތީބު",
  "ވަކިކުރޭ", "ގުޅުވާ", "ބަދަލު", "ތެދު_އަދަދު", "ހުސްޖާގަ_ފޮހޭ", "ކުޑަކުރޭ", "ބޮޑުކުރޭ",
  "ޝާ256", "ބޭސް64_އެންކޯޑު", "ބޭސް64_ޑީކޯޑު", "ދިމާވޭތޯ",
  // English aliases
  "input", "len", "type", "append", "push", "pop", "keys", "values",
  "open", "serve", "create_router", "response_json", "response_html", "response_text",
  "sha256", "base64_encode", "base64_decode", "match", "replace", "search"
]);

// Tokenizer regular expression
const TOKEN_REGEX = /(\/\/[^\n]*|\/\*[\s\S]*?\*\/)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([\u0780-\u07BFa-zA-Z_][\u0780-\u07BFa-zA-Z0-9_]*)|(\*\*|\?\?|\+=|-=|\*=|\/=|%=|<<|>>|==|!=|<=|>=|&&|\|\||[=+\-*/%!<>&|^~])|([()[\]{},;:])/gu;

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function highlightDhiCode(code) {
  if (!code) return "";
  let lastIndex = 0;
  let out = "";
  let match;
  TOKEN_REGEX.lastIndex = 0;

  while ((match = TOKEN_REGEX.exec(code)) !== null) {
    const index = match.index;
    if (index > lastIndex) {
      out += escapeHtml(code.slice(lastIndex, index));
    }

    const [full, comment, str, num, ident, op, punct] = match;

    if (comment) {
      out += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
    } else if (str) {
      out += `<span class="tok-string">${escapeHtml(str)}</span>`;
    } else if (num) {
      out += `<span class="tok-number">${escapeHtml(num)}</span>`;
    } else if (ident) {
      if (DHI_KEYWORDS.has(ident)) {
        out += `<span class="tok-keyword">${escapeHtml(ident)}</span>`;
      } else if (DHI_BOOLEANS.has(ident)) {
        out += `<span class="tok-boolean">${escapeHtml(ident)}</span>`;
      } else if (DHI_BUILTINS.has(ident)) {
        out += `<span class="tok-builtin">${escapeHtml(ident)}</span>`;
      } else {
        out += `<span class="tok-ident">${escapeHtml(ident)}</span>`;
      }
    } else if (op) {
      out += `<span class="tok-operator">${escapeHtml(op)}</span>`;
    } else if (punct) {
      out += `<span class="tok-punct">${escapeHtml(punct)}</span>`;
    }

    lastIndex = TOKEN_REGEX.lastIndex;
  }

  if (lastIndex < code.length) {
    out += escapeHtml(code.slice(lastIndex));
  }

  return out;
}

// Update live highlighter overlay
function updateHighlight() {
  if (!editor || !highlightContent) return;
  const code = editor.value;
  highlightContent.innerHTML = highlightDhiCode(code) + (code.endsWith("\n") ? " " : "");
  syncScroll();
}

// Sync scrolling between editor textarea and highlight pre
function syncScroll() {
  if (!editor || !highlight) return;
  highlight.scrollTop = editor.scrollTop;
  highlight.scrollLeft = editor.scrollLeft;
}

// Wire editor events
if (editor) {
  editor.addEventListener("input", updateHighlight);
  editor.addEventListener("scroll", syncScroll);

  // Tab key indentation (inserts 4 spaces instead of leaving focus)
  editor.addEventListener("keydown", (e) => {
    if (e.key === "Tab") {
      e.preventDefault();
      const start = editor.selectionStart;
      const end = editor.selectionEnd;
      editor.value = editor.value.substring(0, start) + "    " + editor.value.substring(end);
      editor.selectionStart = editor.selectionEnd = start + 4;
      updateHighlight();
    }
  });
}

// Highlight all static <code> elements on page (e.g. in keywords table)
function highlightStaticCodeSnippets() {
  const codeBlocks = document.querySelectorAll(".keywords-table td code, .keywords-table-card code");
  codeBlocks.forEach((block) => {
    const raw = block.textContent;
    block.innerHTML = highlightDhiCode(raw);
  });
}

// Set initial example
if (typeof EXAMPLES !== "undefined" && EXAMPLES.hello) {
  editor.value = EXAMPLES.hello.code;
  updateHighlight();
}

// =============================================================================
// 3. Web Terminal Logging & Management
// =============================================================================
function appendTerminal(text, type = "normal") {
  const line = document.createElement("div");
  line.className = `terminal-line terminal-${type}`;
  line.textContent = text;
  terminal.appendChild(line);
  terminal.scrollTop = terminal.scrollHeight;
}

// Clear terminal
if (btnClear) {
  btnClear.addEventListener("click", () => {
    terminal.innerHTML = '<div class="terminal-dim">(ޓާމިނަލް ފޮހެލެވިއްޖެ)</div>';
    if (execTimeBadge) execTimeBadge.textContent = "";
  });
}

// Direction toggle (RTL / LTR)
let isRtl = true;
if (btnDir) {
  btnDir.addEventListener("click", () => {
    isRtl = !isRtl;
    document.documentElement.dir = isRtl ? "rtl" : "ltr";
    editor.dir = isRtl ? "rtl" : "ltr";
    if (highlight) highlight.dir = isRtl ? "rtl" : "ltr";
    terminal.dir = isRtl ? "rtl" : "ltr";
    btnDir.innerHTML = isRtl ? `<span id="dir-icon">🔀</span> RTL` : `<span id="dir-icon">🔀</span> LTR`;
    syncScroll();
  });
}

// Tab Switching
exampleTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    exampleTabs.forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");

    const key = tab.getAttribute("data-example");
    if (typeof EXAMPLES !== "undefined" && EXAMPLES[key]) {
      editor.value = EXAMPLES[key].code;
      updateHighlight();
    }
  });
});

// Copy quickstart command
if (btnCopyCmd) {
  btnCopyCmd.addEventListener("click", () => {
    const cmd = document.getElementById("quick-cmd").textContent;
    navigator.clipboard.writeText(cmd).then(() => {
      btnCopyCmd.textContent = "✅";
      setTimeout(() => (btnCopyCmd.textContent = "📋"), 2000);
    });
  });
}

// Copy editor code
if (btnCopyCode) {
  btnCopyCode.addEventListener("click", () => {
    navigator.clipboard.writeText(editor.value).then(() => {
      btnCopyCode.textContent = "ކޮޕީ ވެއްޖެ!";
      setTimeout(() => (btnCopyCode.textContent = "ކޮޕީ"), 2000);
    });
  });
}

// =============================================================================
// 4. Pyodide WebAssembly Engine
// =============================================================================
async function initPyodide() {
  try {
    statusIndicator.textContent = "Wasm ލޯޑުވަނީ...";
    statusIndicator.className = "status-badge loading";

    pyodide = await loadPyodide();

    // Fetch and mount DhiCode interpreter modules
    const modules = [
      "token_types.py",
      "lexer.py",
      "ast_nodes.py",
      "parser.py",
      "stdlib.py",
      "evaluator.py",
      "dhicode.py"
    ];

    for (const mod of modules) {
      try {
        let resp = await fetch(`./${mod}`);
        if (!resp.ok) {
          resp = await fetch(`../${mod}`);
        }
        if (resp.ok) {
          const content = await resp.text();
          pyodide.FS.writeFile(mod, content);
        }
      } catch (err) {
        console.warn(`Could not fetch ${mod}:`, err);
      }
    }

    isReady = true;
    statusIndicator.textContent = "● ތައްޔާރު";
    statusIndicator.className = "status-badge ready";

    terminal.innerHTML = "";
    appendTerminal("✅ DhiCode WebAssembly ރަންޓައިމް ކާމިޔާބުކަމާއެކު ތައްޔާރުވެއްޖެ!", "success");
    appendTerminal("ކޯޑު ހިންގުމަށް '▶ ހިންގާ (Run)' ފިއްތަވާ ނުވަތަ Ctrl + Enter ޖައްސަވާ.", "dim");
  } catch (err) {
    statusIndicator.textContent = "● މައްސަލައެއް";
    statusIndicator.className = "status-badge error";
    appendTerminal(`Error initializing Pyodide: ${err}`, "error");
  }
}

// Run Code
async function runDhiCode() {
  if (!isReady || !pyodide) {
    appendTerminal("އަދި ރަންޓައިމް ތައްޔާރެއް ނުވޭ. މަޑުކޮށްލައްވާ...", "error");
    return;
  }

  terminal.innerHTML = "";
  if (execTimeBadge) execTimeBadge.textContent = "ހިނގަނީ...";

  const code = editor.value;
  btnRun.disabled = true;
  btnRun.textContent = "ހިނގަނީ...";

  const t0 = performance.now();

  try {
    pyodide.globals.set("dhi_source", code);

    await pyodide.runPythonAsync(`
import sys
from evaluator import Evaluator, Environment, DhicodeError, DhicodeFunction, NULL_OBJ
from lexer import Lexer
from parser import Parser
from ast_nodes import CallExpression, Identifier

def run_web(source):
    logs = []
    def web_output(val):
        logs.append(("normal", str(val)))

    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()

    if parser.errors:
        for err in parser.errors:
            logs.append(("error", f"ޕާސަރ ކުށް: {err}"))
        return logs

    env = Environment()
    evaluator = Evaluator(output_callback=web_output)
    result = evaluator.eval(program, env)

    if isinstance(result, DhicodeError):
        logs.append(("error", f"ކުށް: {result.message}"))
        return logs

    main_fn = env.get("މައި")
    if isinstance(main_fn, DhicodeFunction):
        main_res = evaluator.eval(CallExpression(None, Identifier(None, "މައި"), []), env)
        if isinstance(main_res, DhicodeError):
            logs.append(("error", f"ކުށް: {main_res.message}"))

    return logs

logs = run_web(dhi_source)
`);

    const t1 = performance.now();
    const duration = Math.round(t1 - t0);
    if (execTimeBadge) {
      execTimeBadge.textContent = `⏱️ ${duration}ms`;
    }

    const logs = pyodide.globals.get("logs").toJs();
    if (!logs || logs.length === 0) {
      appendTerminal("(ނިމުނީ - އެއްވެސް ލިޔުމެއް ނުދައްކާ)", "dim");
    } else {
      for (const [type, msg] of logs) {
        appendTerminal(msg, type);
      }
    }
  } catch (err) {
    appendTerminal(`ރަންޓައިމް ކުށް: ${err}`, "error");
    if (execTimeBadge) execTimeBadge.textContent = "ކުށެއް!";
  } finally {
    btnRun.disabled = false;
    btnRun.textContent = "▶ ހިންގާ (Ctrl+Enter)";
  }
}

if (btnRun) {
  btnRun.addEventListener("click", runDhiCode);
}

// Global keyboard shortcut: Ctrl + Enter / Cmd + Enter
document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    runDhiCode();
  }
});

// =============================================================================
// 5. Initial Bootstrapping
// =============================================================================
initTheme();
highlightStaticCodeSnippets();
updateHighlight();
initPyodide();
