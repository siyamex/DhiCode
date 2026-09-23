# lsp_server.py - Language Server Protocol Server for DhiCode
import sys
import os
import json
from typing import Dict, Any, List

from lexer import Lexer
from parser import Parser
from formatter import format_code

# Documentation catalog for hover
DHIVEHI_DOCS = {
    # Keywords
    "ކަނޑައަޅާ": "**ކަނޑައަޅާ (let / define)**\n\nއާ ވެރިއަބަލެއް ކަނޑައެޅުމަށް ނުވަތަ އުފެއްދުމަށް ބޭނުންކުރާ ކީވޯޑު.\n\n```dhicode\nކަނޑައަޅާ ނަން = \"އަޙްމަދު\"\nކަނޑައަޅާ އަގު = 50\n```",
    "ވަޒީފާ": "**ވަޒީފާ (function)**\n\nއައު ފަންކްޝަނެއް ހެދުމަށް ބޭނުންކުރާ ކީވޯޑު.\n\n```dhicode\nވަޒީފާ ގުނާ(އަދަދު)\n    ފޮނުވާ އަދަދު + 1\nނިމުނީ\n```",
    "ފޮނުވާ": "**ފޮނުވާ (return)**\n\nވަޒީފާއަކުން ނަތީޖާ އަނބުރާ ފޮނުވުމަށް ބޭނުންކުރާ ކީވޯޑު.",
    "ދައްކާ": "**ދައްކާ (print)**\n\nސްކްރީނަށް ނުވަތަ ޓާމިނަލަށް ލިޔުން/އަގު ނެރުމަށް ބޭނުންކުރާ ކީވޯޑު.\n\n```dhicode\nދައްކާ \"އައްސަލާމް ޢަލައިކުމް!\"\n```",
    "ނަމަ": "**ނަމަ (if)**\n\nޝަރުޠީ ބަޔާން (Conditional statement).\n\n```dhicode\nނަމަ އުމުރު >= 18\n    ދައްކާ \"ބޮޑު މީހެއް\"\nނިމުނީ\n```",
    "ނޫންނަމަ": "**ނޫންނަމަ (else)**\n\nޝަރުޠު ފުރިހަމަ ނުވާނަމަ ހިންގާ ބައި.",
    "ހިނދު": "**ހިނދު (while loop)**\n\nވަކި ޝަރުޠެއް ފުރިހަމަވާހައި ހިނދަކު ތަކުރާރުކުރާ ލޫޕް.",
    "ކޮންމެ": "**ކޮންމެ (for-each loop)**\n\nލިސްޓެއްގައިވާ ކޮންމެ އެއްޗެއް ވަކިވަކިން ނަގައިގެން ހިންގާ ލޫޕް.\n\n```dhicode\nކޮންމެ ރަށް ތެރޭގައި ރަށްތައް\n    ދައްކާ ރަށް\nނިމުނީ\n```",
    "ތެރޭގައި": "**ތެރޭގައި (in)**\n\n`ކޮންމެ` ލޫޕްގައި ލިސްޓު ކަނޑައެޅުމަށް ބޭނުންކުރާ ކީވޯޑު.",
    "ނިމުނީ": "**ނިމުނީ (end)**\n\nބްލޮކެއް (ވަޒީފާ، ނަމަ، ހިނދު، ކޮންމެ، މަސައްކަތްކުރޭ) ނިމުނުކަން އަންގައިދޭ ކީވޯޑު.",
    "މަސައްކަތްކުރޭ": "**މަސައްކަތްކުރޭ (try)**\n\nކުށެއް ހިނގައިދާނެ ކޯޑެއް ރައްކާތެރިކަމާއެކު ހިންގަން މަސައްކަތްކުރުން.\n\n```dhicode\nމަސައްކަތްކުރޭ\n    ކަނޑައަޅާ ނަތީޖާ = 10 / 0\nކުށެއް_ފެނިއްޖެނަމަ ކުށް\n    ދައްކާ \"މައްސަލައެއް: \" + ކުށް\nނިމުނީ\n```",
    "ކުށެއް_ފެނިއްޖެނަމަ": "**ކުށެއް_ފެނިއްޖެނަމަ (catch)**\n\nމަސައްކަތްކުރި ކޯޑުން ކުށެއް ފެނިއްޖެނަމަ އެ ކުށް ނަގައި ހިންގާ ބްލޮކް.",
    "ގެނޭ": "**ގެނޭ (import)**\n\nމޮޑިއުލްތަކާއި އެހެން ފައިލްތައް އެތެރެކުރުމަށް ބޭނުންކުރާ ކީވޯޑު.\n\n```dhicode\nގެނޭ \"ހިސާބު\"\nގެނޭ \"ނަކަތް\"\nގެނޭ \"ނަމާދު\"\nގެނޭ \"ނެޓްވޯކް\"\n```",
    "އުކާލާ": "**އުކާލާ (throw)**\n\nއައު ކުށެއް އުފައްދައި އުކާލުން (Raise exception).",

    # Built-in functions
    "ދިގުމިން": "**ދިގުމިން(ލިސްޓު ނުވަތަ ލިޔުން)**\n\nލިސްޓެއްގައިވާ އައިޓަމްތަކުގެ އަދަދު ނުވަތަ ލިޔުމެއްގެ އަކުރުގެ އަދަދު ހޯދާ ފަންކްޝަން.",
    "އަޅާ": "**އަޅާ(ލިސްޓު, އެތި)**\n\nލިސްޓުގެ އެންމެ ފަހަތަށް އާ އެއްޗެއް އިތުރުކުރުން (append).",
    "ނަގާ": "**ނަގާ(ލިސްޓު)**\n\nލިސްޓުގެ އެންމެ ފަހު އެތި ނަގައި ލިސްޓުން އުނިކުރުން (pop).",
    "ޖަޒުރު": "**ޖަޒުރު(އަދަދު)**\n\nނަންބަރެއްގެ ސްކުއެއަރ ރޫޓް (Square root) ހޯދުން.",
    "ބާރު": "**ބާރު(އަދަދު, ބާރު)**\n\nއަދަދެއްގެ ވަކި ބާރެއް (Power / Exponent) ހޯދުން.",
    "ކައިރި": "**ކައިރި(އަދަދު)**\n\nއަދަދެއް އެންމެ ކައިރި ފުރިހަމަ އަދަދަށް ބަދަލުކުރުން (Round).",
    "އިއްތިފާޤު": "**އިއްތިފާޤު(މިން, މެކްސް)**\n\nއިއްތިފާޤީ ރެންޑަމް ނަންބަރެއް ހޯދުން (Random integer).",
    "މިއަދުގެ_ނަކަތް": "**މިއަދުގެ_ނަކަތް()**\n\nމިއަދުގެ ތާރީޚަށް ފެތޭ ދިވެހި ނަކަތުގެ މަޢުލޫމާތު ހޯދުން (Nakaiy Calendar).",
    "ނަކަތް_ހޯދާ": "**ނަކަތް_ހޯދާ(މަސް, ދުވަސް)**\n\nވަކި ތާރީޚެއްގެ ދިވެހި ނަކަތް ހޯދުން.",
    "މިއަދުގެ_ވަގުތު": "**މިއަދުގެ_ވަގުތު(ރަށް=\"މާލެ\")**\n\nމިއަދުގެ ނަމާދު ވަގުތުތައް ހޯދުން (Prayer times).",
    "ދެން_އޮތް_ނަމާދު": "**ދެން_އޮތް_ނަމާދު(ރަށް=\"މާލެ\")**\n\nދެން އެންމެ އަވަހަށް އޮތް ނަމާދާއި ބާކީ މިނިޓް ހޯދުން.",
    "އަދަދު_ބަހަށް": "**އަދަދު_ބަހަށް(އަދަދު)**\n\nހިސާބު ނަންބަރު ދިވެހި ބަހަށް ބަދަލުކުރުން (Number to Dhivehi words).\n\n```dhicode\nއަދަދު_ބަހަށް(125) // 'ސަތޭކަ ފަންސަވީސް'\n```",
    "ތާނަ_ތަރުތީބު": "**ތާނަ_ތަރުތީބު(ލިސްޓު)**\n\nދިވެހި ބަސްތައް ތާނަ އަލިފުބާގެ ތަރުތީބުން އެތުރުން (Thaana alphabetical collation)."
}

class DhiCodeLspServer:
    def __init__(self):
        self.documents: Dict[str, str] = {}
        self.running = True

    def read_message(self) -> Dict[str, Any]:
        """Read standard JSON-RPC 2.0 message with Content-Length header."""
        content_length = 0
        while True:
            line = sys.stdin.buffer.readline()
            if not line:
                return None
            line_str = line.decode('ascii', errors='replace').strip()
            if not line_str:
                break
            if line_str.lower().startswith('content-length:'):
                content_length = int(line_str.split(':', 1)[1].strip())

        if content_length > 0:
            body = sys.stdin.buffer.read(content_length)
            return json.loads(body.decode('utf-8'))
        return None

    def send_message(self, message: Dict[str, Any]):
        """Send standard JSON-RPC 2.0 message with Content-Length header."""
        body = json.dumps(message, ensure_ascii=False).encode('utf-8')
        header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')
        sys.stdout.buffer.write(header)
        sys.stdout.buffer.write(body)
        sys.stdout.buffer.flush()

    def send_response(self, req_id: Any, result: Any = None, error: Any = None):
        msg = {
            "jsonrpc": "2.0",
            "id": req_id
        }
        if error:
            msg["error"] = error
        else:
            msg["result"] = result
        self.send_message(msg)

    def publish_diagnostics(self, uri: str, text: str):
        """Parse source and publish syntax diagnostics."""
        lexer = Lexer(text)
        parser = Parser(lexer)
        parser.parse_program()

        diagnostics = []
        for err in parser.errors:
            # Try to extract line info if formatted
            diagnostics.append({
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 0, "character": 1}
                },
                "severity": 1, # Error
                "source": "dhicode",
                "message": err
            })

        self.send_message({
            "jsonrpc": "2.0",
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": uri,
                "diagnostics": diagnostics
            }
        })

    def handle_request(self, message: Dict[str, Any]):
        method = message.get("method")
        req_id = message.get("id")
        params = message.get("params", {})

        if method == "initialize":
            self.send_response(req_id, {
                "capabilities": {
                    "textDocumentSync": 1, # Full
                    "hoverProvider": True,
                    "completionProvider": {
                        "resolveProvider": False,
                        "triggerCharacters": [".", "(", "\"", " "]
                    },
                    "documentFormattingProvider": True
                },
                "serverInfo": {
                    "name": "DhiCode Language Server",
                    "version": "0.3.0"
                }
            })

        elif method == "initialized":
            pass

        elif method == "textDocument/didOpen":
            doc = params.get("textDocument", {})
            uri = doc.get("uri")
            text = doc.get("text", "")
            self.documents[uri] = text
            self.publish_diagnostics(uri, text)

        elif method == "textDocument/didChange":
            doc = params.get("textDocument", {})
            uri = doc.get("uri")
            changes = params.get("contentChanges", [])
            if changes:
                text = changes[-1].get("text", "")
                self.documents[uri] = text
                self.publish_diagnostics(uri, text)

        elif method == "textDocument/hover":
            doc = params.get("textDocument", {})
            uri = doc.get("uri")
            pos = params.get("position", {})
            line_idx = pos.get("line", 0)
            char_idx = pos.get("character", 0)

            text = self.documents.get(uri, "")
            lines = text.splitlines()

            hover_doc = None
            if 0 <= line_idx < len(lines):
                line = lines[line_idx]
                # Find word at char_idx
                # Match Dhivehi or ASCII word
                import re
                words = re.finditer(r'[\u0780-\u07BFa-zA-Z_]+', line)
                for w in words:
                    if w.start() <= char_idx <= w.end():
                        target_word = w.group()
                        if target_word in DHIVEHI_DOCS:
                            hover_doc = DHIVEHI_DOCS[target_word]
                        break

            if hover_doc:
                self.send_response(req_id, {
                    "contents": {
                        "kind": "markdown",
                        "value": hover_doc
                    }
                })
            else:
                self.send_response(req_id, None)

        elif method == "textDocument/completion":
            items = []
            # Keywords
            for kw in DHIVEHI_DOCS:
                items.append({
                    "label": kw,
                    "kind": 14 if kw in ("ކަނޑައަޅާ", "ވަޒީފާ", "ނަމަ", "ހިނދު", "ކޮންމެ", "ނިމުނީ") else 3,
                    "detail": "ދިވެހި ކޯޑު (DhiCode)",
                    "documentation": {
                        "kind": "markdown",
                        "value": DHIVEHI_DOCS.get(kw, "")
                    }
                })
            self.send_response(req_id, {
                "isIncomplete": False,
                "items": items
            })

        elif method == "textDocument/formatting":
            doc = params.get("textDocument", {})
            uri = doc.get("uri")
            text = self.documents.get(uri, "")

            formatted = format_code(text)
            lines = text.splitlines()

            self.send_response(req_id, [
                {
                    "range": {
                        "start": {"line": 0, "character": 0},
                        "end": {"line": len(lines) + 1, "character": 0}
                    },
                    "newText": formatted
                }
            ])

        elif method == "shutdown":
            self.send_response(req_id, None)

        elif method == "exit":
            self.running = False

    def run(self):
        while self.running:
            msg = self.read_message()
            if msg is None:
                break
            self.handle_request(msg)

if __name__ == "__main__":
    server = DhiCodeLspServer()
    server.run()
