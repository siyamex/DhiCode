# stdlib.py
import math
import time
import os
import sys
import random
from typing import Dict, Any

def get_stdlib_modules(obj_factory) -> Dict[str, Dict[str, Any]]:
    """
    Returns standard library modules for DhiCode.
    obj_factory provides helpers:
      - num(val)
      - string(val)
      - boolean(val)
      - builtin(fn)
      - error(msg)
      - null()
      - list(vals)
    """

    # --- 1. ހިސާބު (Math) ---
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

    # --- 2. ފައިލް (File System) ---
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

    # --- 3. ވަގުތު (Time) ---
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

    # --- 4. ނިޒާމު (System) ---
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

    return {
        "ހިސާބު": math_module,
        "ފައިލް": file_module,
        "ވަގުތު": time_module,
        "ނިޒާމު": system_module,
    }
