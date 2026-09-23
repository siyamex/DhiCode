// web/app.js
let pyodide = null;
let isReady = false;

const editor = document.getElementById("code-editor");
const terminal = document.getElementById("terminal-output");
const statusIndicator = document.getElementById("runtime-status");
const exampleSelect = document.getElementById("example-select");
const btnRun = document.getElementById("btn-run");
const btnClear = document.getElementById("btn-clear");
const btnDir = document.getElementById("btn-dir");

// Set default example
editor.value = EXAMPLES.hello;

// Append line to web terminal
function appendTerminal(text, type = "normal") {
  const line = document.createElement("div");
  line.className = `terminal-line terminal-${type}`;
  line.textContent = text;
  terminal.appendChild(line);
  terminal.scrollTop = terminal.scrollHeight;
}

// Clear terminal
btnClear.addEventListener("click", () => {
  terminal.innerHTML = "";
});

// Toggle Text Direction (RTL / LTR)
let isRtl = true;
btnDir.addEventListener("click", () => {
  isRtl = !isRtl;
  editor.dir = isRtl ? "rtl" : "ltr";
  terminal.dir = isRtl ? "rtl" : "ltr";
  btnDir.innerHTML = isRtl ? `<span>🔀</span> RTL` : `<span>🔀</span> LTR`;
});

// Example switcher
exampleSelect.addEventListener("change", (e) => {
  const key = e.target.value;
  if (EXAMPLES[key]) {
    editor.value = EXAMPLES[key];
  }
});

// Initialize Pyodide WebAssembly
async function initPyodide() {
  try {
    statusIndicator.textContent = "Wasm ލޯޑުވަނީ...";
    statusIndicator.className = "status-indicator loading";

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
    statusIndicator.textContent = "ތައްޔާރު (Ready)";
    statusIndicator.className = "status-indicator ready";

    terminal.innerHTML = "";
    appendTerminal("✅ DhiCode Wasm ރަންޓައިމް ކާމިޔާބުކަމާއެކު ތައްޔާރުވެއްޖެ! ކޯޑު ހިންގުމަށް 'ހިންގާ (Run)' ފިއްތަވާ.", "success");
  } catch (err) {
    statusIndicator.textContent = "މައްސަލައެއް!";
    statusIndicator.className = "status-indicator error";
    appendTerminal(`Error initializing Pyodide: ${err}`, "error");
  }
}

// Run Code
async function runDhiCode() {
  if (!isReady || !pyodide) {
    appendTerminal("އަދި ރަންޓައިމް ތައްޔާރެއް ނުވޭ. މަޑުކޮށްލައްވާ...", "warning");
    return;
  }

  terminal.innerHTML = "";
  const code = editor.value;

  btnRun.disabled = true;
  btnRun.textContent = "ހިނގަނީ...";

  try {
    // Mount custom stdout callback
    pyodide.globals.set("dhi_source", code);
    pyodide.globals.set("output_log", []);

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

    const logs = pyodide.globals.get("logs").toJs();
    if (logs.length === 0) {
      appendTerminal("(ނިމުނީ - އެއްވެސް ލިޔުމެއް ނުދައްކާ)", "normal");
    } else {
      for (const [type, msg] of logs) {
        appendTerminal(msg, type);
      }
    }
  } catch (err) {
    appendTerminal(`ރަންޓައިމް ކުށް: ${err}`, "error");
  } finally {
    btnRun.disabled = false;
    btnRun.textContent = "▶ ހިންގާ (Run)";
  }
}

btnRun.addEventListener("click", runDhiCode);

// Keyboard shortcut: Ctrl + Enter / Cmd + Enter
document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    runDhiCode();
  }
});

// Start initialization
initPyodide();
