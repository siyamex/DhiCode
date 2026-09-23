// web/app.js - DhiCode Live Web Playground Controller
let pyodide = null;
let isReady = false;

// DOM Elements
const editor = document.getElementById("code-editor");
const terminal = document.getElementById("terminal-output");
const statusIndicator = document.getElementById("runtime-status");
const btnRun = document.getElementById("btn-run");
const btnClear = document.getElementById("btn-clear");
const btnDir = document.getElementById("btn-dir");
const btnCopyCmd = document.getElementById("btn-copy-cmd");
const btnCopyCode = document.getElementById("btn-copy-code");
const execTimeBadge = document.getElementById("exec-time");
const exampleTabs = document.querySelectorAll("#example-tabs .ide-tab");

// Set initial example
if (typeof EXAMPLES !== "undefined" && EXAMPLES.hello) {
  editor.value = EXAMPLES.hello.code;
}

// Append line to web terminal
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
    terminal.dir = isRtl ? "rtl" : "ltr";
    btnDir.innerHTML = isRtl ? `<span id="dir-icon">🔀</span> RTL` : `<span id="dir-icon">🔀</span> LTR`;
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

// Initialize Pyodide WebAssembly
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

// Start initialization
initPyodide();
