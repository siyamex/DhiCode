// vscode-dhicode/extension.js - DhiCode VS Code Extension
const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

const DHIVEHI_DOCS = {
  "ކަނޑައަޅާ": "**ކަނޑައަޅާ (let / define)**\n\nއާ ވެރިއަބަލެއް ކަނޑައެޅުމަށް ބޭނުންކުރާ ކީވޯޑު.\n\n```dhicode\nކަނޑައަޅާ އަގު = 50\n```",
  "ވަޒީފާ": "**ވަޒީފާ (function)**\n\nއައު ފަންކްޝަނެއް ހެދުމަށް ބޭނުންކުރާ ކީވޯޑު.\n\n```dhicode\nވަޒީފާ ގުނާ(އަދަދު)\n    ފޮނުވާ އަދަދު + 1\nނިމުނީ\n```",
  "ފޮނުވާ": "**ފޮނުވާ (return)**\n\nވަޒީފާއަކުން ނަތީޖާ އަނބުރާ ފޮނުވުމަށް ބޭނުންކުރާ ކީވޯޑު.",
  "ދައްކާ": "**ދައްކާ (print)**\n\nސްކްރީނަށް ނުވަތަ ޓާމިނަލަށް ލިޔުން ނެރުމަށް ބޭނުންކުރާ ކީވޯޑު.",
  "ނަމަ": "**ނަމަ (if)**\n\nޝަރުޠީ ބަޔާން (Conditional statement).",
  "ނޫންނަމަ": "**ނޫންނަމަ (else)**\n\nޝަރުޠު ފުރިހަމަ ނުވާނަމަ ހިންގާ ބައި.",
  "ހިނދު": "**ހިނދު (while loop)**\n\nޝަރުޠެއް ފުރިހަމަވާހައި ހިނދަކު ތަކުރާރުކުރާ ލޫޕް.",
  "ކޮންމެ": "**ކޮންމެ (for-each loop)**\n\nލިސްޓެއްގައިވާ ކޮންމެ އެއްޗަކަށް ހިންގާ ލޫޕް.",
  "ނިމުނީ": "**ނިމުނީ (end)**\n\nބްލޮކެއް ނިމުނުކަން އަންގައިދޭ ކީވޯޑު.",
  "މަސައްކަތްކުރޭ": "**މަސައްކަތްކުރޭ (try)**\n\nކުށް ސަލާމަތްކުރުމަށް މަސައްކަތްކުރާ ބްލޮކް.",
  "ކުށެއް_ފެނިއްޖެނަމަ": "**ކުށެއް_ފެނިއްޖެނަމަ (catch)**\n\nކުށެއް ފެނިއްޖެނަމަ އެ ކުށް ނަގައި ހިންގާ ބްލޮކް.",
  "ގެނޭ": "**ގެނޭ (import)**\n\nމޮޑިއުލްތައް އެތެރެކުރުން (ހިސާބު, ނަކަތް, ނަމާދު, ނެޓްވޯކް).",
  "އަދަދު_ބަހަށް": "**އަދަދު_ބަހަށް(އަދަދު)**\n\nހިސާބު ނަންބަރު ދިވެހި ބަހަށް ބަދަލުކުރުން.",
  "ތާނަ_ތަރުތީބު": "**ތާނަ_ތަރުތީބު(ލިސްޓު)**\n\nދިވެހި ބަސްތައް ތާނަ އަލިފުބާގެ ތަރުތީބުން އެތުރުން.",
  "މިއަދުގެ_ނަކަތް": "**މިއަދުގެ_ނަކަތް()**\n\nމިއަދުގެ ދިވެހި ނަކަތުގެ މަޢުލޫމާތު.",
  "މިއަދުގެ_ވަގުތު": "**މިއަދުގެ_ވަގުތު(ރަށް)**\n\nމިއަދުގެ ނަމާދު ވަގުތުތައް."
};

function activate(context) {
  // 1. Hover Provider
  context.subscriptions.push(
    vscode.languages.registerHoverProvider('dhicode', {
      provideHover(document, position) {
        const wordRange = document.getWordRangeAtPosition(position, /[\u0780-\u07BFa-zA-Z_]+/);
        if (!wordRange) return null;
        const word = document.getText(wordRange);
        if (DHIVEHI_DOCS[word]) {
          return new vscode.Hover(new vscode.MarkdownString(DHIVEHI_DOCS[word]));
        }
        return null;
      }
    })
  );

  // 2. Completion Item Provider
  context.subscriptions.push(
    vscode.languages.registerCompletionItemProvider('dhicode', {
      provideCompletionItems() {
        return Object.keys(DHIVEHI_DOCS).map(key => {
          const item = new vscode.CompletionItem(key, vscode.CompletionItemKind.Keyword);
          item.detail = 'ދިވެހި ކޯޑު (DhiCode)';
          item.documentation = new vscode.MarkdownString(DHIVEHI_DOCS[key]);
          return item;
        });
      }
    })
  );

  // 3. Document Formatting Provider
  context.subscriptions.push(
    vscode.languages.registerDocumentFormattingEditProvider('dhicode', {
      provideDocumentFormattingEdits(document) {
        return new Promise((resolve) => {
          const proc = spawn('python', ['-m', 'formatter', document.fileName], {
            cwd: vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri.fsPath : undefined
          });

          let output = '';
          proc.stdout.on('data', (d) => output += d.toString('utf8'));
          proc.on('close', (code) => {
            if (code === 0 && output) {
              const fullRange = new vscode.Range(
                document.positionAt(0),
                document.positionAt(document.getText().length)
              );
              resolve([vscode.TextEdit.replace(fullRange, output)]);
            } else {
              resolve([]);
            }
          });
          proc.on('error', () => resolve([]));
        });
      }
    })
  );

  // 4. Run Command
  context.subscriptions.push(
    vscode.commands.registerCommand('dhicode.run', () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) return;
      const file = editor.document.fileName;
      const terminal = vscode.window.activeTerminal || vscode.window.createTerminal('DhiCode');
      terminal.show();
      terminal.sendText(`python dhicode.py run "${file}"`);
    })
  );

  // 5. Build Command
  context.subscriptions.push(
    vscode.commands.registerCommand('dhicode.build', () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) return;
      const file = editor.document.fileName;
      const terminal = vscode.window.activeTerminal || vscode.window.createTerminal('DhiCode');
      terminal.show();
      terminal.sendText(`python dhicode.py build "${file}"`);
    })
  );
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
