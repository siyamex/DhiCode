# stdlib.py - DhiCode Extended Standard Library
import math
import time
import os
import sys
import random
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, date
from typing import Dict, Any, List

def get_stdlib_modules(obj_factory) -> Dict[str, Dict[str, Any]]:
    """
    Returns extended standard library modules for DhiCode.
    obj_factory provides:
      - num, string, boolean, null, list, dict, error, builtin, py_to_dhi, dhi_to_py
    """

    py_to_dhi = obj_factory.get('py_to_dhi', lambda v: obj_factory['string'](str(v)))
    dhi_to_py = obj_factory.get('dhi_to_py', lambda o: o.inspect())

    # =========================================================================
    # 1. ހިސާބު (Math Module)
    # =========================================================================
    def math_sqrt(*args):
        if not args or not hasattr(args[0], 'value'):
            return obj_factory['error']("ޖަޒުރު() ބޭނުންކުރަންވާނީ ނަންބަރަކާއެކު")
        v = args[0].value
        if v < 0:
            return obj_factory['error']("ނެގަޓިވް އަދަދެއްގެ ޖަޒުރެއް ނުހޯދޭނެ")
        return obj_factory['num'](math.sqrt(v))

    def math_pow(*args):
        if len(args) < 2:
            return obj_factory['error']("ބާރު() އަށް 2 އަދަދު ދޭންވާނެ")
        return obj_factory['num'](math.pow(args[0].value, args[1].value))

    def math_round(*args):
        if not args:
            return obj_factory['error']("ކައިރި() އަށް އަދަދެއް ދޭންވާނެ")
        return obj_factory['num'](round(args[0].value))

    def math_floor(*args):
        if not args:
            return obj_factory['error']("ފްލޯރ() އަށް އަދަދެއް ދޭންވާނެ")
        return obj_factory['num'](math.floor(args[0].value))

    def math_ceil(*args):
        if not args:
            return obj_factory['error']("ސީލް() އަށް އަދަދެއް ދޭންވާނެ")
        return obj_factory['num'](math.ceil(args[0].value))

    def math_max(*args):
        if not args:
            return obj_factory['error']("އެންމެ_ބޮޑު() އަށް އަދަދުތަކެއް ދޭންވާނެ")
        return obj_factory['num'](max(a.value for a in args))

    def math_min(*args):
        if not args:
            return obj_factory['error']("އެންމެ_ކުޑަ() އަށް އަދަދުތަކެއް ދޭންވާނެ")
        return obj_factory['num'](min(a.value for a in args))

    def math_random(*args):
        min_v = int(args[0].value) if len(args) > 0 else 0
        max_v = int(args[1].value) if len(args) > 1 else 100
        return obj_factory['num'](random.randint(min_v, max_v))

    math_module = {
        "ޖަޒުރު": obj_factory['builtin'](math_sqrt),
        "ބާރު": obj_factory['builtin'](math_pow),
        "ކައިރި": obj_factory['builtin'](math_round),
        "ފްލޯރ": obj_factory['builtin'](math_floor),
        "ސީލް": obj_factory['builtin'](math_ceil),
        "އެންމެ_ބޮޑު": obj_factory['builtin'](math_max),
        "އެންމެ_ކުޑަ": obj_factory['builtin'](math_min),
        "އިއްތިފާޤު": obj_factory['builtin'](math_random),
        "ޕައި": obj_factory['num'](math.pi),
    }

    # =========================================================================
    # 2. ފައިލް (File System Module)
    # =========================================================================
    def file_read(*args):
        if not args:
            return obj_factory['error']("ފައިލް_ކިޔާ() އަށް ފައިލްގެ ނަން ދޭންވާނެ")
        path = args[0].inspect()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return obj_factory['string'](content)
        except Exception as e:
            return obj_factory['error'](f"ފައިލް ކިޔުމުގައި މައްސަލައެއް: {e}")

    def file_write(*args):
        if len(args) < 2:
            return obj_factory['error']("ފައިލް_ލިޔޭ() އަށް ފައިލްގެ ނަމާއި ލިޔުން ދޭންވާނެ")
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
            return obj_factory['error']("ފައިލް_އިތުރުކުރޭ() އަށް ފައިލްގެ ނަމާއި ލިޔުން ދޭންވާނެ")
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

    file_module = {
        "ކިޔާ": obj_factory['builtin'](file_read),
        "ލިޔޭ": obj_factory['builtin'](file_write),
        "އިތުރުކުރޭ": obj_factory['builtin'](file_append),
        "ވޭތޯ": obj_factory['builtin'](file_exists),
    }

    # =========================================================================
    # 3. ވަގުތު (Time Module)
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
        return obj_factory['string'](time.strftime("%Y-%m-%d %H:%M:%S"))

    time_module = {
        "މިހާރު": obj_factory['builtin'](time_now),
        "ހިނދުކޮޅު": obj_factory['builtin'](time_sleep),
        "ތާރީޚް": obj_factory['builtin'](time_date_str),
    }

    # =========================================================================
    # 4. ނިޒާމު (System Module)
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

    system_module = {
        "އާގިއުމެންޓުތައް": obj_factory['builtin'](sys_argv),
        "ހުއްޓާ": obj_factory['builtin'](sys_exit),
        "އެންވައިރޮންމެންޓް": obj_factory['builtin'](sys_getenv),
    }

    # =========================================================================
    # 5. ނެޓްވޯކް (Network & JSON Module) [Option 1]
    # =========================================================================
    def net_http_get(*args):
        if not args:
            return obj_factory['error']("ނަގާ() އަށް ޔޫއާރްއެލް (URL) ދޭންވާނެ")
        url = args[0].inspect()
        headers = {}
        if len(args) > 1:
            raw_h = dhi_to_py(args[1])
            if isinstance(raw_h, dict):
                headers = {str(k): str(v) for k, v in raw_h.items()}

        if "User-Agent" not in headers:
            headers["User-Agent"] = "DhiCode/0.3.0"

        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                status_code = resp.status
                body_bytes = resp.read()
                body_text = body_bytes.decode('utf-8', errors='replace')
                resp_headers = dict(resp.headers)

                parsed_json = None
                try:
                    parsed_json = json.loads(body_text)
                except Exception:
                    parsed_json = None

                return py_to_dhi({
                    "ކޯޑު": status_code,
                    "ލިޔުން": body_text,
                    "ހެޑަރ": resp_headers,
                    "ޖޭސަން": parsed_json
                })
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace') if hasattr(e, 'read') else ""
            return py_to_dhi({
                "ކޯޑު": e.code,
                "ލިޔުން": body,
                "ހެޑަރ": dict(e.headers) if hasattr(e, 'headers') else {},
                "ޖޭސަން": None
            })
        except Exception as e:
            return obj_factory['error'](f"ނެޓްވޯކް މައްސަލައެއް: {e}")

    def net_http_post(*args):
        if not args:
            return obj_factory['error']("ފޮނުވާ() އަށް ޔޫއާރްއެލް (URL) ދޭންވާނެ")
        url = args[0].inspect()
        data = None
        headers = {}

        if len(args) > 1:
            raw_data = dhi_to_py(args[1])
            if isinstance(raw_data, (dict, list)):
                data = json.dumps(raw_data, ensure_ascii=False).encode('utf-8')
                headers["Content-Type"] = "application/json; charset=utf-8"
            elif isinstance(raw_data, str):
                data = raw_data.encode('utf-8')
            else:
                data = str(raw_data).encode('utf-8')

        if len(args) > 2:
            raw_h = dhi_to_py(args[2])
            if isinstance(raw_h, dict):
                for k, v in raw_h.items():
                    headers[str(k)] = str(v)

        if "User-Agent" not in headers:
            headers["User-Agent"] = "DhiCode/0.3.0"

        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                status_code = resp.status
                body_bytes = resp.read()
                body_text = body_bytes.decode('utf-8', errors='replace')
                resp_headers = dict(resp.headers)

                parsed_json = None
                try:
                    parsed_json = json.loads(body_text)
                except Exception:
                    parsed_json = None

                return py_to_dhi({
                    "ކޯޑު": status_code,
                    "ލިޔުން": body_text,
                    "ހެޑަރ": resp_headers,
                    "ޖޭސަން": parsed_json
                })
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace') if hasattr(e, 'read') else ""
            return py_to_dhi({
                "ކޯޑު": e.code,
                "ލިޔުން": body,
                "ހެޑަރ": dict(e.headers) if hasattr(e, 'headers') else {},
                "ޖޭސަން": None
            })
        except Exception as e:
            return obj_factory['error'](f"ނެޓްވޯކް މައްސަލައެއް: {e}")

    def net_json_parse(*args):
        if not args:
            return obj_factory['error']("ޖޭސަން_ކިޔާ() އަށް ލިޔުމެއް ދޭންވާނެ")
        raw = args[0].inspect()
        try:
            data = json.loads(raw)
            return py_to_dhi(data)
        except Exception as e:
            return obj_factory['error'](f"ޖޭސަން ކިޔުމުގައި ކުށެއް: {e}")

    def net_json_stringify(*args):
        if not args:
            return obj_factory['error']("ޖޭސަން_ހަދާ() އަށް އެއްޗެއް ދޭންވާނެ")
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

    network_module = {
        "ނަގާ": obj_factory['builtin'](net_http_get),
        "ފޮނުވާ": obj_factory['builtin'](net_http_post),
        "ޖޭސަން_ކިޔާ": obj_factory['builtin'](net_json_parse),
        "ޖޭސަން_ހަދާ": obj_factory['builtin'](net_json_stringify),
        "ޔޫއާރްއެލް_އެންކޯޑް": obj_factory['builtin'](net_url_encode),
        "ޔޫއާރްއެލް_ޑީކޯޑް": obj_factory['builtin'](net_url_decode),
    }

    # =========================================================================
    # 6. ނަކަތް (Maldivian Nakaiy Calendar Module) [Option 2]
    # =========================================================================
    # 27 traditional Maldivian Nakaiy with date bounds (month, day) and climate features
    NAKAIY_LIST = [
        # --- Hulhangu (South-West Monsoon) - 18 Nakaiy ---
        {"ނަން": "އައްސިދަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "04-08", "ނިމެނީ": "04-21", "ދިގުމިން": 14, "ސިފަ": "ވިއްސާރަ، ގުގުރުން އަދި ކަނޑުގަދަ"},
        {"ނަން": "ބުރަނަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "04-22", "ނިމެނީ": "05-05", "ދިގުމިން": 14, "ސިފަ": "ކޮޅިގަނޑު، ވައިގަދަވުން"},
        {"ނަން": "ކެތި", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "05-06", "ނިމެނީ": "05-19", "ދިގުމިން": 14, "ސިފަ": "ވިލާ ބޯވުން، ވާރޭ ވެހުން"},
        {"ނަން": "ރޯނު", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "05-20", "ނިމެނީ": "06-02", "ދިގުމިން": 14, "ސިފަ": "ވައި ބާރުވެ ބޮޑެތި ރާޅުތައް ނެގުން"},
        {"ނަން": "މިއަހެލި", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "06-03", "ނިމެނީ": "06-16", "ދިގުމިން": 14, "ސިފަ": "ކުއްލިއަކަށް އަންނަ ބާރު ވިއްސާރަ"},
        {"ނަން": "އަދަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "06-17", "ނިމެނީ": "06-30", "ދިގުމިން": 14, "ސިފަ": "ވައިބާރުވެ ދޭތެރެދޭތެރެއިން ވާރޭވެހުން"},
        {"ނަން": "ފުނަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "07-01", "ނިމެނީ": "07-14", "ދިގުމިން": 14, "ސިފަ": "ކަނޑު ގަދަވެ ވައި ބާރުވުން"},
        {"ނަން": "ފުސް", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "07-15", "ނިމެނީ": "07-27", "ދިގުމިން": 13, "ސިފަ": "ވިލާ ބޯވެ ބަނަކޮށް އޮތުން"},
        {"ނަން": "އަހުލިހަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "07-28", "ނިމެނީ": "08-09", "ދިގުމިން": 13, "ސިފަ": "މަޑުމައިތިރި ކަނޑު، ދޭތެރެއިން ވާރޭ"},
        {"ނަން": "މާ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "08-10", "ނިމެނީ": "08-22", "ދިގުމިން": 13, "ސިފަ": "މަޑު ވައިރޯޅި، އުޑުމަތި ސާފުވުން"},
        {"ނަން": "ފުރަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "08-23", "ނިމެނީ": "09-04", "ދިގުމިން": 13, "ސިފަ": "އަރިއަރިޔަށް ވާރޭ ވެހުން"},
        {"ނަން": "އުތުރަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "09-05", "ނިމެނީ": "09-17", "ދިގުމިން": 13, "ސިފަ": "ބޯކޮށް ވާރޭވެހި ވައި ބާރުވުން"},
        {"ނަން": "އަތަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "09-18", "ނިމެނީ": "09-30", "ދިގުމިން": 13, "ސިފަ": "އަވިދޭ، ދޭތެރެއިން ކުއްލި ވިއްސާރަ"},
        {"ނަން": "ހިތަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "10-01", "ނިމެނީ": "10-13", "ދިގުމިން": 13, "ސިފަ": "މަޑު ވައި، މަސްވެރިކަން ރަނގަޅުވުން"},
        {"ނަން": "ހޭ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "10-14", "ނިމެނީ": "10-26", "ދިގުމިން": 13, "ސިފަ": "ގަދަ ވައި، މޫސުމީ ބަދަލުތައް"},
        {"ނަން": "ވިހާ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "10-27", "ނިމެނީ": "11-09", "ދިގުމިން": 14, "ސިފަ": "މަޑު ވައި، މަސްވެރިކަން ވަރަށް ރަނގަޅު"},
        {"ނަން": "ނޮރޮ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "11-10", "ނިމެނީ": "11-22", "ދިގުމިން": 13, "ސިފަ": "ފުސް ވިލާ، ލުއި ވިއްސާރަ"},
        {"ނަން": "ދޮށަ", "މޫސުން": "ހުޅަނގު", "ފެށެނީ": "11-23", "ނިމެނީ": "12-06", "ދިގުމިން": 14, "ސިފަ": "ހުޅަނގު މޫސުމުގެ އެންމެ ފަހު ނަކަތް"},

        # --- Iruvai (North-East Monsoon) - 9 Nakaiy ---
        {"ނަން": "މުލަ", "މޫސުން": "އިރުވައި", "ފެށެނީ": "12-07", "ނިމެނީ": "12-19", "ދިގުމިން": 13, "ސިފަ": "އިރުވައި މޫސުމުގެ ފެށުން، ގަދަ ވައި"},
        {"ނަން": "ފުރަހަޅަ", "މޫސުން": "އިރުވައި", "ފެށެނީ": "12-20", "ނިމެނީ": "01-01", "ދިގުމިން": 13, "ސިފަ": "ވައި ބާރުވެ ކަނޑު ގަދަވުން"},
        {"ނަން": "އުތުރުހަޅަ", "މޫސުން": "އިރުވައި", "ފެށެނީ": "01-02", "ނިމެނީ": "01-14", "ދިގުމިން": 13, "ސިފަ": "ސާފު އުޑުމަތި، ފިނި ރޯޅި"},
        {"ނަން": "ހުވަން", "މޫސުން": "އިރުވައި", "ފެށެނީ": "01-15", "ނިމެނީ": "01-27", "ދިގުމިން": 13, "ސިފަ": "ހިމޭން ކަނޑު، އަވިގަދަ ރީތި ދުވަސްތައް"},
        {"ނަން": "ދިނަޝަ", "މޫސުން": "އިރުވައި", "ފެށެނީ": "01-28", "ނިމެނީ": "02-09", "ދިގުމިން": 13, "ސިފަ": "މަޑު ވައި، ހިތްފަސޭހަ މޫސުން"},
        {"ނަން": "ހިޔަވިހާ", "މޫސުން": "އިރުވައި", "ފެށެނީ": "02-10", "ނިމެނީ": "02-22", "ދިގުމިން": 13, "ސިފަ": "ވަރަށް ހިމޭން މަޑު ކަނޑު، ހޫނުގަދަ"},
        {"ނަން": "ވައިވައި", "މޫސުން": "އިރުވައި", "ފެށެނީ": "02-23", "ނިމެނީ": "03-07", "ދިގުމިން": 13, "ސިފަ": "އެކި ދިމަދިމާއިން ވައި ޖެހުން"},
        {"ނަން": "ފަސްބުރުނު", "މޫސުން": "އިރުވައި", "ފެށެނީ": "03-08", "ނިމެނީ": "03-20", "ދިގުމިން": 13, "ސިފަ": "ކުއްލި ވިއްސާރަ، ހޫނުގަދަވުން"},
        {"ނަން": "ފޭބުރުނު", "މޫސުން": "އިރުވައި", "ފެށެނީ": "03-21", "ނިމެނީ": "04-07", "ދިގުމިން": 18, "ސިފަ": "އިރުވައި މޫސުމުގެ ނިމުން، މަޑުމައިތިރި"}
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
                # wraps around new year (e.g. 12-20 to 01-01)
                if target >= start or target <= end:
                    return n
        return NAKAIY_LIST[0]

    def nakaiy_today(*args):
        now = datetime.now()
        nak = _find_nakaiy_by_date(now.month, now.day)
        return py_to_dhi(nak)

    def nakaiy_lookup(*args):
        if len(args) < 2:
            return obj_factory['error']("ނަކަތް_ހޯދާ() އަށް މަހާއި ދުވަސް ދޭންވާނެ (މިސާލު: ނަކަތް_ހޯދާ(5, 12))")
        m = int(args[0].value) if hasattr(args[0], 'value') else int(args[0])
        d = int(args[1].value) if hasattr(args[1], 'value') else int(args[1])
        nak = _find_nakaiy_by_date(m, d)
        return py_to_dhi(nak)

    def nakaiy_all(*args):
        return py_to_dhi(NAKAIY_LIST)

    nakaiy_module = {
        "މިއަދުގެ_ނަކަތް": obj_factory['builtin'](nakaiy_today),
        "ނަކަތް_ހޯދާ": obj_factory['builtin'](nakaiy_lookup),
        "ހުރިހާ_ނަކަތް": obj_factory['builtin'](nakaiy_all),
    }

    # =========================================================================
    # 7. ނަމާދު (Maldivian Prayer Times Module) [Option 2]
    # =========================================================================
    # Accurate coordinates for Maldivian atolls/cities
    ATOLL_COORDS = {
        "މާލެ": (4.1755, 73.5093),
        "ހުޅުމާލެ": (4.2133, 73.5414),
        "ވިލިމާލެ": (4.1736, 73.4844),
        "އައްޑޫ": (-0.6300, 73.1600),
        "ފުވައްމުލައް": (-0.2980, 73.4240),
        "ކުޅުދުއްފުށި": (6.6220, 73.0700),
        "ތިނަދޫ": (0.5310, 72.9960),
        "ހއ": (6.9000, 72.9000),
        "ހދ": (6.6000, 73.0000),
        "ށ": (6.2000, 73.1000),
        "ނ": (5.8000, 73.3000),
        "ރ": (5.6000, 72.9000),
        "ބ": (5.1000, 72.9000),
        "ޅ": (5.4000, 73.6000),
        "ކ": (4.4000, 73.5000),
        "އއ": (4.0000, 72.8000),
        "އދ": (3.6000, 72.8000),
        "ވ": (3.4000, 73.5000),
        "މ": (2.9000, 73.5000),
        "ފ": (3.1000, 72.9000),
        "ދ": (2.7000, 72.9000),
        "ތ": (2.2000, 73.1000),
        "ލ": (1.9000, 73.4000),
        "ގއ": (0.7000, 73.4000),
        "ގދ": (0.4000, 73.1000),
        "ޏ": (-0.3000, 73.4200),
        "ސ": (-0.6300, 73.1600),
    }

    def _calc_prayer_times(lat: float, lon: float, year: int, month: int, day: int) -> Dict[str, str]:
        # Astronomical calculation based on solar declination and equation of time
        d = date(year, month, day)
        day_of_year = d.timetuple().tm_yday

        # Fractional year in radians
        gamma = 2 * math.pi / 365 * (day_of_year - 1)

        # Equation of time in minutes
        eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                           - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))

        # Solar declination in radians
        decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) \
               - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)

        lat_rad = math.radians(lat)
        timezone = 5.0 # Maldives UTC+5

        # Solar noon (transit) in hours
        solar_noon = 12 + (4 * (timezone * 15 - lon) - eqtime) / 60

        def _hour_angle(angle_deg: float) -> float:
            # angle_deg: altitude of sun (negative when below horizon)
            rad = math.radians(angle_deg)
            cos_ha = (math.sin(rad) - math.sin(lat_rad) * math.sin(decl)) / (math.cos(lat_rad) * math.cos(decl))
            cos_ha = max(-1.0, min(1.0, cos_ha))
            return math.degrees(math.acos(cos_ha)) / 15.0

        # Fajr: 18° below horizon (-18)
        ha_fajr = _hour_angle(-18.0)
        t_fajr = solar_noon - ha_fajr

        # Sunrise: -0.833°
        ha_sunrise = _hour_angle(-0.833)
        t_sunrise = solar_noon - ha_sunrise

        # Dhuhr: solar noon + 2 min buffer
        t_dhuhr = solar_noon + 2.0 / 60.0

        # Asr (Shafi'i: shadow = object length + noon shadow)
        # altitude of sun at asr: arccot(1 + tan|lat - decl|)
        noon_alt = math.pi / 2 - abs(lat_rad - decl)
        noon_shadow = 1.0 / math.tan(noon_alt) if math.tan(noon_alt) != 0 else 0
        asr_alt = math.atan(1.0 / (1.0 + noon_shadow))
        ha_asr = _hour_angle(math.degrees(asr_alt))
        t_asr = solar_noon + ha_asr

        # Maghrib: Sunset (-0.833°) + 2 min buffer
        t_sunset = solar_noon + ha_sunrise
        t_maghrib = t_sunset + 2.0 / 60.0

        # Isha: 18° below horizon (-18)
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
            "ފަތިސް": fmt_h(t_fajr),
            "އިރުއަރާ": fmt_h(t_sunrise),
            "މެންދުރު": fmt_h(t_dhuhr),
            "ޢަޞުރު": fmt_h(t_asr),
            "މަޣްރިބް": fmt_h(t_maghrib),
            "ޢިޝާ": fmt_h(t_isha)
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
        order = ["ފަތިސް", "މެންދުރު", "ޢަޞުރު", "މަޣްރިބް", "ޢިޝާ"]

        next_prayer = None
        rem_minutes = 0

        for p in order:
            t_str = times[p]
            parts = t_str.split(":")
            p_min = int(parts[0]) * 60 + int(parts[1])
            if p_min > cur_min:
                next_prayer = p
                rem_minutes = p_min - cur_min
                break

        if not next_prayer:
            # Tomorrow's Fajr
            tomorrow = datetime.fromtimestamp(time.time() + 86400)
            t_times = _calc_prayer_times(lat, lon, tomorrow.year, tomorrow.month, tomorrow.day)
            f_parts = t_times["ފަތިސް"].split(":")
            f_min = int(f_parts[0]) * 60 + int(f_parts[1])
            rem_minutes = (1440 - cur_min) + f_min
            next_prayer = "ފަތިސް"

        return py_to_dhi({
            "ނަމާދު": next_prayer,
            "ވަގުތު": times.get(next_prayer, "05:00"),
            "ބާކީ_މިނިޓް": rem_minutes
        })

    prayer_module = {
        "މިއަދުގެ_ވަގުތު": obj_factory['builtin'](prayer_today),
        "ވަގުތު_ހޯދާ": obj_factory['builtin'](prayer_lookup),
        "ދެން_އޮތް_ނަމާދު": obj_factory['builtin'](prayer_next),
    }

    # =========================================================================
    # 8. ތާނަ_ހިސާބު (Number-to-Words & Thaana Collation) [Option 2]
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
            # In Dhivehi: e.g. 35 -> ފަންސަތިރީސް, 31 -> އެއްތިރީސް
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
            return obj_factory['error']("އަދަދު_ބަހަށް() އަށް އަދަދެއް ދޭންވާނެ")
        val = int(args[0].value) if hasattr(args[0], 'value') else int(args[0])
        return obj_factory['string'](_number_to_dhivehi(val))

    def thaana_collation_key(word: str):
        # Strips fili and maps consonants to Thaana alphabet index
        key = []
        for ch in word:
            if ch in THAANA_ORDER_MAP:
                key.append(THAANA_ORDER_MAP[ch])
            elif '\u0780' <= ch <= '\u07BF':
                # Fili mark, assign secondary weight
                key.append(100 + ord(ch))
            else:
                key.append(200 + ord(ch))
        return key

    def thaana_sort_fn(*args):
        if not args:
            return obj_factory['error']("ތާނަ_ތަރުތީބު() އަށް ލިސްޓެއް ދޭންވާނެ")
        raw_list = dhi_to_py(args[0])
        if not isinstance(raw_list, list):
            return obj_factory['error']("ތާނަ_ތަރުތީބު() އަށް ލިސްޓެއް ދޭންވާނެ")

        sorted_list = sorted(raw_list, key=lambda s: thaana_collation_key(str(s)))
        return py_to_dhi(sorted_list)

    def thaana_alphabet_fn(*args):
        return py_to_dhi(THAANA_ALPHABET)

    thaana_math_module = {
        "އަދަދު_ބަހަށް": obj_factory['builtin'](num_to_dhivehi_fn),
        "ތާނަ_ތަރުތީބު": obj_factory['builtin'](thaana_sort_fn),
        "ތާނަ_އަކުރުތައް": obj_factory['builtin'](thaana_alphabet_fn),
    }

    # Module registry
    return {
        "ހިސާބު": math_module,
        "ފައިލް": file_module,
        "ވަގުތު": time_module,
        "ނިޒާމު": system_module,
        "ނެޓްވޯކް": network_module,
        "ނަކަތް": nakaiy_module,
        "ނަމާދު": prayer_module,
        "ތާނަ_ހިސާބު": thaana_math_module,
    }
