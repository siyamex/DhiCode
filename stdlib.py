# stdlib.py - DhiCode Extended Standard Library with Maldivian Cultural & Dual-Language Modules
import math
import time
import os
import sys
import random
import json
import urllib.request
import urllib.parse
import urllib.error
import hashlib
import hmac
import base64
import secrets
import re
import platform
import sqlite3
import http.server
import socketserver
import threading
from datetime import datetime, date
from typing import Dict, Any, List

def get_stdlib_modules(obj_factory) -> Dict[str, Dict[str, Any]]:
    """
    Returns extended standard library modules for DhiCode.
    obj_factory provides:
      - num, string, boolean, null, list, dict, error, builtin, py_to_dhi, dhi_to_py, call_fn
    """

    py_to_dhi = obj_factory.get('py_to_dhi', lambda v: obj_factory['string'](str(v)))
    dhi_to_py = obj_factory.get('dhi_to_py', lambda o: o.inspect())
    call_fn = obj_factory.get('call_fn', lambda fn, args: obj_factory['error']("Function invocation bridge not available"))

    # =========================================================================
    # 1. ހިސާބު (Math Module - "math")
    # =========================================================================
    def math_sqrt(*args):
        if not args or not hasattr(args[0], 'value'):
            return obj_factory['error']("ޖަޒުރު() / sqrt() ބޭނުންކުރަންވާނީ ނަންބަރަކާއެކު")
        v = args[0].value
        if v < 0:
            return obj_factory['error']("ނެގަޓިވް އަދަދެއްގެ ޖަޒުރެއް ނުހޯދޭނެ")
        return obj_factory['num'](math.sqrt(v))

    def math_pow(*args):
        if len(args) < 2:
            return obj_factory['error']("ބާރު() / pow() އަށް 2 އަދަދު ދޭންވާނެ")
        return obj_factory['num'](math.pow(args[0].value, args[1].value))

    def math_round(*args):
        if not args:
            return obj_factory['error']("ކައިރި() / round() އަށް އަދަދެއް ދޭންވާނެ")
        return obj_factory['num'](round(args[0].value))

    def math_floor(*args):
        if not args:
            return obj_factory['error']("ފްލޯރ() / floor() އަށް އަދަދެއް ދޭންވާނެ")
        return obj_factory['num'](math.floor(args[0].value))

    def math_ceil(*args):
        if not args:
            return obj_factory['error']("ސީލް() / ceil() އަށް އަދަދެއް ދޭންވާނެ")
        return obj_factory['num'](math.ceil(args[0].value))

    def math_max(*args):
        if not args:
            return obj_factory['error']("އެންމެ_ބޮޑު() / max() އަށް އަދަދުތަކެއް ދޭންވާނެ")
        return obj_factory['num'](max(a.value for a in args))

    def math_min(*args):
        if not args:
            return obj_factory['error']("އެންމެ_ކުޑަ() / min() އަށް އަދަދުތަކެއް ދޭންވާނެ")
        return obj_factory['num'](min(a.value for a in args))

    def math_random(*args):
        min_v = int(args[0].value) if len(args) > 0 and hasattr(args[0], 'value') else 0
        max_v = int(args[1].value) if len(args) > 1 and hasattr(args[1], 'value') else 100
        return obj_factory['num'](random.randint(min_v, max_v))

    def math_abs(*args):
        if not args or not hasattr(args[0], 'value'):
            return obj_factory['error']("މުތުލަޤު() / abs() އަށް ނަންބަރެއް ދޭންވާނެ")
        return obj_factory['num'](abs(args[0].value))

    def math_sin(*args):
        if not args or not hasattr(args[0], 'value'):
            return obj_factory['error']("ސައިން() / sin() އަށް ނަންބަރެއް ދޭންވާނެ")
        return obj_factory['num'](math.sin(args[0].value))

    def math_cos(*args):
        if not args or not hasattr(args[0], 'value'):
            return obj_factory['error']("ކޮސް() / cos() އަށް ނަންބަރެއް ދޭންވާނެ")
        return obj_factory['num'](math.cos(args[0].value))

    def math_tan(*args):
        if not args or not hasattr(args[0], 'value'):
            return obj_factory['error']("ޓޭން() / tan() އަށް ނަންބަރެއް ދޭންވާނެ")
        return obj_factory['num'](math.tan(args[0].value))

    def math_log(*args):
        if not args or not hasattr(args[0], 'value'):
            return obj_factory['error']("ލޮގް() / log() އަށް ނަންބަރެއް ދޭންވާނެ")
        v = args[0].value
        if v <= 0:
            return obj_factory['error']("0 ނުވަތަ ނެގަޓިވް އަދަދެއްގެ ލޮގް އެއް ނުހޯދޭނެ")
        if len(args) > 1 and hasattr(args[1], 'value'):
            return obj_factory['num'](math.log(v, args[1].value))
        return obj_factory['num'](math.log(v))

    math_module = {
        # Dhivehi
        "ޖަޒުރު": obj_factory['builtin'](math_sqrt),
        "ބާރު": obj_factory['builtin'](math_pow),
        "ކައިރި": obj_factory['builtin'](math_round),
        "ފްލޯރ": obj_factory['builtin'](math_floor),
        "ސީލް": obj_factory['builtin'](math_ceil),
        "އެންމެ_ބޮޑު": obj_factory['builtin'](math_max),
        "އެންމެ_ކުޑަ": obj_factory['builtin'](math_min),
        "އިއްތިފާޤު": obj_factory['builtin'](math_random),
        "މުތުލަޤު": obj_factory['builtin'](math_abs),
        "ސައިން": obj_factory['builtin'](math_sin),
        "ކޮސް": obj_factory['builtin'](math_cos),
        "ޓޭން": obj_factory['builtin'](math_tan),
        "ލޮގް": obj_factory['builtin'](math_log),
        "ޕައި": obj_factory['num'](math.pi),
        "އީ": obj_factory['num'](math.e),

        # English
        "sqrt": obj_factory['builtin'](math_sqrt),
        "pow": obj_factory['builtin'](math_pow),
        "round": obj_factory['builtin'](math_round),
        "floor": obj_factory['builtin'](math_floor),
        "ceil": obj_factory['builtin'](math_ceil),
        "max": obj_factory['builtin'](math_max),
        "min": obj_factory['builtin'](math_min),
        "random": obj_factory['builtin'](math_random),
        "abs": obj_factory['builtin'](math_abs),
        "sin": obj_factory['builtin'](math_sin),
        "cos": obj_factory['builtin'](math_cos),
        "tan": obj_factory['builtin'](math_tan),
        "log": obj_factory['builtin'](math_log),
        "pi": obj_factory['num'](math.pi),
        "PI": obj_factory['num'](math.pi),
        "e": obj_factory['num'](math.e),
        "E": obj_factory['num'](math.e),
    }

    # =========================================================================
    # 2. ފައިލް (File System Module - "file" / "fs")
    # =========================================================================
    def file_read(*args):
        if not args:
            return obj_factory['error']("ކިޔާ() / read() އަށް ފައިލްގެ ނަން ދޭންވާނެ")
        path = args[0].inspect()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return obj_factory['string'](content)
        except Exception as e:
            return obj_factory['error'](f"ފައިލް ކިޔުމުގައި މައްސަލައެއް: {e}")

    def file_write(*args):
        if len(args) < 2:
            return obj_factory['error']("ލިޔޭ() / write() އަށް ފައިލްގެ ނަމާއި ލިޔުން ދޭންވާނެ")
        path = args[0].inspect()
        content = args[1].inspect()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return obj_factory['boolean'](True)
        except Exception as e:
            return obj_factory['error'](f"ފައިލް ލިޔުމުގައި މައްސަލައެއް: {e}")

    def file_append(*args):
        if len(args) < 2:
            return obj_factory['error']("އިތުރުކުރޭ() / append() އަށް ފައިލްގެ ނަމާއި ލިޔުން ދޭންވާނެ")
        path = args[0].inspect()
        content = args[1].inspect()
        try:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
            return obj_factory['boolean'](True)
        except Exception as e:
            return obj_factory['error'](f"ފައިލަށް އިތުރުކުރުމުގައި މައްސަލައެއް: {e}")

    def file_exists(*args):
        if not args:
            return obj_factory['boolean'](False)
        path = args[0].inspect()
        return obj_factory['boolean'](os.path.exists(path))

    def file_delete(*args):
        if not args:
            return obj_factory['error']("ފޮހޭ() / delete() އަށް ފައިލްގެ ނަން ދޭންވާނެ")
        path = args[0].inspect()
        try:
            if os.path.isdir(path):
                os.rmdir(path)
            elif os.path.exists(path):
                os.remove(path)
            return obj_factory['boolean'](True)
        except Exception as e:
            return obj_factory['error'](f"ފައިލް ފޮހުމުގައި މައްސަލައެއް: {e}")

    def file_mkdir(*args):
        if not args:
            return obj_factory['error']("ހަދާ() / mkdir() އަށް ޑިރެކްޓަރީ ނަން ދޭންވާނެ")
        path = args[0].inspect()
        try:
            os.makedirs(path, exist_ok=True)
            return obj_factory['boolean'](True)
        except Exception as e:
            return obj_factory['error'](f"ޑިރެކްޓަރީ ހެދުމުގައި މައްސަލައެއް: {e}")

    def file_list_dir(*args):
        path = args[0].inspect() if args else "."
        try:
            entries = os.listdir(path)
            return obj_factory['list']([obj_factory['string'](e) for e in entries])
        except Exception as e:
            return obj_factory['error'](f"ޑިރެކްޓަރީ ލިސްޓުކުރުމުގައި މައްސަލައެއް: {e}")

    def file_size(*args):
        if not args:
            return obj_factory['error']("ބޮޑުމިން() / file_size() އަށް ފައިލްގެ ނަން ދޭންވާނެ")
        path = args[0].inspect()
        try:
            return obj_factory['num'](os.path.getsize(path))
        except Exception as e:
            return obj_factory['error'](f"ފައިލްގެ ބޮޑުމިން ބެލުމުގައި މައްސަލައެއް: {e}")

    file_module = {
        # Dhivehi
        "ކިޔާ": obj_factory['builtin'](file_read),
        "ލިޔޭ": obj_factory['builtin'](file_write),
        "އިތުރުކުރޭ": obj_factory['builtin'](file_append),
        "ވޭތޯ": obj_factory['builtin'](file_exists),
        "ފޮހޭ": obj_factory['builtin'](file_delete),
        "ހަދާ": obj_factory['builtin'](file_mkdir),
        "ލިސްޓު_ކުރޭ": obj_factory['builtin'](file_list_dir),
        "ބޮޑުމިން": obj_factory['builtin'](file_size),

        # English
        "read": obj_factory['builtin'](file_read),
        "write": obj_factory['builtin'](file_write),
        "append": obj_factory['builtin'](file_append),
        "exists": obj_factory['builtin'](file_exists),
        "delete": obj_factory['builtin'](file_delete),
        "remove": obj_factory['builtin'](file_delete),
        "mkdir": obj_factory['builtin'](file_mkdir),
        "list_dir": obj_factory['builtin'](file_list_dir),
        "listdir": obj_factory['builtin'](file_list_dir),
        "size": obj_factory['builtin'](file_size),
        "file_size": obj_factory['builtin'](file_size),
    }

    # =========================================================================
    # 3. ވަގުތު (Time Module - "time")
    # =========================================================================
    def time_now(*args):
        return obj_factory['num'](time.time())

    def time_sleep(*args):
        if not args:
            return obj_factory['null']()
        secs = args[0].value if hasattr(args[0], 'value') else 0
        time.sleep(secs)
        return obj_factory['null']()

    def time_date_str(*args):
        fmt = args[0].inspect() if args else "%Y-%m-%d %H:%M:%S"
        return obj_factory['string'](time.strftime(fmt))

    def time_timestamp(*args):
        now = datetime.now()
        y = int(args[0].value) if len(args) > 0 and hasattr(args[0], 'value') else now.year
        m = int(args[1].value) if len(args) > 1 and hasattr(args[1], 'value') else now.month
        d = int(args[2].value) if len(args) > 2 and hasattr(args[2], 'value') else now.day
        hr = int(args[3].value) if len(args) > 3 and hasattr(args[3], 'value') else 0
        mn = int(args[4].value) if len(args) > 4 and hasattr(args[4], 'value') else 0
        sc = int(args[5].value) if len(args) > 5 and hasattr(args[5], 'value') else 0
        try:
            dt = datetime(y, m, d, hr, mn, sc)
            return obj_factory['num'](dt.timestamp())
        except Exception as e:
            return obj_factory['error'](f"ތާރީޚް ހެދުމުގައި މައްސަލައެއް: {e}")

    def time_parse_date(*args):
        if not args:
            return obj_factory['error']("ބަދަލުކުރޭ() / parse_date() އަށް ތާރީޚް ލިޔުން ދޭންވާނެ")
        date_str = args[0].inspect()
        fmt = args[1].inspect() if len(args) > 1 else "%Y-%m-%d"
        try:
            dt = datetime.strptime(date_str, fmt)
            return obj_factory['num'](dt.timestamp())
        except Exception as e:
            return obj_factory['error'](f"ތާރީޚް ކިޔުމުގައި މައްސަލައެއް: {e}")

    time_module = {
        # Dhivehi
        "މިހާރު": obj_factory['builtin'](time_now),
        "ހިނދުކޮޅު": obj_factory['builtin'](time_sleep),
        "ތާރީޚް": obj_factory['builtin'](time_date_str),
        "ވަގުތު_ހަދާ": obj_factory['builtin'](time_timestamp),
        "ބަދަލުކުރޭ": obj_factory['builtin'](time_parse_date),

        # English
        "now": obj_factory['builtin'](time_now),
        "sleep": obj_factory['builtin'](time_sleep),
        "format": obj_factory['builtin'](time_date_str),
        "date_str": obj_factory['builtin'](time_date_str),
        "timestamp": obj_factory['builtin'](time_timestamp),
        "parse_date": obj_factory['builtin'](time_parse_date),
    }

    # =========================================================================
    # 4. ނިޒާމު (System & OS Module - "os" / "sys")
    # =========================================================================
    def sys_argv(*args):
        args_list = [obj_factory['string'](a) for a in sys.argv]
        return obj_factory['list'](args_list)

    def sys_exit(*args):
        code = int(args[0].value) if args and hasattr(args[0], 'value') else 0
        sys.exit(code)

    def sys_getenv(*args):
        if not args:
            return obj_factory['string']("")
        key = args[0].inspect()
        return obj_factory['string'](os.environ.get(key, ""))

    def sys_platform(*args):
        return obj_factory['string'](sys.platform)

    def sys_cwd(*args):
        return obj_factory['string'](os.getcwd())

    system_module = {
        # Dhivehi
        "އާގިއުމެންޓުތައް": obj_factory['builtin'](sys_argv),
        "ހުއްޓާ": obj_factory['builtin'](sys_exit),
        "އެންވައިރޮންމެންޓް": obj_factory['builtin'](sys_getenv),
        "ޕްލެޓްފޯމް": obj_factory['builtin'](sys_platform),
        "މަގު": obj_factory['builtin'](sys_cwd),

        # English
        "args": obj_factory['builtin'](sys_argv),
        "argv": obj_factory['builtin'](sys_argv),
        "exit": obj_factory['builtin'](sys_exit),
        "getenv": obj_factory['builtin'](sys_getenv),
        "platform": obj_factory['builtin'](sys_platform),
        "cwd": obj_factory['builtin'](sys_cwd),
    }

    # =========================================================================
    # 5. ނެޓްވޯކް (Network, HTTP & JSON Module - "net" / "http")
    # =========================================================================
    def _execute_http(method: str, args):
        if not args:
            return obj_factory['error'](f"{method}() އަށް ޔޫއާރްއެލް (URL) ދޭންވާނެ")
        url = args[0].inspect()
        data = None
        headers = {}

        if method in ("POST", "PUT") and len(args) > 1:
            raw_data = dhi_to_py(args[1])
            if isinstance(raw_data, (dict, list)):
                data = json.dumps(raw_data, ensure_ascii=False).encode('utf-8')
                headers["Content-Type"] = "application/json; charset=utf-8"
            elif isinstance(raw_data, str):
                data = raw_data.encode('utf-8')
            else:
                data = str(raw_data).encode('utf-8')

        header_idx = 2 if method in ("POST", "PUT") else 1
        if len(args) > header_idx:
            raw_h = dhi_to_py(args[header_idx])
            if isinstance(raw_h, dict):
                for k, v in raw_h.items():
                    headers[str(k)] = str(v)

        if "User-Agent" not in headers:
            headers["User-Agent"] = "DhiCode/0.4.0"

        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=10) as resp:
                status_code = resp.status
                body_bytes = resp.read()
                body_text = body_bytes.decode('utf-8', errors='replace')
                resp_headers = dict(resp.headers)
                try:
                    parsed_json = json.loads(body_text)
                except Exception:
                    parsed_json = None

                return py_to_dhi({
                    "ކޯޑު": status_code, "status": status_code,
                    "ލިޔުން": body_text, "body": body_text,
                    "ހެޑަރ": resp_headers, "headers": resp_headers,
                    "ޖޭސަން": parsed_json, "json": parsed_json
                })
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace') if hasattr(e, 'read') else ""
            return py_to_dhi({
                "ކޯޑު": e.code, "status": e.code,
                "ލިޔުން": body, "body": body,
                "ހެޑަރ": dict(e.headers) if hasattr(e, 'headers') else {}, "headers": dict(e.headers) if hasattr(e, 'headers') else {},
                "ޖޭސަން": None, "json": None
            })
        except Exception as e:
            return obj_factory['error'](f"ނެޓްވޯކް މައްސަލައެއް ({method}): {e}")

    def net_http_get(*args):
        return _execute_http("GET", args)

    def net_http_post(*args):
        return _execute_http("POST", args)

    def net_http_put(*args):
        return _execute_http("PUT", args)

    def net_http_delete(*args):
        return _execute_http("DELETE", args)

    def net_json_parse(*args):
        if not args:
            return obj_factory['error']("ޖޭސަން_ކިޔާ() / parse_json() އަށް ލިޔުމެއް ދޭންވާނެ")
        raw = args[0].inspect()
        try:
            data = json.loads(raw)
            return py_to_dhi(data)
        except Exception as e:
            return obj_factory['error'](f"ޖޭސަން ކިޔުމުގައި ކުށެއް: {e}")

    def net_json_stringify(*args):
        if not args:
            return obj_factory['error']("ޖޭސަން_ހަދާ() / stringify_json() އަށް އެއްޗެއް ދޭންވާނެ")
        py_data = dhi_to_py(args[0])
        try:
            res = json.dumps(py_data, ensure_ascii=False, indent=2)
            return obj_factory['string'](res)
        except Exception as e:
            return obj_factory['error'](f"ޖޭސަން ހެދުމުގައި ކުށެއް: {e}")

    def net_url_encode(*args):
        if not args:
            return obj_factory['string']("")
        val = args[0].inspect()
        return obj_factory['string'](urllib.parse.quote(val))

    def net_url_decode(*args):
        if not args:
            return obj_factory['string']("")
        val = args[0].inspect()
        return obj_factory['string'](urllib.parse.unquote(val))

    def _create_dhi_http_handler(handler_fn, silent=True):
        class DhiHTTPHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                if not silent:
                    sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

            def _handle_request(self, method: str):
                parsed_url = urllib.parse.urlparse(self.path)
                req_path = parsed_url.path
                query_dict = {}
                if parsed_url.query:
                    qs_parts = urllib.parse.parse_qs(parsed_url.query, keep_blank_values=True)
                    for k, v in qs_parts.items():
                        query_dict[k] = v[0] if len(v) == 1 else v

                headers_dict = dict(self.headers)
                content_length = int(self.headers.get('Content-Length', 0))
                body_bytes = self.rfile.read(content_length) if content_length > 0 else b""
                body_str = body_bytes.decode('utf-8', errors='replace')

                parsed_json = None
                if body_str:
                    try:
                        parsed_json = json.loads(body_str)
                    except Exception:
                        parsed_json = None

                req_py = {
                    "method": method, "ކަން": method,
                    "path": req_path, "މަގު": req_path,
                    "query": query_dict, "ކިއަރީ": query_dict,
                    "query_string": parsed_url.query, "ކިއަރީ_ލިޔުން": parsed_url.query,
                    "headers": headers_dict, "ހެޑަރ": headers_dict,
                    "body": body_str, "ހަށިގަނޑު": body_str, "ލިޔުން": body_str,
                    "json": parsed_json, "ޖޭސަން": parsed_json,
                }
                dhi_req = py_to_dhi(req_py)

                target_fn = handler_fn
                if hasattr(handler_fn, 'pairs'):
                    target_fn = handler_fn.pairs.get("handle") or handler_fn.pairs.get("ހިންގާ") or handler_fn

                try:
                    res_obj = call_fn(target_fn, [dhi_req])
                except Exception as e:
                    res_obj = obj_factory['error'](f"ހޭންޑްލަރ ހިންގުމުގައި މައްސަލައެއް: {e}")

                self._send_dhi_response(res_obj)

            def _send_dhi_response(self, res_obj):
                status_code = 200
                res_headers = {}
                res_body = b""

                if hasattr(res_obj, 'type_str') and res_obj.type_str() == "ކުށް":
                    status_code = 500
                    res_headers["Content-Type"] = "application/json; charset=utf-8"
                    err_msg = res_obj.message if hasattr(res_obj, 'message') else str(res_obj)
                    res_body = json.dumps({"error": err_msg}, ensure_ascii=False).encode('utf-8')

                elif hasattr(res_obj, 'pairs'):
                    pairs = res_obj.pairs
                    st_val = pairs.get("status") or pairs.get("ކޯޑު")
                    if st_val is not None and hasattr(st_val, 'value'):
                        status_code = int(st_val.value)

                    h_val = pairs.get("headers") or pairs.get("ހެޑަރ")
                    if h_val is not None and hasattr(h_val, 'pairs'):
                        for hk, hv in h_val.pairs.items():
                            res_headers[str(hk)] = hv.inspect() if hasattr(hv, 'inspect') else str(hv)

                    if "json" in pairs or "ޖޭސަން" in pairs:
                        j_val = pairs.get("json") or pairs.get("ޖޭސަން")
                        py_j = dhi_to_py(j_val)
                        res_body = json.dumps(py_j, ensure_ascii=False).encode('utf-8')
                        if "Content-Type" not in res_headers:
                            res_headers["Content-Type"] = "application/json; charset=utf-8"
                    elif "body" in pairs or "ހަށިގަނޑު" in pairs or "ލިޔުން" in pairs:
                        b_val = pairs.get("body") or pairs.get("ހަށިގަނޑު") or pairs.get("ލިޔުން")
                        b_text = b_val.inspect() if hasattr(b_val, 'inspect') else str(b_val)
                        res_body = b_text.encode('utf-8')
                    else:
                        if status_code != 204:
                            py_d = dhi_to_py(res_obj)
                            res_body = json.dumps(py_d, ensure_ascii=False).encode('utf-8')
                            if "Content-Type" not in res_headers:
                                res_headers["Content-Type"] = "application/json; charset=utf-8"

                elif hasattr(res_obj, 'type_str') and res_obj.type_str() == "ލިޔުން":
                    text = res_obj.value
                    res_body = text.encode('utf-8')
                    stripped = text.strip()
                    if stripped.startswith("<html") or stripped.startswith("<!DOCTYPE") or stripped.startswith("<"):
                        res_headers["Content-Type"] = "text/html; charset=utf-8"
                    else:
                        res_headers["Content-Type"] = "text/plain; charset=utf-8"

                elif hasattr(res_obj, 'type_str') and res_obj.type_str() == "ހުސް":
                    status_code = 204
                    res_body = b""

                else:
                    py_data = dhi_to_py(res_obj)
                    res_body = json.dumps(py_data, ensure_ascii=False).encode('utf-8')
                    res_headers["Content-Type"] = "application/json; charset=utf-8"

                res_headers["Content-Length"] = str(len(res_body))

                try:
                    self.send_response(status_code)
                    for hk, hv in res_headers.items():
                        self.send_header(hk, hv)
                    self.end_headers()
                    if res_body:
                        self.wfile.write(res_body)
                except Exception:
                    pass

            def do_GET(self): self._handle_request("GET")
            def do_POST(self): self._handle_request("POST")
            def do_PUT(self): self._handle_request("PUT")
            def do_DELETE(self): self._handle_request("DELETE")
            def do_PATCH(self): self._handle_request("PATCH")
            def do_HEAD(self): self._handle_request("HEAD")
            def do_OPTIONS(self): self._handle_request("OPTIONS")

        return DhiHTTPHandler

    def net_serve(*args):
        if len(args) < 2:
            return obj_factory['error']("serve() / ސާވަރު() އަށް ޕޯޓަކާއި ހޭންޑްލަރ ވަޒީފާއެއް ދޭންވާނެ")

        port = int(args[0].value) if hasattr(args[0], 'value') else 8080
        handler_fn = args[1]

        options = {}
        if len(args) > 2 and hasattr(args[2], 'pairs'):
            options = dhi_to_py(args[2])

        host = options.get("host", "127.0.0.1")
        background = bool(options.get("background", False))
        max_requests = options.get("max_requests", None)
        silent = bool(options.get("silent", True))

        handler_cls = _create_dhi_http_handler(handler_fn, silent=silent)

        try:
            socketserver.TCPServer.allow_reuse_address = True
            server = socketserver.ThreadingTCPServer((host, port), handler_cls)
        except Exception as e:
            return obj_factory['error'](f"ސާވަރު ފެށުމުގައި މައްސަލައެއް ({host}:{port}): {e}")

        actual_port = server.server_address[1]

        def stop_server(*_):
            try:
                server.shutdown()
                server.server_close()
                return obj_factory['boolean'](True)
            except Exception:
                return obj_factory['boolean'](False)

        server_dict = {
            "port": obj_factory['num'](actual_port),
            "host": obj_factory['string'](host),
            "stop": obj_factory['builtin'](stop_server),
            "close": obj_factory['builtin'](stop_server),
            "ލައްޕާ": obj_factory['builtin'](stop_server),
            "ހުއްޓާ": obj_factory['builtin'](stop_server),
        }
        res_handle = obj_factory['dict'](server_dict)

        if background:
            t = threading.Thread(target=server.serve_forever, daemon=True)
            t.start()
            return res_handle
        else:
            try:
                if max_requests is not None and int(max_requests) > 0:
                    for _ in range(int(max_requests)):
                        server.handle_request()
                else:
                    server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
            return res_handle

    def net_create_router(*args):
        routes = {
            "GET": {},
            "POST": {},
            "PUT": {},
            "DELETE": {},
            "PATCH": {},
            "ALL": {}
        }

        def _add_route(method, r_args):
            if len(r_args) < 2:
                return obj_factory['error'](f"{method}() އަށް މަގަކާއި ވަޒީފާއެއް ދޭންވާނެ")
            path = r_args[0].inspect()
            handler = r_args[1]
            routes[method][path] = handler
            return obj_factory['boolean'](True)

        def r_get(*r_args): return _add_route("GET", r_args)
        def r_post(*r_args): return _add_route("POST", r_args)
        def r_put(*r_args): return _add_route("PUT", r_args)
        def r_delete(*r_args): return _add_route("DELETE", r_args)
        def r_patch(*r_args): return _add_route("PATCH", r_args)
        def r_all(*r_args): return _add_route("ALL", r_args)

        def r_handle(*r_args):
            if not r_args:
                return obj_factory['error']("handle() އަށް އެދުން (request) ދޭންވާނެ")
            req = r_args[0]
            if not hasattr(req, 'pairs'):
                return obj_factory['error']("އެދުމަކީ ރަދީފަކަށް ވާންވާނެ")

            method = req.pairs.get("method") or req.pairs.get("ކަން")
            path = req.pairs.get("path") or req.pairs.get("މަގު")
            m_str = method.inspect() if method else "GET"
            p_str = path.inspect() if path else "/"

            h = routes.get(m_str, {}).get(p_str)
            if not h and p_str.endswith('/') and len(p_str) > 1:
                h = routes.get(m_str, {}).get(p_str[:-1])
            if not h:
                h = routes.get("ALL", {}).get(p_str)
            if not h:
                h = routes.get(m_str, {}).get("*") or routes.get("ALL", {}).get("*")

            if h:
                return call_fn(h, [req])

            return py_to_dhi({
                "status": 404, "ކޯޑު": 404,
                "body": f"Not Found: {m_str} {p_str}",
                "ލިޔުން": f"ނުފެނުނު: {m_str} {p_str}"
            })

        router_dict = {
            # English
            "get": obj_factory['builtin'](r_get),
            "post": obj_factory['builtin'](r_post),
            "put": obj_factory['builtin'](r_put),
            "delete": obj_factory['builtin'](r_delete),
            "patch": obj_factory['builtin'](r_patch),
            "all": obj_factory['builtin'](r_all),
            "handle": obj_factory['builtin'](r_handle),

            # Dhivehi
            "ނަގާ": obj_factory['builtin'](r_get),
            "ފޮނުވާ": obj_factory['builtin'](r_post),
            "ބަދަލުކުރޭ": obj_factory['builtin'](r_put),
            "ފޮހެލާ": obj_factory['builtin'](r_delete),
            "ހުރިހާ": obj_factory['builtin'](r_all),
            "ހިންގާ": obj_factory['builtin'](r_handle),
        }
        return obj_factory['dict'](router_dict)

    def net_response_json(*args):
        if not args:
            return obj_factory['error']("response_json() އަށް ޑޭޓާ ދޭންވާނެ")
        data = dhi_to_py(args[0])
        status = int(args[1].value) if len(args) > 1 and hasattr(args[1], 'value') else 200
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if len(args) > 2 and hasattr(args[2], 'pairs'):
            for k, v in args[2].pairs.items():
                headers[str(k)] = v.inspect() if hasattr(v, 'inspect') else str(v)

        json_str = json.dumps(data, ensure_ascii=False)
        return py_to_dhi({
            "status": status, "ކޯޑު": status,
            "body": json_str, "ލިޔުން": json_str,
            "headers": headers, "ހެޑަރ": headers,
            "json": data, "ޖޭސަން": data
        })

    def net_response_html(*args):
        if not args:
            return obj_factory['error']("response_html() އަށް އެޗްޓީއެމްއެލް ލިޔުމެއް ދޭންވާނެ")
        html_str = args[0].inspect()
        status = int(args[1].value) if len(args) > 1 and hasattr(args[1], 'value') else 200
        headers = {"Content-Type": "text/html; charset=utf-8"}
        if len(args) > 2 and hasattr(args[2], 'pairs'):
            for k, v in args[2].pairs.items():
                headers[str(k)] = v.inspect() if hasattr(v, 'inspect') else str(v)

        return py_to_dhi({
            "status": status, "ކޯޑު": status,
            "body": html_str, "ލިޔުން": html_str,
            "headers": headers, "ހެޑަރ": headers
        })

    def net_response_text(*args):
        if not args:
            return obj_factory['error']("response_text() އަށް ލިޔުމެއް ދޭންވާނެ")
        text_str = args[0].inspect()
        status = int(args[1].value) if len(args) > 1 and hasattr(args[1], 'value') else 200
        headers = {"Content-Type": "text/plain; charset=utf-8"}
        if len(args) > 2 and hasattr(args[2], 'pairs'):
            for k, v in args[2].pairs.items():
                headers[str(k)] = v.inspect() if hasattr(v, 'inspect') else str(v)

        return py_to_dhi({
            "status": status, "ކޯޑު": status,
            "body": text_str, "ލިޔުން": text_str,
            "headers": headers, "ހެޑަރ": headers
        })

    network_module = {
        # Dhivehi
        "ނަގާ": obj_factory['builtin'](net_http_get),
        "ފޮނުވާ": obj_factory['builtin'](net_http_post),
        "ބަދަލުކުރޭ": obj_factory['builtin'](net_http_put),
        "ފޮހެލާ": obj_factory['builtin'](net_http_delete),
        "ޖޭސަން_ކިޔާ": obj_factory['builtin'](net_json_parse),
        "ޖޭސަން_ހަދާ": obj_factory['builtin'](net_json_stringify),
        "ޔޫއާރްއެލް_އެންކޯޑް": obj_factory['builtin'](net_url_encode),
        "ޔޫއާރްއެލް_ޑީކޯޑް": obj_factory['builtin'](net_url_decode),
        "ސާވަރު": obj_factory['builtin'](net_serve),
        "ރައުޓަރ_ހަދާ": obj_factory['builtin'](net_create_router),
        "ރައުޓަރ": obj_factory['builtin'](net_create_router),
        "ޖޭސަން_ޖަވާބު": obj_factory['builtin'](net_response_json),
        "އެޗްޓީއެމްއެލް_ޖަވާބު": obj_factory['builtin'](net_response_html),
        "ލިޔުން_ޖަވާބު": obj_factory['builtin'](net_response_text),

        # English
        "get": obj_factory['builtin'](net_http_get),
        "post": obj_factory['builtin'](net_http_post),
        "put": obj_factory['builtin'](net_http_put),
        "delete": obj_factory['builtin'](net_http_delete),
        "parse_json": obj_factory['builtin'](net_json_parse),
        "stringify_json": obj_factory['builtin'](net_json_stringify),
        "url_encode": obj_factory['builtin'](net_url_encode),
        "url_decode": obj_factory['builtin'](net_url_decode),
        "serve": obj_factory['builtin'](net_serve),
        "create_router": obj_factory['builtin'](net_create_router),
        "router": obj_factory['builtin'](net_create_router),
        "response_json": obj_factory['builtin'](net_response_json),
        "response_html": obj_factory['builtin'](net_response_html),
        "response_text": obj_factory['builtin'](net_response_text),
    }

    # =========================================================================
    # 6. ނަކަތް (Maldivian Nakaiy Calendar Module - "nakaiy")
    # =========================================================================
    NAKAIY_LIST = [
        # --- Hulhangu (South-West Monsoon) - 18 Nakaiy ---
        {"ނަން": "އައްސިދަ", "name": "Assidha", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "04-08", "ނިމެނީ": "04-21", "ދިގުމިން": 14, "ސިފަ": "ވިއްސާރަ، ގުގުރުން އަދި ކަނޑުގަދަ"},
        {"ނަން": "ބުރަނަ", "name": "Burana", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "04-22", "ނިމެނީ": "05-05", "ދިގުމިން": 14, "ސިފަ": "ކޮޅިގަނޑު، ވައިގަދަވުން"},
        {"ނަން": "ކެތި", "name": "Kethi", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "05-06", "ނިމެނީ": "05-19", "ދިގުމިން": 14, "ސިފަ": "ވިލާ ބޯވުން، ވާރޭ ވެހުން"},
        {"ނަން": "ރޯނު", "name": "Roanu", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "05-20", "ނިމެނީ": "06-02", "ދިގުމިން": 14, "ސިފަ": "ވައި ބާރުވެ ބޮޑެތި ރާޅުތައް ނެގުން"},
        {"ނަން": "މިއަހެލި", "name": "Miaheli", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "06-03", "ނިމެނީ": "06-16", "ދިގުމިން": 14, "ސިފަ": "ކުއްލިއަކަށް އަންނަ ބާރު ވިއްސާރަ"},
        {"ނަން": "އަދަ", "name": "Adha", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "06-17", "ނިމެނީ": "06-30", "ދިގުމިން": 14, "ސިފަ": "ވައިބާރުވެ ދޭތެރެދޭތެރެއިން ވާރޭވެހުން"},
        {"ނަން": "ފުނަ", "name": "Funa", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "07-01", "ނިމެނީ": "07-14", "ދިގުމިން": 14, "ސިފަ": "ކަނޑު ގަދަވެ ވައި ބާރުވުން"},
        {"ނަން": "ފުސް", "name": "Fus", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "07-15", "ނިމެނީ": "07-27", "ދިގުމިން": 13, "ސިފަ": "ވިލާ ބޯވެ ބަނަކޮށް އޮތުން"},
        {"ނަން": "އަހުލިހަ", "name": "Ahuliha", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "07-28", "ނިމެނީ": "08-09", "ދިގުމިން": 13, "ސިފަ": "މަޑުމައިތިރި ކަނޑު، ދޭތެރެއިން ވާރޭ"},
        {"ނަން": "މާ", "name": "Maa", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "08-10", "ނިމެނީ": "08-22", "ދިގުމިން": 13, "ސިފަ": "މަޑު ވައިރޯޅި، އުޑުމަތި ސާފުވުން"},
        {"ނަން": "ފުރަ", "name": "Fura", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "08-23", "ނިމެނީ": "09-04", "ދިގުމިން": 13, "ސިފަ": "އަރިއަރިޔަށް ވާރޭ ވެހުން"},
        {"ނަން": "އުތުރަ", "name": "Uthura", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "09-05", "ނިމެނީ": "09-17", "ދިގުމިން": 13, "ސިފަ": "ބޯކޮށް ވާރޭވެހި ވައި ބާރުވުން"},
        {"ނަން": "އަތަ", "name": "Atha", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "09-18", "ނިމެނީ": "09-30", "ދިގުމިން": 13, "ސިފަ": "އަވިދޭ، ދޭތެރެއިން ކުއްލި ވިއްސާރަ"},
        {"ނަން": "ހިތަ", "name": "Hitha", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "10-01", "ނިމެނީ": "10-13", "ދިގުމިން": 13, "ސިފަ": "މަޑު ވައި، މަސްވެރިކަން ރަނގަޅުވުން"},
        {"ނަން": "ހޭ", "name": "Hey", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "10-14", "ނިމެނީ": "10-26", "ދިގުމިން": 13, "ސިފަ": "ގަދަ ވައި، މޫސުމީ ބަދަލުތައް"},
        {"ނަން": "ވިހާ", "name": "Vihaa", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "10-27", "ނިމެނީ": "11-09", "ދިގުމިން": 14, "ސިފަ": "މަޑު ވައި، މަސްވެރިކަން ވަރަށް ރަނގަޅު"},
        {"ނަން": "ނޮރޮ", "name": "Noro", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "11-10", "ނިމެނީ": "11-22", "ދިގުމިން": 13, "ސިފަ": "ފުސް ވިލާ، ލުއި ވިއްސާރަ"},
        {"ނަން": "ދޮށަ", "name": "Dhosha", "މޫސުން": "ހުޅަނގު", "monsoon": "Hulhangu", "ފެށެނީ": "11-23", "ނިމެނީ": "12-06", "ދިގުމިން": 14, "ސިފަ": "ހުޅަނގު މޫސުމުގެ އެންމެ ފަހު ނަކަތް"},

        # --- Iruvai (North-East Monsoon) - 9 Nakaiy ---
        {"ނަން": "މުލަ", "name": "Mula", "މޫސުން": "އިރުވައި", "monsoon": "Iruvai", "ފެށެނީ": "12-07", "ނިމެނީ": "12-19", "ދިގުމިން": 13, "ސިފަ": "އިރުވައި މޫސުމުގެ ފެށުން، ގަދަ ވައި"},
        {"ނަން": "ފުރަހަޅަ", "name": "Furahala", "މޫސުން": "އިރުވައި", "monsoon": "Iruvai", "ފެށެނީ": "12-20", "ނިމެނީ": "01-01", "ދިގުމިން": 13, "ސިފަ": "ވައި ބާރުވެ ކަނޑު ގަދަވުން"},
        {"ނަން": "އުތުރުހަޅަ", "name": "Uthuruhala", "މޫސުން": "އިރުވައި", "monsoon": "Iruvai", "ފެށެނީ": "01-02", "ނިމެނީ": "01-14", "ދިގުމިން": 13, "ސިފަ": "ސާފު އުޑުމަތި، ފިނި ރޯޅި"},
        {"ނަން": "ހުވަން", "name": "Huvan", "މޫސުން": "އިރުވައި", "monsoon": "Iruvai", "ފެށެނީ": "01-15", "ނިމެނީ": "01-27", "ދިގުމިން": 13, "ސިފަ": "ހިމޭން ކަނޑު، އަވިގަދަ ރީތި ދުވަސްތައް"},
        {"ނަން": "ދިނަޝަ", "name": "Dhinasha", "މޫސުން": "އިރުވައި", "monsoon": "Iruvai", "ފެށެނީ": "01-28", "ނިމެނީ": "02-09", "ދިގުމިން": 13, "ސިފަ": "މަޑު ވައި، ހިތްފަސޭހަ މޫސުން"},
        {"ނަން": "ހިޔަވިހާ", "name": "Hiyavihaa", "މޫސުން": "އިރުވައި", "monsoon": "Iruvai", "ފެށެނީ": "02-10", "ނިމެނީ": "02-22", "ދިގުމިން": 13, "ސިފަ": "ވަރަށް ހިމޭން މަޑު ކަނޑު، ހޫނުގަދަ"},
        {"ނަން": "ވައިވައި", "name": "Vaivai", "މޫސުން": "އިރުވައި", "monsoon": "Iruvai", "ފެށެނީ": "02-23", "ނިމެނީ": "03-07", "ދިގުމިން": 13, "ސިފަ": "އެކި ދިމަދިމާއިން ވައި ޖެހުން"},
        {"ނަން": "ފަސްބުރުނު", "name": "Fasburunu", "މޫސުން": "އިރުވައި", "monsoon": "Iruvai", "ފެށެނީ": "03-08", "ނިމެނީ": "03-20", "ދިގުމިން": 13, "ސިފަ": "ކުއްލި ވިއްސާރަ، ހޫނުގަދަވުން"},
        {"ނަން": "ފޭބުރުނު", "name": "Faeburunu", "މޫސުން": "އިރުވައި", "monsoon": "Iruvai", "ފެށެނީ": "03-21", "ނިމެނީ": "04-07", "ދިގުމިން": 18, "ސިފަ": "އިރުވައި މޫސުމުގެ ނިމުން، މަޑުމައިތިރި"}
    ]

    def _find_nakaiy_by_date(m: int, d: int) -> Dict[str, Any]:
        target = f"{m:02d}-{d:02d}"
        for n in NAKAIY_LIST:
            start = n["ފެށެނީ"]
            end = n["ނިމެނީ"]
            if start <= end:
                if start <= target <= end:
                    return n
            else:
                if target >= start or target <= end:
                    return n
        return NAKAIY_LIST[0]

    def nakaiy_today(*args):
        now = datetime.now()
        nak = _find_nakaiy_by_date(now.month, now.day)
        return py_to_dhi(nak)

    def nakaiy_lookup(*args):
        if len(args) < 2:
            return obj_factory['error']("ނަކަތް_ހޯދާ() / lookup() އަށް މަހާއި ދުވަސް ދޭންވާނެ")
        m = int(args[0].value) if hasattr(args[0], 'value') else int(args[0])
        d = int(args[1].value) if hasattr(args[1], 'value') else int(args[1])
        nak = _find_nakaiy_by_date(m, d)
        return py_to_dhi(nak)

    def nakaiy_all(*args):
        return py_to_dhi(NAKAIY_LIST)

    def nakaiy_monsoon(*args):
        if args and hasattr(args[0], 'value'):
            m = int(args[0].value)
            d = int(args[1].value) if len(args) > 1 and hasattr(args[1], 'value') else 1
            nak = _find_nakaiy_by_date(m, d)
        else:
            now = datetime.now()
            nak = _find_nakaiy_by_date(now.month, now.day)
        return obj_factory['string'](nak["މޫސުން"])

    def nakaiy_day(*args):
        if args and hasattr(args[0], 'value'):
            m = int(args[0].value)
            d = int(args[1].value) if len(args) > 1 and hasattr(args[1], 'value') else 1
            current_date = date(datetime.now().year, m, d)
            nak = _find_nakaiy_by_date(m, d)
        else:
            now = datetime.now()
            current_date = now.date()
            nak = _find_nakaiy_by_date(now.month, now.day)

        start_m, start_d = map(int, nak["ފެށެނީ"].split("-"))
        y = current_date.year
        if start_m == 12 and current_date.month == 1:
            start_date = date(y - 1, start_m, start_d)
        else:
            start_date = date(y, start_m, start_d)

        day_num = (current_date - start_date).days + 1
        return obj_factory['num'](max(1, day_num))

    nakaiy_module = {
        # Dhivehi
        "މިއަދުގެ_ނަކަތް": obj_factory['builtin'](nakaiy_today),
        "ނަކަތް_ހޯދާ": obj_factory['builtin'](nakaiy_lookup),
        "ހުރިހާ_ނަކަތް": obj_factory['builtin'](nakaiy_all),
        "މޫސުން": obj_factory['builtin'](nakaiy_monsoon),
        "ނަކަތް_ދުވަސް": obj_factory['builtin'](nakaiy_day),

        # English
        "today": obj_factory['builtin'](nakaiy_today),
        "lookup": obj_factory['builtin'](nakaiy_lookup),
        "all": obj_factory['builtin'](nakaiy_all),
        "monsoon": obj_factory['builtin'](nakaiy_monsoon),
        "nakaiy_day": obj_factory['builtin'](nakaiy_day),
        "day": obj_factory['builtin'](nakaiy_day),
    }

    # =========================================================================
    # 7. ނަމާދު (Maldivian Prayer Times & Hijri Calendar - "prayer")
    # =========================================================================
    ATOLL_COORDS = {
        "މާލެ": (4.1755, 73.5093),
        "Male": (4.1755, 73.5093),
        "ހުޅުމާލެ": (4.2133, 73.5414),
        "Hulhumale": (4.2133, 73.5414),
        "ވިލިމާލެ": (4.1736, 73.4844),
        "Vilimale": (4.1736, 73.4844),
        "އައްޑޫ": (-0.6300, 73.1600),
        "Addu": (-0.6300, 73.1600),
        "ފުވައްމުލައް": (-0.2980, 73.4240),
        "Fuvahmulah": (-0.2980, 73.4240),
        "ކުޅުދުއްފުށި": (6.6220, 73.0700),
        "Kulhudhuffushi": (6.6220, 73.0700),
        "ތިނަދޫ": (0.5310, 72.9960),
        "Thinadhoo": (0.5310, 72.9960),
        "ހއ": (6.9000, 72.9000), "HA": (6.9000, 72.9000),
        "ހދ": (6.6000, 73.0000), "HDh": (6.6000, 73.0000),
        "ށ": (6.2000, 73.1000),  "Sh": (6.2000, 73.1000),
        "ނ": (5.8000, 73.3000),  "N": (5.8000, 73.3000),
        "ރ": (5.6000, 72.9000),  "R": (5.6000, 72.9000),
        "ބ": (5.1000, 72.9000),  "B": (5.1000, 72.9000),
        "ޅ": (5.4000, 73.6000),  "Lh": (5.4000, 73.6000),
        "ކ": (4.4000, 73.5000),  "K": (4.4000, 73.5000),
        "އއ": (4.0000, 72.8000), "AA": (4.0000, 72.8000),
        "އދ": (3.6000, 72.8000), "ADh": (3.6000, 72.8000),
        "ވ": (3.4000, 73.5000),  "V": (3.4000, 73.5000),
        "މ": (2.9000, 73.5000),  "M": (2.9000, 73.5000),
        "ފ": (3.1000, 72.9000),  "F": (3.1000, 72.9000),
        "ދ": (2.7000, 72.9000),  "Dh": (2.7000, 72.9000),
        "ތ": (2.2000, 73.1000),  "Th": (2.2000, 73.1000),
        "ލ": (1.9000, 73.4000),  "L": (1.9000, 73.4000),
        "ގއ": (0.7000, 73.4000), "GA": (0.7000, 73.4000),
        "ގދ": (0.4000, 73.1000), "GDh": (0.4000, 73.1000),
        "ޏ": (-0.3000, 73.4200), "Gn": (-0.3000, 73.4200),
        "ސ": (-0.6300, 73.1600), "S": (-0.6300, 73.1600),
    }

    HIJRI_MONTHS = [
        "މުޙައްރަމް", "ޞަފަރު", "ރަބީޢުލްއައްވަލް", "ރަބީޢުލްއާޚިރު",
        "ޖުމާދަލްއޫލާ", "ޖުމާދަލްއާޚިރާ", "ރަޖަބު", "ޝަޢުބާން",
        "ރަމަޟާން", "ޝައްވާލް", "ޛުލްޤަޢިދާ", "ޛުލްޙިއްޖާ"
    ]

    def _calc_prayer_times(lat: float, lon: float, year: int, month: int, day: int) -> Dict[str, str]:
        d = date(year, month, day)
        day_of_year = d.timetuple().tm_yday
        gamma = 2 * math.pi / 365 * (day_of_year - 1)

        eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                           - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
        decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) \
               - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)

        lat_rad = math.radians(lat)
        timezone = 5.0
        solar_noon = 12 + (4 * (timezone * 15 - lon) - eqtime) / 60

        def _hour_angle(angle_deg: float) -> float:
            rad = math.radians(angle_deg)
            cos_ha = (math.sin(rad) - math.sin(lat_rad) * math.sin(decl)) / (math.cos(lat_rad) * math.cos(decl))
            cos_ha = max(-1.0, min(1.0, cos_ha))
            return math.degrees(math.acos(cos_ha)) / 15.0

        ha_fajr = _hour_angle(-18.0)
        t_fajr = solar_noon - ha_fajr

        ha_sunrise = _hour_angle(-0.833)
        t_sunrise = solar_noon - ha_sunrise

        t_dhuhr = solar_noon + 2.0 / 60.0

        noon_alt = math.pi / 2 - abs(lat_rad - decl)
        noon_shadow = 1.0 / math.tan(noon_alt) if math.tan(noon_alt) != 0 else 0
        asr_alt = math.atan(1.0 / (1.0 + noon_shadow))
        ha_asr = _hour_angle(math.degrees(asr_alt))
        t_asr = solar_noon + ha_asr

        t_sunset = solar_noon + ha_sunrise
        t_maghrib = t_sunset + 2.0 / 60.0
        t_isha = solar_noon + ha_fajr

        def fmt_h(h_val: float) -> str:
            h_val = h_val % 24
            hours = int(h_val)
            mins = int(round((h_val - hours) * 60))
            if mins == 60:
                hours = (hours + 1) % 24
                mins = 0
            return f"{hours:02d}:{mins:02d}"

        return {
            "ފަތިސް": fmt_h(t_fajr), "Fajr": fmt_h(t_fajr),
            "އިރުއަރާ": fmt_h(t_sunrise), "Sunrise": fmt_h(t_sunrise),
            "މެންދުރު": fmt_h(t_dhuhr), "Dhuhr": fmt_h(t_dhuhr),
            "ޢަޞުރު": fmt_h(t_asr), "Asr": fmt_h(t_asr),
            "މަޣްރިބް": fmt_h(t_maghrib), "Maghrib": fmt_h(t_maghrib),
            "ޢިޝާ": fmt_h(t_isha), "Isha": fmt_h(t_isha)
        }

    def prayer_today(*args):
        place = args[0].inspect() if args else "މާލެ"
        lat, lon = ATOLL_COORDS.get(place, ATOLL_COORDS["މާލެ"])
        now = datetime.now()
        res = _calc_prayer_times(lat, lon, now.year, now.month, now.day)
        return py_to_dhi(res)

    def prayer_lookup(*args):
        place = args[0].inspect() if args else "މާލެ"
        lat, lon = ATOLL_COORDS.get(place, ATOLL_COORDS["މާލެ"])
        y = int(args[1].value) if len(args) > 1 and hasattr(args[1], 'value') else datetime.now().year
        m = int(args[2].value) if len(args) > 2 and hasattr(args[2], 'value') else datetime.now().month
        d = int(args[3].value) if len(args) > 3 and hasattr(args[3], 'value') else datetime.now().day
        res = _calc_prayer_times(lat, lon, y, m, d)
        return py_to_dhi(res)

    def prayer_next(*args):
        place = args[0].inspect() if args else "މާލެ"
        lat, lon = ATOLL_COORDS.get(place, ATOLL_COORDS["މާލެ"])
        now = datetime.now()
        times = _calc_prayer_times(lat, lon, now.year, now.month, now.day)

        cur_min = now.hour * 60 + now.minute
        order = [("ފަތިސް", "Fajr"), ("މެންދުރު", "Dhuhr"), ("ޢަޞުރު", "Asr"), ("މަޣްރިބް", "Maghrib"), ("ޢިޝާ", "Isha")]

        next_dhi, next_eng = None, None
        rem_minutes = 0

        for p_dhi, p_eng in order:
            t_str = times[p_dhi]
            parts = t_str.split(":")
            p_min = int(parts[0]) * 60 + int(parts[1])
            if p_min > cur_min:
                next_dhi = p_dhi
                next_eng = p_eng
                rem_minutes = p_min - cur_min
                break

        if not next_dhi:
            tomorrow = datetime.fromtimestamp(time.time() + 86400)
            t_times = _calc_prayer_times(lat, lon, tomorrow.year, tomorrow.month, tomorrow.day)
            f_parts = t_times["ފަތިސް"].split(":")
            f_min = int(f_parts[0]) * 60 + int(f_parts[1])
            rem_minutes = (1440 - cur_min) + f_min
            next_dhi = "ފަތިސް"
            next_eng = "Fajr"

        return py_to_dhi({
            "ނަމާދު": next_dhi, "prayer": next_eng,
            "ވަގުތު": times.get(next_dhi, "05:00"), "time": times.get(next_dhi, "05:00"),
            "ބާކީ_މިނިޓް": rem_minutes, "remaining_minutes": rem_minutes
        })

    def prayer_atolls(*args):
        # Return unique Dhivehi atoll names
        atoll_names = [k for k in ATOLL_COORDS.keys() if any('\u0780' <= c <= '\u07BF' for c in k)]
        return py_to_dhi(atoll_names)

    def _calc_hijri(year: int, month: int, day: int):
        Y, M, D = year, month, day
        if M <= 2:
            Y -= 1
            M += 12
        A = Y // 100
        B = 2 - A + (A // 4)
        jdn = int(365.25 * (Y + 4716)) + int(30.6001 * (M + 1)) + D + B - 1524
        l = jdn - 1948440 + 10632
        n = int((l - 1) / 10631)
        l = l - 10631 * n + 354
        j = (int((10985 - l) / 5316)) * (int((50 * l) / 17719)) + (int(l / 5670)) * (int((43 * l) / 15238))
        l = l - (int((30 - j) / 15)) * (int((17719 * j) / 50)) - (int(j / 16)) * (int((15238 * j) / 43)) + 29
        hijri_month = int((24 * l) / 709)
        hijri_day = l - int((709 * hijri_month) / 24)
        hijri_year = 30 * n + j - 30
        h_month_name = HIJRI_MONTHS[(hijri_month - 1) % 12]
        return {
            "އަހަރު": hijri_year, "year": hijri_year,
            "މަސް": h_month_name, "month": h_month_name,
            "މަސް_ނަންބަރު": hijri_month, "month_num": hijri_month,
            "ދުވަސް": hijri_day, "day": hijri_day,
            "ތާރީޚް": f"{hijri_day} {h_month_name} {hijri_year}",
            "formatted": f"{hijri_day} {h_month_name} {hijri_year}"
        }

    def prayer_hijri(*args):
        now = datetime.now()
        y = int(args[0].value) if len(args) > 0 and hasattr(args[0], 'value') else now.year
        m = int(args[1].value) if len(args) > 1 and hasattr(args[1], 'value') else now.month
        d = int(args[2].value) if len(args) > 2 and hasattr(args[2], 'value') else now.day
        res = _calc_hijri(y, m, d)
        return py_to_dhi(res)

    prayer_module = {
        # Dhivehi
        "މިއަދުގެ_ވަގުތު": obj_factory['builtin'](prayer_today),
        "ވަގުތު_ހޯދާ": obj_factory['builtin'](prayer_lookup),
        "ދެން_އޮތް_ނަމާދު": obj_factory['builtin'](prayer_next),
        "ހުރިހާ_ރަށްތައް": obj_factory['builtin'](prayer_atolls),
        "ހިޖުރީ_ތާރީޚް": obj_factory['builtin'](prayer_hijri),

        # English
        "today": obj_factory['builtin'](prayer_today),
        "lookup": obj_factory['builtin'](prayer_lookup),
        "next_prayer": obj_factory['builtin'](prayer_next),
        "atolls": obj_factory['builtin'](prayer_atolls),
        "hijri_date": obj_factory['builtin'](prayer_hijri),
        "hijri": obj_factory['builtin'](prayer_hijri),
    }

    # =========================================================================
    # 8. ތާނަ (Thaana & Dhivehi Language Module - "thaana")
    # =========================================================================
    ONES_DHIVEHI = [
        "", "އެއް", "ދެ", "ތިން", "ހަތަރު", "ފަސް", "ހަ", "ހަތް", "އަށް", "ނުވަ"
    ]

    ONES_STANDALONE = [
        "ސުމެއް", "އެކެއް", "ދޭއް", "ތިނެއް", "ހަތަރެއް", "ފަހެއް", "ހައެއް", "ހަތެއް", "އަށެއް", "ނުވައެއް"
    ]

    TEENS = [
        "ދިހައެއް", "އެގާރަ", "ބާރަ", "ތޭރަ", "ސާދަ", "ފަނަރަ", "ސޯޅަ", "ސަތާރަ", "އަށާރަ", "ނަވާރަ"
    ]

    TENS = [
        "", "ދިހަ", "ވިހި", "ތިރީސް", "ސާޅީސް", "ފަންސާސް", "ފަސްދޮޅަސް", "ހައްދިހަ", "އައްޑިހަ", "ނުވަދިހަ"
    ]

    TWENTIES = [
        "ވިހި", "އެކާވީސް", "ބާވީސް", "ތޭވީސް", "ސައުވީސް", "ފަންސަވީސް", "ސައްބީސް", "ސަތާވީސް", "އަށާވީސް", "ނަވާވީސް"
    ]

    THAANA_ALPHABET = [
        'ހ', 'ށ', 'ނ', 'ރ', 'ބ', 'ޅ', 'ކ', 'އ', 'ވ', 'މ', 'ފ', 'ދ', 'ތ', 'ލ', 'ގ', 'ޏ', 'ސ', 'ޑ', 'ޒ', 'ޓ', 'ޔ', 'ޕ', 'ޖ', 'ޗ'
    ]
    THAANA_ORDER_MAP = {char: idx for idx, char in enumerate(THAANA_ALPHABET)}

    def _number_to_dhivehi(n: int) -> str:
        if n < 0:
            return "މައިނަސް " + _number_to_dhivehi(-n)
        if n == 0:
            return ONES_STANDALONE[0]
        if n < 10:
            return ONES_STANDALONE[n]
        if n < 20:
            return TEENS[n - 10]
        if n < 30:
            return TWENTIES[n - 20]
        if n < 100:
            rem = n % 10
            base = TENS[n // 10]
            if rem == 0:
                return base
            prefix = ONES_DHIVEHI[rem]
            return f"{prefix}{base}"

        if n < 1000:
            h = n // 100
            rem = n % 100
            h_str = "ސަތޭކަ" if h == 1 else f"{ONES_DHIVEHI[h]}ސަތޭކަ" if h != 2 else "ދުއިސައްތަ"
            if rem == 0:
                return h_str
            return f"{h_str} {_number_to_dhivehi(rem)}"

        if n < 1000000:
            th = n // 1000
            rem = n % 1000
            th_str = f"{_number_to_dhivehi(th)} ހާސް"
            if rem == 0:
                return th_str
            return f"{th_str} {_number_to_dhivehi(rem)}"

        if n < 1000000000:
            mil = n // 1000000
            rem = n % 1000000
            mil_str = f"{_number_to_dhivehi(mil)} މިލިއަން"
            if rem == 0:
                return mil_str
            return f"{mil_str} {_number_to_dhivehi(rem)}"

        return str(n)

    def num_to_dhivehi_fn(*args):
        if not args:
            return obj_factory['error']("އަދަދު_ބަހަށް() / to_words() އަށް އަދަދެއް ދޭންވާނެ")
        val = int(args[0].value) if hasattr(args[0], 'value') else int(args[0])
        return obj_factory['string'](_number_to_dhivehi(val))

    def thaana_collation_key(word: str):
        key = []
        for ch in word:
            if ch in THAANA_ORDER_MAP:
                key.append(THAANA_ORDER_MAP[ch])
            elif '\u0780' <= ch <= '\u07BF':
                key.append(100 + ord(ch))
            else:
                key.append(200 + ord(ch))
        return key

    def thaana_sort_fn(*args):
        if not args:
            return obj_factory['error']("ތާނަ_ތަރުތީބު() / sort() އަށް ލިސްޓެއް ދޭންވާނެ")
        raw_list = dhi_to_py(args[0])
        if not isinstance(raw_list, list):
            return obj_factory['error']("ތާނަ_ތަރުތީބު() / sort() އަށް ލިސްޓެއް ދޭންވާނެ")

        sorted_list = sorted(raw_list, key=lambda s: thaana_collation_key(str(s)))
        return py_to_dhi(sorted_list)

    def thaana_alphabet_fn(*args):
        return py_to_dhi(THAANA_ALPHABET)

    def thaana_is_thaana(*args):
        if not args:
            return obj_factory['boolean'](False)
        text = args[0].inspect()
        has_thaana = any('\u0780' <= ch <= '\u07BF' for ch in text)
        return obj_factory['boolean'](has_thaana)

    def thaana_strip_fili(*args):
        if not args:
            return obj_factory['string']("")
        text = args[0].inspect()
        stripped = "".join(ch for ch in text if not ('\u07A6' <= ch <= '\u07B0'))
        return obj_factory['string'](stripped)

    def thaana_currency_mvr(*args):
        if not args:
            return obj_factory['error']("ރުފިޔާ() / currency_mvr() އަށް އަދަދެއް ދޭންވާނެ")
        val = float(args[0].value) if hasattr(args[0], 'value') else float(args[0])
        symbol = args[1].inspect() if len(args) > 1 else "ރ."
        return obj_factory['string'](f"{symbol} {val:,.2f}")

    def thaana_to_latin(*args):
        if not args:
            return obj_factory['string']("")
        text = args[0].inspect()
        c_map = {
            'ހ': 'h', 'ށ': 'sh', 'ނ': 'n', 'ރ': 'r', 'ބ': 'b',
            'ޅ': 'lh', 'ކ': 'k', 'އ': '', 'ވ': 'v', 'މ': 'm',
            'ފ': 'f', 'ދ': 'dh', 'ތ': 'th', 'ލ': 'l', 'ގ': 'g',
            'ޏ': 'gn', 'ސ': 's', 'ޑ': 'd', 'ޒ': 'z', 'ޓ': 't',
            'ޔ': 'y', 'ޕ': 'p', 'ޖ': 'j', 'ޗ': 'ch',
            'ޘ': 'th', 'ޙ': 'h', 'ޚ': 'kh', 'ޛ': 'dh', 'ޜ': 'z',
            'ޝ': 'sh', 'ޞ': 's', 'ޟ': 'd', 'ޠ': 't', 'ޡ': 'z',
            'ޢ': '', 'ޣ': 'gh', 'ޤ': 'q', 'ޥ': 'w'
        }
        f_map = {
            '\u07A6': 'a', '\u07A7': 'aa', '\u07A8': 'i', '\u07A9': 'ee',
            '\u07AA': 'u', '\u07AB': 'oo', '\u07AC': 'e', '\u07AD': 'ey',
            '\u07AE': 'o', '\u07AF': 'oa', '\u07B0': ''
        }
        res = []
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if ch in c_map:
                c = c_map[ch]
                if i + 1 < n and text[i+1] in f_map:
                    f = f_map[text[i+1]]
                    if text[i+1] == '\u07B0' and ch == 'އ':
                        if i + 2 < n and text[i+2] in c_map and c_map[text[i+2]]:
                            c = c_map[text[i+2]][0]
                        else:
                            c = "'"
                    res.append(c + f)
                    i += 2
                else:
                    res.append(c)
                    i += 1
            elif ch in f_map:
                res.append(f_map[ch])
                i += 1
            else:
                res.append(ch)
                i += 1
        return obj_factory['string'](''.join(res))

    thaana_math_module = {
        # Dhivehi
        "އަދަދު_ބަހަށް": obj_factory['builtin'](num_to_dhivehi_fn),
        "ތާނަ_ތަރުތީބު": obj_factory['builtin'](thaana_sort_fn),
        "ތާނަ_އަކުރުތައް": obj_factory['builtin'](thaana_alphabet_fn),
        "ތާނަތޯ": obj_factory['builtin'](thaana_is_thaana),
        "ފިލި_ފޮހޭ": obj_factory['builtin'](thaana_strip_fili),
        "ރުފިޔާ": obj_factory['builtin'](thaana_currency_mvr),
        "ލެޓިން_ބަދަލު": obj_factory['builtin'](thaana_to_latin),

        # English
        "number_to_words": obj_factory['builtin'](num_to_dhivehi_fn),
        "to_words": obj_factory['builtin'](num_to_dhivehi_fn),
        "sort": obj_factory['builtin'](thaana_sort_fn),
        "alphabet": obj_factory['builtin'](thaana_alphabet_fn),
        "is_thaana": obj_factory['builtin'](thaana_is_thaana),
        "strip_fili": obj_factory['builtin'](thaana_strip_fili),
        "currency_mvr": obj_factory['builtin'](thaana_currency_mvr),
        "mvr": obj_factory['builtin'](thaana_currency_mvr),
        "to_latin": obj_factory['builtin'](thaana_to_latin),
        "latin": obj_factory['builtin'](thaana_to_latin),
    }

    # =========================================================================
    # 9. ކްރިޕްޓޯ (Cryptography & Security Module - "crypto") [NEW]
    # =========================================================================
    def crypto_sha256(*args):
        if not args:
            return obj_factory['error']("sha256() އަށް ލިޔުމެއް ދޭންވާނެ")
        raw = args[0].inspect()
        return obj_factory['string'](hashlib.sha256(raw.encode('utf-8')).hexdigest())

    def crypto_sha512(*args):
        if not args:
            return obj_factory['error']("sha512() އަށް ލިޔުމެއް ދޭންވާނެ")
        raw = args[0].inspect()
        return obj_factory['string'](hashlib.sha512(raw.encode('utf-8')).hexdigest())

    def crypto_md5(*args):
        if not args:
            return obj_factory['error']("md5() އަށް ލިޔުމެއް ދޭންވާނެ")
        raw = args[0].inspect()
        return obj_factory['string'](hashlib.md5(raw.encode('utf-8')).hexdigest())

    def crypto_hmac_sha256(*args):
        if len(args) < 2:
            return obj_factory['error']("hmac() އަށް ތަޅަކާއި މެސެޖެއް ދޭންވާނެ")
        key = args[0].inspect().encode('utf-8')
        msg = args[1].inspect().encode('utf-8')
        return obj_factory['string'](hmac.new(key, msg, hashlib.sha256).hexdigest())

    def crypto_base64_encode(*args):
        if not args:
            return obj_factory['error']("base64_encode() އަށް ލިޔުމެއް ދޭންވާނެ")
        raw = args[0].inspect().encode('utf-8')
        return obj_factory['string'](base64.b64encode(raw).decode('ascii'))

    def crypto_base64_decode(*args):
        if not args:
            return obj_factory['error']("base64_decode() އަށް ލިޔުމެއް ދޭންވާނެ")
        raw = args[0].inspect().encode('ascii')
        try:
            return obj_factory['string'](base64.b64decode(raw).decode('utf-8', errors='replace'))
        except Exception as e:
            return obj_factory['error'](f"base64 ޑީކޯޑް ކުރުމުގައި މައްސަލައެއް: {e}")

    def crypto_random_token(*args):
        length = int(args[0].value) if args and hasattr(args[0], 'value') else 16
        return obj_factory['string'](secrets.token_hex(length))

    crypto_module = {
        # Dhivehi
        "އެސްއެޗްއޭ256": obj_factory['builtin'](crypto_sha256),
        "އެސްއެޗްއޭ512": obj_factory['builtin'](crypto_sha512),
        "އެމްޑީ5": obj_factory['builtin'](crypto_md5),
        "އެޗްމެކް": obj_factory['builtin'](crypto_hmac_sha256),
        "ބޭސް64_އެންކޯޑް": obj_factory['builtin'](crypto_base64_encode),
        "ބޭސް64_ޑީކޯޑް": obj_factory['builtin'](crypto_base64_decode),
        "ރެންޑަމް_ޓޯކަން": obj_factory['builtin'](crypto_random_token),

        # English
        "sha256": obj_factory['builtin'](crypto_sha256),
        "sha512": obj_factory['builtin'](crypto_sha512),
        "md5": obj_factory['builtin'](crypto_md5),
        "hmac_sha256": obj_factory['builtin'](crypto_hmac_sha256),
        "hmac": obj_factory['builtin'](crypto_hmac_sha256),
        "base64_encode": obj_factory['builtin'](crypto_base64_encode),
        "b64encode": obj_factory['builtin'](crypto_base64_encode),
        "base64_decode": obj_factory['builtin'](crypto_base64_decode),
        "b64decode": obj_factory['builtin'](crypto_base64_decode),
        "random_token": obj_factory['builtin'](crypto_random_token),
        "token": obj_factory['builtin'](crypto_random_token),
    }

    # =========================================================================
    # 10. ރެގެކްސް (Regular Expressions Module - "regex") [NEW]
    # =========================================================================
    def regex_match(*args):
        if len(args) < 2:
            return obj_factory['error']("match() އަށް ޕެޓާނަކާއި ލިޔުމެއް ދޭންވާނެ")
        pat = args[0].inspect()
        text = args[1].inspect()
        try:
            m = re.match(pat, text)
            return obj_factory['boolean'](bool(m))
        except Exception as e:
            return obj_factory['error'](f"ރެގެކްސް މައްސަލައެއް: {e}")

    def regex_search(*args):
        if len(args) < 2:
            return obj_factory['error']("search() އަށް ޕެޓާނަކާއި ލިޔުމެއް ދޭންވާނެ")
        pat = args[0].inspect()
        text = args[1].inspect()
        try:
            m = re.search(pat, text)
            if not m:
                return obj_factory['null']()
            return py_to_dhi({
                "found": True,
                "text": m.group(0),
                "start": m.start(),
                "end": m.end()
            })
        except Exception as e:
            return obj_factory['error'](f"ރެގެކްސް މައްސަލައެއް: {e}")

    def regex_replace(*args):
        if len(args) < 3:
            return obj_factory['error']("replace() އަށް ޕެޓާން، ބަދަލުކުރާ_އެއްޗެއް، އަދި ލިޔުން ދޭންވާނެ")
        pat = args[0].inspect()
        repl = args[1].inspect()
        text = args[2].inspect()
        try:
            res = re.sub(pat, repl, text)
            return obj_factory['string'](res)
        except Exception as e:
            return obj_factory['error'](f"ރެގެކްސް މައްސަލައެއް: {e}")

    def regex_split(*args):
        if len(args) < 2:
            return obj_factory['error']("split() އަށް ޕެޓާނަކާއި ލިޔުމެއް ދޭންވާނެ")
        pat = args[0].inspect()
        text = args[1].inspect()
        try:
            parts = re.split(pat, text)
            return obj_factory['list']([obj_factory['string'](p) for p in parts])
        except Exception as e:
            return obj_factory['error'](f"ރެގެކްސް މައްސަލައެއް: {e}")

    regex_module = {
        # Dhivehi
        "ދިމާވޭތޯ": obj_factory['builtin'](regex_match),
        "ހޯދާ": obj_factory['builtin'](regex_search),
        "ބަދަލުކުރޭ": obj_factory['builtin'](regex_replace),
        "ވަކިކުރޭ": obj_factory['builtin'](regex_split),

        # English
        "match": obj_factory['builtin'](regex_match),
        "search": obj_factory['builtin'](regex_search),
        "replace": obj_factory['builtin'](regex_replace),
        "split": obj_factory['builtin'](regex_split),
    }

    # =========================================================================
    # 12. ޑޭޓާބޭސް (SQLite Database Module - "db" / "sqlite" / "ޑޭޓާބޭސް")
    # =========================================================================
    def _py_val_to_sqlite(val):
        if val is None:
            return None
        if hasattr(val, 'type_str') and val.type_str() == "ހުސް":
            return None
        if hasattr(val, 'value'):
            if isinstance(val.value, float) and val.value.is_integer():
                return int(val.value)
            return val.value
        py = dhi_to_py(val)
        if isinstance(py, (dict, list)):
            return json.dumps(py, ensure_ascii=False)
        return py

    def _sqlite_val_to_dhi(val):
        if val is None:
            return obj_factory['null']()
        if isinstance(val, (int, float)):
            return obj_factory['num'](val)
        if isinstance(val, bool):
            return obj_factory['boolean'](val)
        if isinstance(val, str):
            return obj_factory['string'](val)
        if isinstance(val, bytes):
            return obj_factory['string'](val.decode('utf-8', errors='replace'))
        return py_to_dhi(val)

    _active_db_conn = [None]

    def db_open(*args):
        path = ":memory:"
        if args and hasattr(args[0], 'inspect'):
            p = args[0].inspect().strip()
            if p:
                path = p

        try:
            conn = sqlite3.connect(path, check_same_thread=False)
            conn.isolation_level = None
            conn.row_factory = sqlite3.Row
        except Exception as e:
            return obj_factory['error'](f"ޑޭޓާބޭސް ހުޅުވުމުގައި މައްސަލައެއް ({path}): {e}")

        def _parse_params(raw_args, start_idx=1):
            if len(raw_args) <= start_idx:
                return []
            p_arg = raw_args[start_idx]
            if hasattr(p_arg, 'elements'):
                return [_py_val_to_sqlite(x) for x in p_arg.elements]
            return [_py_val_to_sqlite(x) for x in raw_args[start_idx:]]

        def conn_execute(*c_args):
            if not c_args:
                return obj_factory['error']("execute() އަށް އެސްކިއުއެލް (SQL) ލިޔުމެއް ދޭންވާނެ")
            sql = c_args[0].inspect()
            params = _parse_params(c_args, 1)
            try:
                cur = conn.cursor()
                cur.execute(sql, params)
                res = {
                    "last_id": cur.lastrowid if cur.lastrowid is not None else 0,
                    "rows_affected": cur.rowcount if cur.rowcount is not None else 0,
                    "ކުރީގެ_އައިޑީ": cur.lastrowid if cur.lastrowid is not None else 0,
                    "ބަދަލުވި_ބަރި": cur.rowcount if cur.rowcount is not None else 0
                }
                return py_to_dhi(res)
            except Exception as e:
                return obj_factory['error'](f"އެސްކިއުއެލް ހިންގުމުގައި މައްސަލައެއް: {e}")

        def conn_execute_many(*c_args):
            if len(c_args) < 2:
                return obj_factory['error']("execute_many() އަށް އެސްކިއުއެލް އަދި ޕެރާމީޓަރުތަކުގެ ލިސްޓެއް ދޭންވާނެ")
            sql = c_args[0].inspect()
            param_list_arg = c_args[1]
            param_list = []
            if hasattr(param_list_arg, 'elements'):
                for item in param_list_arg.elements:
                    if hasattr(item, 'elements'):
                        param_list.append([_py_val_to_sqlite(x) for x in item.elements])
                    else:
                        param_list.append([_py_val_to_sqlite(item)])
            else:
                return obj_factory['error']("execute_many() އަށް ޕެރާމީޓަރުތަކުގެ ލިސްޓެއް ދޭންވާނެ")

            try:
                cur = conn.cursor()
                cur.executemany(sql, param_list)
                res = {
                    "rows_affected": cur.rowcount if cur.rowcount is not None else 0,
                    "ބަދަލުވި_ބަރި": cur.rowcount if cur.rowcount is not None else 0
                }
                return py_to_dhi(res)
            except Exception as e:
                return obj_factory['error'](f"ގިނަ އެސްކިއުއެލް ހިންގުމުގައި މައްސަލައެއް: {e}")

        def conn_query(*c_args):
            if not c_args:
                return obj_factory['error']("query() އަށް އެސްކިއުއެލް (SQL) ލިޔުމެއް ދޭންވާނެ")
            sql = c_args[0].inspect()
            params = _parse_params(c_args, 1)
            try:
                cur = conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                result_list = []
                for row in rows:
                    row_dict = {}
                    for col in row.keys():
                        row_dict[col] = _sqlite_val_to_dhi(row[col])
                    result_list.append(obj_factory['dict'](row_dict))
                return obj_factory['list'](result_list)
            except Exception as e:
                return obj_factory['error'](f"ކިއަރީ ކުރުމުގައި މައްސަލައެއް: {e}")

        def conn_query_one(*c_args):
            if not c_args:
                return obj_factory['error']("query_one() އަށް އެސްކިއުއެލް (SQL) ލިޔުމެއް ދޭންވާނެ")
            sql = c_args[0].inspect()
            params = _parse_params(c_args, 1)
            try:
                cur = conn.cursor()
                cur.execute(sql, params)
                row = cur.fetchone()
                if row is None:
                    return obj_factory['null']()
                row_dict = {}
                for col in row.keys():
                    row_dict[col] = _sqlite_val_to_dhi(row[col])
                return obj_factory['dict'](row_dict)
            except Exception as e:
                return obj_factory['error'](f"ކިއަރީ ކުރުމުގައި މައްސަލައެއް: {e}")

        def conn_begin(*c_args):
            try:
                conn.execute("BEGIN")
                return obj_factory['boolean'](True)
            except Exception as e:
                return obj_factory['error'](f"ޓްރާންސެކްޝަން ފެށުމުގައި މައްސަލައެއް: {e}")

        def conn_commit(*c_args):
            try:
                conn.execute("COMMIT")
                return obj_factory['boolean'](True)
            except Exception as e:
                return obj_factory['error'](f"ޔަޤީންކުރުމުގައި (commit) މައްސަލައެއް: {e}")

        def conn_rollback(*c_args):
            try:
                conn.execute("ROLLBACK")
                return obj_factory['boolean'](True)
            except Exception as e:
                return obj_factory['error'](f"ރުޖޫޢަކުރުމުގައި (rollback) މައްސަލައެއް: {e}")

        def conn_close(*c_args):
            try:
                conn.close()
                if _active_db_conn[0] is conn_handle:
                    _active_db_conn[0] = None
                return obj_factory['boolean'](True)
            except Exception as e:
                return obj_factory['error'](f"ޑޭޓާބޭސް ލެއްޕުމުގައި މައްސަލައެއް: {e}")

        def conn_tables(*c_args):
            try:
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
                tables = [r[0] for r in cur.fetchall()]
                return obj_factory['list']([obj_factory['string'](t) for t in tables])
            except Exception as e:
                return obj_factory['error'](f"ތާވަލުތައް ހޯދުމުގައި މައްސަލައެއް: {e}")

        conn_dict = {
            # English
            "execute": obj_factory['builtin'](conn_execute),
            "execute_many": obj_factory['builtin'](conn_execute_many),
            "query": obj_factory['builtin'](conn_query),
            "query_one": obj_factory['builtin'](conn_query_one),
            "begin": obj_factory['builtin'](conn_begin),
            "commit": obj_factory['builtin'](conn_commit),
            "rollback": obj_factory['builtin'](conn_rollback),
            "close": obj_factory['builtin'](conn_close),
            "tables": obj_factory['builtin'](conn_tables),

            # Dhivehi
            "ހިންގާ": obj_factory['builtin'](conn_execute),
            "ގިނައިން_ހިންގާ": obj_factory['builtin'](conn_execute_many),
            "ހޯދާ": obj_factory['builtin'](conn_query),
            "ކިއަރީ": obj_factory['builtin'](conn_query),
            "އެކަތި_ހޯދާ": obj_factory['builtin'](conn_query_one),
            "ފަށާ": obj_factory['builtin'](conn_begin),
            "ޔަޤީންކުރޭ": obj_factory['builtin'](conn_commit),
            "ރުޖޫޢަކުރޭ": obj_factory['builtin'](conn_rollback),
            "ލައްޕާ": obj_factory['builtin'](conn_close),
            "ތާވަލުތައް": obj_factory['builtin'](conn_tables),
        }
        conn_handle = obj_factory['dict'](conn_dict)
        _active_db_conn[0] = conn_handle
        return conn_handle

    def db_top_execute(*args):
        if not _active_db_conn[0]:
            db_open()
        return _active_db_conn[0].pairs["execute"].fn(*args)

    def db_top_query(*args):
        if not _active_db_conn[0]:
            db_open()
        return _active_db_conn[0].pairs["query"].fn(*args)

    def db_top_query_one(*args):
        if not _active_db_conn[0]:
            db_open()
        return _active_db_conn[0].pairs["query_one"].fn(*args)

    def db_top_close(*args):
        if _active_db_conn[0]:
            return _active_db_conn[0].pairs["close"].fn(*args)
        return obj_factory['boolean'](True)

    db_module = {
        # English
        "open": obj_factory['builtin'](db_open),
        "connect": obj_factory['builtin'](db_open),
        "db_open": obj_factory['builtin'](db_open),
        "execute": obj_factory['builtin'](db_top_execute),
        "query": obj_factory['builtin'](db_top_query),
        "query_one": obj_factory['builtin'](db_top_query_one),
        "close": obj_factory['builtin'](db_top_close),

        # Dhivehi
        "ހުޅުވާ": obj_factory['builtin'](db_open),
        "ގުޅާ": obj_factory['builtin'](db_open),
        "ޑޭޓާބޭސް_ހުޅުވާ": obj_factory['builtin'](db_open),
        "ހިންގާ": obj_factory['builtin'](db_top_execute),
        "ހޯދާ": obj_factory['builtin'](db_top_query),
        "އެކަތި_ހޯދާ": obj_factory['builtin'](db_top_query_one),
        "ލައްޕާ": obj_factory['builtin'](db_top_close),
    }

    # =========================================================================
    # Module Registry (Dual Dhivehi and English Names)
    # =========================================================================
    return {
        # Dhivehi Module Identifiers
        "ހިސާބު": math_module,
        "ފައިލް": file_module,
        "ވަގުތު": time_module,
        "ނިޒާމު": system_module,
        "ނެޓްވޯކް": network_module,
        "ނަކަތް": nakaiy_module,
        "ނަމާދު": prayer_module,
        "ތާނަ_ހިސާބު": thaana_math_module,
        "ތާނަ": thaana_math_module,
        "ކްރިޕްޓޯ": crypto_module,
        "ރެގެކްސް": regex_module,
        "ޑޭޓާބޭސް": db_module,
        "ޑީބީ": db_module,

        # English Module Identifiers
        "math": math_module,
        "file": file_module,
        "fs": file_module,
        "time": time_module,
        "sys": system_module,
        "os": system_module,
        "net": network_module,
        "http": network_module,
        "nakaiy": nakaiy_module,
        "prayer": prayer_module,
        "thaana": thaana_math_module,
        "crypto": crypto_module,
        "regex": regex_module,
        "db": db_module,
        "sqlite": db_module,
        "database": db_module,
    }
