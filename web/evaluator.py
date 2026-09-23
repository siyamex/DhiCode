# evaluator.py
import os
from typing import Dict, Any, Optional, List, Union
from ast_nodes import (
    Node, Expression, Program, BlockStatement, LetStatement, ConstStatement,
    AssignmentStatement, IndexAssignmentStatement, ReturnStatement,
    PrintStatement, ExpressionStatement, IfStatement, WhileStatement,
    ForInStatement, FunctionStatement, ImportStatement, TryCatchStatement,
    ThrowStatement, Identifier, NumberLiteral, StringLiteral,
    BooleanLiteral, NullLiteral, ListLiteral, DictLiteral, IndexExpression,
    PrefixExpression, InfixExpression, CallExpression,
    Parameter, ClassStatement, DestructureLetStatement, DotAssignmentStatement,
    ThisExpression, DotExpression, ArrowFunctionLiteral, RangeExpression
)
from stdlib import get_stdlib_modules

# --- Runtime Objects ---

class DhicodeObject:
    def type_str(self) -> str:
        return "ނޭނގޭ"

    def inspect(self) -> str:
        return ""

class DhicodeNumber(DhicodeObject):
    def __init__(self, value: float):
        self.value = value

    def type_str(self) -> str:
        return "ނަންބަރު"

    def inspect(self) -> str:
        if isinstance(self.value, int) or self.value.is_integer():
            return str(int(self.value))
        return str(self.value)

class DhicodeString(DhicodeObject):
    def __init__(self, value: str):
        self.value = value

    def type_str(self) -> str:
        return "ލިޔުން"

    def inspect(self) -> str:
        return self.value

class DhicodeBoolean(DhicodeObject):
    def __init__(self, value: bool):
        self.value = value

    def type_str(self) -> str:
        return "ބޫލިއަން"

    def inspect(self) -> str:
        return "އާން" if self.value else "ނޫން"

class DhicodeList(DhicodeObject):
    def __init__(self, elements: List[DhicodeObject]):
        self.elements = elements

    def type_str(self) -> str:
        return "ލިސްޓު"

    def inspect(self) -> str:
        return "[" + ", ".join(e.inspect() for e in self.elements) + "]"

class DhicodeDict(DhicodeObject):
    def __init__(self, pairs: Dict[Any, DhicodeObject]):
        self.pairs = pairs

    def type_str(self) -> str:
        return "ރަދީފު"

    def inspect(self) -> str:
        items = []
        for k, v in self.pairs.items():
            k_str = k.inspect() if isinstance(k, DhicodeObject) else str(k)
            items.append(f"{k_str}: {v.inspect()}")
        return "{" + ", ".join(items) + "}"

class DhicodeNull(DhicodeObject):
    def type_str(self) -> str:
        return "ހުސް"

    def inspect(self) -> str:
        return "ހުސް"

class DhicodeReturnValue(DhicodeObject):
    def __init__(self, value: DhicodeObject):
        self.value = value

    def type_str(self) -> str:
        return "ފޮނުވާ_އަގު"

    def inspect(self) -> str:
        return self.value.inspect()

class DhicodeError(DhicodeObject):
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.message = message
        self.line = line
        self.column = column

    def type_str(self) -> str:
        return "ކުށް"

    def inspect(self) -> str:
        loc = f" (ލައިން {self.line})" if self.line > 0 else ""
        return f"ކުށް{loc}: {self.message}"

class DhicodeClass(DhicodeObject):
    def __init__(self, name: str, methods: Dict[str, 'DhicodeFunction'], super_class: Optional['DhicodeClass'] = None):
        self.name = name
        self.methods = methods
        self.super_class = super_class

    def type_str(self) -> str:
        return "ކްލާސް"

    def inspect(self) -> str:
        return f"<ކްލާސް {self.name}>"

    def get_method(self, name: str) -> Optional['DhicodeFunction']:
        if name in self.methods:
            return self.methods[name]
        if self.super_class is not None:
            return self.super_class.get_method(name)
        return None

class DhicodeInstance(DhicodeObject):
    def __init__(self, klass: DhicodeClass):
        self.klass = klass
        self.fields: Dict[str, DhicodeObject] = {}

    def type_str(self) -> str:
        return self.klass.name

    def inspect(self) -> str:
        fields_str = ", ".join(f"{k}: {v.inspect()}" for k, v in self.fields.items())
        return f"<{self.klass.name} {{{fields_str}}}>"

    def get(self, name: str) -> Optional[DhicodeObject]:
        if name in self.fields:
            return self.fields[name]
        method = self.klass.get_method(name)
        if method is not None:
            return DhicodeBoundMethod(self, method)
        return None

    def set(self, name: str, value: DhicodeObject) -> DhicodeObject:
        self.fields[name] = value
        return value

class DhicodeBoundMethod(DhicodeObject):
    def __init__(self, instance: DhicodeInstance, method: 'DhicodeFunction'):
        self.instance = instance
        self.method = method

    def type_str(self) -> str:
        return "މެތަޑް"

    def inspect(self) -> str:
        return f"<މެތަޑް {self.instance.klass.name}.{self.method.inspect()}>"

class DhicodeFunction(DhicodeObject):
    def __init__(self, parameters: List[Any], body: Union[BlockStatement, Expression], env: 'Environment'):
        self.parameters = parameters
        self.body = body
        self.env = env

    def type_str(self) -> str:
        return "ވަޒީފާ"

    def inspect(self) -> str:
        params = []
        for p in self.parameters:
            if hasattr(p, 'name') and hasattr(p.name, 'value'):
                params.append(p.name.value)
            elif hasattr(p, 'value'):
                params.append(p.value)
            else:
                params.append(str(p))
        return f"ވަޒީފާ({', '.join(params)})"

class DhicodeBuiltin(DhicodeObject):
    def __init__(self, fn):
        self.fn = fn

    def type_str(self) -> str:
        return "ބިލްޓްއިން"

    def inspect(self) -> str:
        return "ބިލްޓްއިން ވަޒީފާ"

# Constants
TRUE_OBJ = DhicodeBoolean(True)
FALSE_OBJ = DhicodeBoolean(False)
NULL_OBJ = DhicodeNull()

# --- Environment ---

class Environment:
    def __init__(self, outer: Optional['Environment'] = None):
        self.store: Dict[str, DhicodeObject] = {}
        self.constants: set = set()
        self.outer = outer

    def get(self, name: str) -> Optional[DhicodeObject]:
        if name in self.store:
            return self.store[name]
        if self.outer is not None:
            return self.outer.get(name)
        return None

    def set(self, name: str, val: DhicodeObject) -> DhicodeObject:
        if name in self.constants:
            return DhicodeError(f"ދާއިމީ ވެރިއަބަލް '{name}' ގެ އަގު ބަދަލެއް ނުކުރެވޭނެ")
        self.store[name] = val
        return val

    def define_const(self, name: str, val: DhicodeObject) -> DhicodeObject:
        if name in self.constants:
            return DhicodeError(f"ދާއިމީ ވެރިއަބަލް '{name}' ގެ އަގު ބަދަލެއް ނުކުރެވޭނެ")
        self.store[name] = val
        self.constants.add(name)
        return val

    def is_const(self, name: str) -> bool:
        if name in self.constants:
            return True
        if self.outer is not None:
            return self.outer.is_const(name)
        return False

    def assign(self, name: str, val: DhicodeObject) -> DhicodeObject:
        if name in self.store:
            if name in self.constants:
                return DhicodeError(f"ދާއިމީ ވެރިއަބަލް '{name}' ގެ އަގު ބަދަލެއް ނުކުރެވޭނެ")
            self.store[name] = val
            return val
        if self.outer is not None and self.outer.get(name) is not None:
            return self.outer.assign(name, val)
        self.store[name] = val
        return val

def python_to_dhi(val: Any) -> DhicodeObject:
    if val is None:
        return NULL_OBJ
    if isinstance(val, bool):
        return TRUE_OBJ if val else FALSE_OBJ
    if isinstance(val, (int, float)):
        return DhicodeNumber(val)
    if isinstance(val, str):
        return DhicodeString(val)
    if isinstance(val, list):
        return DhicodeList([python_to_dhi(x) for x in val])
    if isinstance(val, dict):
        pairs = {}
        for k, v in val.items():
            pairs[str(k)] = python_to_dhi(v)
        return DhicodeDict(pairs)
    if isinstance(val, DhicodeObject):
        return val
    return DhicodeString(str(val))

def dhi_to_python(obj: DhicodeObject) -> Any:
    if obj is None or isinstance(obj, DhicodeNull):
        return None
    if isinstance(obj, DhicodeBoolean):
        return obj.value
    if isinstance(obj, DhicodeNumber):
        return int(obj.value) if obj.value.is_integer() else obj.value
    if isinstance(obj, DhicodeString):
        return obj.value
    if isinstance(obj, DhicodeList):
        return [dhi_to_python(x) for x in obj.elements]
    if isinstance(obj, DhicodeDict):
        res = {}
        for k, v in obj.pairs.items():
            k_key = k if isinstance(k, str) else (k.value if isinstance(k, DhicodeString) else str(k))
            res[k_key] = dhi_to_python(v)
        return res
    return obj.inspect()

# --- Evaluator ---

class Evaluator:
    def __init__(self, output_callback=None, base_path: str = "."):
        self.output_callback = output_callback if output_callback else print
        self.base_path = base_path
        self.module_cache: Dict[str, Environment] = {}

        # Factory for stdlib
        self.obj_factory = {
            'num': lambda v: DhicodeNumber(v),
            'string': lambda v: DhicodeString(v),
            'boolean': lambda v: TRUE_OBJ if v else FALSE_OBJ,
            'null': lambda: NULL_OBJ,
            'list': lambda elems: DhicodeList(elems),
            'dict': lambda pairs: DhicodeDict(pairs),
            'error': lambda msg: DhicodeError(msg),
            'builtin': lambda fn: DhicodeBuiltin(fn),
            'py_to_dhi': python_to_dhi,
            'dhi_to_py': dhi_to_python,
            'call_fn': lambda fn, args: self._apply_function(fn, [a if isinstance(a, DhicodeObject) else python_to_dhi(a) for a in args]),
        }
        self.stdlib = get_stdlib_modules(self.obj_factory)

    def eval(self, node: Optional[Node], env: Environment) -> DhicodeObject:
        if node is None:
            return NULL_OBJ

        # Program
        if isinstance(node, Program):
            return self._eval_program(node, env)

        # Block
        elif isinstance(node, BlockStatement):
            return self._eval_block_statement(node, env)

        # Statements
        elif isinstance(node, LetStatement):
            val = self.eval(node.value, env)
            if isinstance(val, DhicodeError):
                return val
            res = env.set(node.name.value, val)
            if isinstance(res, DhicodeError):
                return res
            return val

        elif isinstance(node, ConstStatement):
            val = self.eval(node.value, env)
            if isinstance(val, DhicodeError):
                return val
            res = env.define_const(node.name.value, val)
            if isinstance(res, DhicodeError):
                return res
            return val

        elif isinstance(node, AssignmentStatement):
            val = self.eval(node.value, env)
            if isinstance(val, DhicodeError):
                return val

            if node.operator == "=":
                new_val = val
            else:
                curr = env.get(node.name.value)
                if curr is None:
                    return DhicodeError(f"ނޭނގޭ ނަމެއް: '{node.name.value}'", node.token.line, node.token.column)
                if isinstance(curr, DhicodeError):
                    return curr
                base_op = node.operator[:-1]
                new_val = self._eval_infix_expression(base_op, curr, val)
                if isinstance(new_val, DhicodeError):
                    return new_val

            res = env.assign(node.name.value, new_val)
            if isinstance(res, DhicodeError):
                return res
            return new_val

        elif isinstance(node, IndexAssignmentStatement):
            target = self.eval(node.target, env)
            if isinstance(target, DhicodeError):
                return target
            index = self.eval(node.index, env)
            if isinstance(index, DhicodeError):
                return index
            val = self.eval(node.value, env)
            if isinstance(val, DhicodeError):
                return val

            if node.operator != "=":
                curr = self._eval_index_expression(target, index, None)
                if isinstance(curr, DhicodeError):
                    return curr
                base_op = node.operator[:-1]
                val = self._eval_infix_expression(base_op, curr, val)
                if isinstance(val, DhicodeError):
                    return val

            if isinstance(target, DhicodeList):
                if not isinstance(index, DhicodeNumber):
                    return DhicodeError(f"ލިސްޓުގެ އިންޑެކްސް ވާންވާނީ ނަންބަރަކަށް: {index.type_str()}")
                idx = int(index.value)
                if idx < 0:
                    idx = len(target.elements) + idx
                if idx < 0 or idx >= len(target.elements):
                    return DhicodeError(f"ލިސްޓުގެ އިންޑެކްސް އިމުން ބޭރުވެއްޖެ: {idx}")
                target.elements[idx] = val
                return val

            elif isinstance(target, DhicodeDict):
                key = index.inspect()
                target.pairs[key] = val
                return val

            return DhicodeError(f"އިންޑެކްސް އަށް އަގު ނުލެވޭ ބާވަތެއް: {target.type_str()}")

        elif isinstance(node, ReturnStatement):
            val = self.eval(node.return_value, env) if node.return_value else NULL_OBJ
            if isinstance(val, DhicodeError):
                return val
            return DhicodeReturnValue(val)

        elif isinstance(node, PrintStatement):
            exprs = node.values if hasattr(node, 'values') and node.values else ([node.value] if node.value is not None else [])
            parts = []
            for expr in exprs:
                val = self.eval(expr, env)
                if isinstance(val, DhicodeError):
                    return val
                parts.append(val.inspect())
            self.output_callback(" ".join(parts))
            return NULL_OBJ

        elif isinstance(node, ExpressionStatement):
            return self.eval(node.expression, env)

        elif isinstance(node, IfStatement):
            return self._eval_if_statement(node, env)

        elif isinstance(node, WhileStatement):
            return self._eval_while_statement(node, env)

        elif isinstance(node, ForInStatement):
            return self._eval_for_in_statement(node, env)

        elif isinstance(node, FunctionStatement):
            fn = DhicodeFunction(node.parameters, node.body, env)
            if node.name.value:
                env.set(node.name.value, fn)
            return fn

        elif isinstance(node, ClassStatement):
            methods: Dict[str, DhicodeFunction] = {}
            super_class = None
            if node.super_class is not None:
                super_obj = env.get(node.super_class.value)
                if not isinstance(super_obj, DhicodeClass):
                    return DhicodeError(f"ދަރިކޮޅު ނަގަންވާނީ ކްލާހަކުން: {node.super_class.value}")
                super_class = super_obj

            for m in node.methods:
                fn_obj = DhicodeFunction(m.parameters, m.body, env)
                methods[m.name.value] = fn_obj

            klass = DhicodeClass(node.name.value, methods, super_class)
            env.set(node.name.value, klass)
            return klass

        elif isinstance(node, DestructureLetStatement):
            val = self.eval(node.value, env)
            if isinstance(val, DhicodeError):
                return val

            if node.kind == "list":
                if not isinstance(val, DhicodeList):
                    return DhicodeError(f"ލިސްޓު ޑީސްޓްރަކްޗަރިންގ ކުރެވޭނީ ލިސްޓަކުން: {val.type_str()}")
                for i, name_ident in enumerate(node.names):
                    elem = val.elements[i] if i < len(val.elements) else NULL_OBJ
                    if node.is_const:
                        env.define_const(name_ident.value, elem)
                    else:
                        env.set(name_ident.value, elem)
                return NULL_OBJ
            elif node.kind == "dict":
                if isinstance(val, DhicodeDict):
                    for name_ident in node.names:
                        key = name_ident.value
                        prop = val.pairs.get(key, NULL_OBJ)
                        if node.is_const:
                            env.define_const(key, prop)
                        else:
                            env.set(key, prop)
                    return NULL_OBJ
                elif isinstance(val, DhicodeInstance):
                    for name_ident in node.names:
                        key = name_ident.value
                        prop = val.get(key) or NULL_OBJ
                        if node.is_const:
                            env.define_const(key, prop)
                        else:
                            env.set(key, prop)
                    return NULL_OBJ
                else:
                    return DhicodeError(f"ރަދީފު ޑީސްޓްރަކްޗަރިންގ ކުރެވޭނީ ރަދީފަކުން ނުވަތަ އޮބްޖެކްޓަކުން: {val.type_str()}")

        elif isinstance(node, DotAssignmentStatement):
            target = self.eval(node.target, env)
            if isinstance(target, DhicodeError):
                return target

            val = self.eval(node.value, env)
            if isinstance(val, DhicodeError):
                return val

            prop_name = node.property_name.value
            op = node.operator

            if op != "=":
                cur_val = NULL_OBJ
                if isinstance(target, DhicodeInstance):
                    cur_val = target.fields.get(prop_name, NULL_OBJ)
                elif isinstance(target, DhicodeDict):
                    cur_val = target.pairs.get(prop_name, NULL_OBJ)
                else:
                    return DhicodeError(f"ޕްރޮޕަޓީ ބަދަލު ނުކުރެވޭނެ އެއްޗެއް: {target.type_str()}")

                bin_op = op[:-1]
                val = self._eval_infix_expression(bin_op, cur_val, val)
                if isinstance(val, DhicodeError):
                    return val

            if isinstance(target, DhicodeInstance):
                target.set(prop_name, val)
                return val
            elif isinstance(target, DhicodeDict):
                target.pairs[prop_name] = val
                return val
            else:
                return DhicodeError(f"ޕްރޮޕަޓީ ބަދަލު ނުކުރެވޭނެ އެއްޗެއް: {target.type_str()}")

        elif isinstance(node, ImportStatement):
            return self._eval_import_statement(node, env)

        elif isinstance(node, TryCatchStatement):
            return self._eval_try_catch_statement(node, env)

        elif isinstance(node, ThrowStatement):
            val = self.eval(node.expr, env)
            msg = val.inspect() if not isinstance(val, DhicodeError) else val.message
            return DhicodeError(msg, node.token.line, node.token.column)

        # Expressions
        elif isinstance(node, Identifier):
            return self._eval_identifier(node, env)

        elif isinstance(node, NumberLiteral):
            return DhicodeNumber(node.value)

        elif isinstance(node, StringLiteral):
            return self._interpolate_string(node.value, env)

        elif isinstance(node, BooleanLiteral):
            return TRUE_OBJ if node.value else FALSE_OBJ

        elif isinstance(node, NullLiteral):
            return NULL_OBJ

        elif isinstance(node, ListLiteral):
            elements = []
            for el in node.elements:
                val = self.eval(el, env)
                if isinstance(val, DhicodeError):
                    return val
                elements.append(val)
            return DhicodeList(elements)

        elif isinstance(node, DictLiteral):
            pairs = {}
            for k_expr, v_expr in node.pairs.items():
                if isinstance(k_expr, Identifier):
                    raw_k = k_expr.value
                else:
                    k_val = self.eval(k_expr, env)
                    if isinstance(k_val, DhicodeError):
                        return k_val
                    raw_k = k_val.inspect()
                v_val = self.eval(v_expr, env)
                if isinstance(v_val, DhicodeError):
                    return v_val
                pairs[raw_k] = v_val
            return DhicodeDict(pairs)

        elif isinstance(node, IndexExpression):
            left = self.eval(node.left, env)
            if isinstance(left, DhicodeError):
                return left
            index = self.eval(node.index, env)
            if isinstance(index, DhicodeError):
                return index
            return self._eval_index_expression(left, index, node)

        elif isinstance(node, PrefixExpression):
            right = self.eval(node.right, env)
            if isinstance(right, DhicodeError):
                return right
            return self._eval_prefix_expression(node.operator, right)

        elif isinstance(node, InfixExpression):
            left = self.eval(node.left, env)
            if isinstance(left, DhicodeError):
                return left

            # Short-circuit logical AND
            if node.operator in ("&&", "އަދި", "and"):
                if not self._is_truthy(left):
                    return FALSE_OBJ
                right = self.eval(node.right, env)
                if isinstance(right, DhicodeError):
                    return right
                return TRUE_OBJ if self._is_truthy(right) else FALSE_OBJ

            # Short-circuit logical OR
            if node.operator in ("||", "ނުވަތަ", "or"):
                if self._is_truthy(left):
                    return TRUE_OBJ
                right = self.eval(node.right, env)
                if isinstance(right, DhicodeError):
                    return right
                return TRUE_OBJ if self._is_truthy(right) else FALSE_OBJ

            # Short-circuit null coalescing
            if node.operator == "??":
                if not isinstance(left, DhicodeNull):
                    return left
                return self.eval(node.right, env)

            right = self.eval(node.right, env)
            if isinstance(right, DhicodeError):
                return right
            return self._eval_infix_expression(node.operator, left, right)

        elif isinstance(node, CallExpression):
            function = self.eval(node.function, env)
            if isinstance(function, DhicodeError):
                return function

            args = []
            for arg_expr in node.arguments:
                arg_val = self.eval(arg_expr, env)
                if isinstance(arg_val, DhicodeError):
                    return arg_val
                args.append(arg_val)

            return self._apply_function(function, args)

        elif isinstance(node, ThisExpression):
            for kw in ("މި", "this", "self"):
                val = env.get(kw)
                if val is not None:
                    return val
            return DhicodeError("މި (this) ބޭނުންކުރެވޭނީ ކްލާހެއްގެ މެތަޑެއްގެ ތެރޭގައެވެ")

        elif isinstance(node, DotExpression):
            target = self.eval(node.left, env)
            if isinstance(target, DhicodeError):
                return target

            prop = node.property_name.value
            if isinstance(target, DhicodeInstance):
                res = target.get(prop)
                if res is not None:
                    return res
                return DhicodeError(f"'{target.klass.name}' ގައި '{prop}' އެއް ނުފެނުނު")
            elif isinstance(target, DhicodeDict):
                if prop in target.pairs:
                    return target.pairs[prop]
                return NULL_OBJ
            else:
                return DhicodeError(f"ޕްރޮޕަޓީ ހޯދޭނީ އޮބްޖެކްޓަކުން ނުވަތަ ރަދީފަކުން: {target.type_str()}")

        elif isinstance(node, ArrowFunctionLiteral):
            return DhicodeFunction(node.parameters, node.body, env)

        elif isinstance(node, RangeExpression):
            start_val = self.eval(node.start, env)
            if isinstance(start_val, DhicodeError):
                return start_val
            end_val = self.eval(node.end, env)
            if isinstance(end_val, DhicodeError):
                return end_val

            if not isinstance(start_val, DhicodeNumber) or not isinstance(end_val, DhicodeNumber):
                return DhicodeError("ރޭންޖް (..) ބޭނުންކުރެވޭނީ ނަންބަރާ ދެމެދުގައެވެ")

            s = int(start_val.value)
            e = int(end_val.value)
            step = 1 if s <= e else -1
            nums = list(range(s, e + step, step))
            return DhicodeList([DhicodeNumber(n) for n in nums])

    def _eval_program(self, program: Program, env: Environment) -> DhicodeObject:
        result: DhicodeObject = NULL_OBJ
        for statement in program.statements:
            result = self.eval(statement, env)
            if isinstance(result, DhicodeReturnValue):
                return result.value
            if isinstance(result, DhicodeError):
                return result
        return result

    def _eval_block_statement(self, block: BlockStatement, env: Environment) -> DhicodeObject:
        result: DhicodeObject = NULL_OBJ
        for statement in block.statements:
            result = self.eval(statement, env)
            if isinstance(result, (DhicodeReturnValue, DhicodeError)):
                return result
        return result

    def _eval_if_statement(self, node: IfStatement, env: Environment) -> DhicodeObject:
        condition = self.eval(node.condition, env)
        if isinstance(condition, DhicodeError):
            return condition

        if self._is_truthy(condition):
            return self.eval(node.consequence, env)
        elif node.alternative is not None:
            return self.eval(node.alternative, env)
        return NULL_OBJ

    def _eval_while_statement(self, node: WhileStatement, env: Environment) -> DhicodeObject:
        result: DhicodeObject = NULL_OBJ
        while True:
            condition = self.eval(node.condition, env)
            if isinstance(condition, DhicodeError):
                return condition
            if not self._is_truthy(condition):
                break
            result = self.eval(node.body, env)
            if isinstance(result, (DhicodeReturnValue, DhicodeError)):
                return result
        return result

    def _eval_for_in_statement(self, node: ForInStatement, env: Environment) -> DhicodeObject:
        iterable = self.eval(node.iterable, env)
        if isinstance(iterable, DhicodeError):
            return iterable

        items = []
        if isinstance(iterable, DhicodeList):
            items = iterable.elements
        elif isinstance(iterable, DhicodeString):
            items = [DhicodeString(ch) for ch in iterable.value]
        elif isinstance(iterable, DhicodeDict):
            items = [DhicodeString(k) for k in iterable.pairs.keys()]
        else:
            return DhicodeError(f"{iterable.type_str()} ގެ މައްޗަށް 'ކޮންމެ' ލޫޕެއް ނުހިންގޭނެ")

        result: DhicodeObject = NULL_OBJ
        for it in items:
            env.set(node.item.value, it)
            result = self.eval(node.body, env)
            if isinstance(result, DhicodeReturnValue):
                return result
            if isinstance(result, DhicodeError):
                return result

        return NULL_OBJ

    def _eval_index_expression(self, left: DhicodeObject, index: DhicodeObject, node: IndexExpression) -> DhicodeObject:
        if isinstance(left, DhicodeList):
            if not isinstance(index, DhicodeNumber):
                return DhicodeError(f"ލިސްޓުގެ އިންޑެކްސް ވާންވާނީ ނަންބަރަކަށް: {index.type_str()}")
            idx = int(index.value)
            if idx < 0:
                idx = len(left.elements) + idx
            if idx < 0 or idx >= len(left.elements):
                return DhicodeError(f"ލިސްޓުގެ އިންޑެކްސް އިމުން ބޭރުވެއްޖެ: {idx}")
            return left.elements[idx]

        elif isinstance(left, DhicodeDict):
            key = index.inspect()
            if key in left.pairs:
                return left.pairs[key]
            return NULL_OBJ

        elif isinstance(left, DhicodeString):
            if not isinstance(index, DhicodeNumber):
                return DhicodeError(f"ލިޔުމުގެ އިންޑެކްސް ވާންވާނީ ނަންބަރަކަށް: {index.type_str()}")
            idx = int(index.value)
            if idx < 0:
                idx = len(left.value) + idx
            if idx < 0 or idx >= len(left.value):
                return DhicodeError(f"ލިޔުމުގެ އިންޑެކްސް އިމުން ބޭރުވެއްޖެ: {idx}")
            return DhicodeString(left.value[idx])

        return DhicodeError(f"އިންޑެކްސް ނުކުރެވޭ ބާވަތެއް: {left.type_str()}")

    def _eval_import_statement(self, node: ImportStatement, env: Environment) -> DhicodeObject:
        mod_name = node.path

        # 1. Check Standard Library
        if mod_name in self.stdlib:
            for k, v in self.stdlib[mod_name].items():
                env.set(k, v)
            return NULL_OBJ

        # 2. Check local file
        target_path = os.path.join(self.base_path, mod_name)
        if not target_path.endswith('.dhi'):
            target_path += '.dhi'

        if not os.path.exists(target_path):
            return DhicodeError(f"ގެނޭ: ފައިލް ނުފެނުނު '{mod_name}'")

        if target_path in self.module_cache:
            mod_env = self.module_cache[target_path]
        else:
            try:
                with open(target_path, 'r', encoding='utf-8') as f:
                    source = f.read()
            except Exception as e:
                return DhicodeError(f"ގެނޭ: ފައިލް ކިޔުމުގައި މައްސަލައެއް: {e}")

            from lexer import Lexer
            from parser import Parser
            lexer = Lexer(source)
            parser = Parser(lexer)
            program = parser.parse_program()
            if parser.errors:
                return DhicodeError(f"ގެނޭ: ޕާސިންގ މައްސަލަ: {parser.errors[0]}")

            mod_env = Environment()
            eval_res = self.eval(program, mod_env)
            if isinstance(eval_res, DhicodeError):
                return eval_res
            self.module_cache[target_path] = mod_env

        # Inject exported variables into current environment
        for k, v in mod_env.store.items():
            env.set(k, v)

        return NULL_OBJ

    def _eval_try_catch_statement(self, node: TryCatchStatement, env: Environment) -> DhicodeObject:
        try_res = self.eval(node.try_block, env)
        if isinstance(try_res, DhicodeError):
            if node.error_var:
                env.set(node.error_var.value, DhicodeString(try_res.message))
            return self.eval(node.catch_block, env)
        return try_res

    def _eval_identifier(self, node: Identifier, env: Environment) -> DhicodeObject:
        val = env.get(node.value)
        if val is not None:
            return val
        builtin = self._get_builtin(node.value)
        if builtin is not None:
            return builtin
        return DhicodeError(f"ނޭނގޭ ނަމެއް: '{node.value}'", node.token.line, node.token.column)

    def _is_truthy(self, obj: DhicodeObject) -> bool:
        if obj is NULL_OBJ:
            return False
        if isinstance(obj, DhicodeBoolean):
            return obj.value
        if isinstance(obj, DhicodeNumber):
            return obj.value != 0
        if isinstance(obj, DhicodeString):
            return len(obj.value) > 0
        if isinstance(obj, DhicodeList):
            return len(obj.elements) > 0
        if isinstance(obj, DhicodeDict):
            return len(obj.pairs) > 0
        return True

    def _eval_prefix_expression(self, operator: str, right: DhicodeObject) -> DhicodeObject:
        if operator in ("!", "not"):
            return FALSE_OBJ if self._is_truthy(right) else TRUE_OBJ
        elif operator == "-":
            if not isinstance(right, DhicodeNumber):
                return DhicodeError(f"ނަންބަރެއް ނޫން އަދަދަކަށް '-' ބޭނުމެއް ނުކުރެވޭނެ: {right.type_str()}")
            return DhicodeNumber(-right.value)
        elif operator == "~":
            if not isinstance(right, DhicodeNumber):
                return DhicodeError(f"ނަންބަރެއް ނޫން އަދަދަކަށް '~' ބޭނުމެއް ނުކުރެވޭނެ: {right.type_str()}")
            return DhicodeNumber(~int(right.value))
        return DhicodeError(f"ނޭނގޭ އޮޕަރޭޓަރ: {operator}{right.type_str()}")

    def _eval_infix_expression(self, operator: str, left: DhicodeObject, right: DhicodeObject) -> DhicodeObject:
        if operator == "??":
            return right if isinstance(left, DhicodeNull) else left

        if operator == "+":
            if isinstance(left, DhicodeList) and isinstance(right, DhicodeList):
                return DhicodeList(left.elements + right.elements)
            if isinstance(left, DhicodeString) or isinstance(right, DhicodeString):
                return DhicodeString(left.inspect() + right.inspect())
            if isinstance(left, DhicodeNumber) and isinstance(right, DhicodeNumber):
                return DhicodeNumber(left.value + right.value)
            return DhicodeError(f"'+' ބޭނުމެއް ނުކުރެވޭނެ {left.type_str()} އަދި {right.type_str()} އާ ދެމެދު")

        if isinstance(left, DhicodeNumber) and isinstance(right, DhicodeNumber):
            return self._eval_numeric_infix(operator, left, right)

        if operator in ("==", "="):
            return TRUE_OBJ if self._is_equal(left, right) else FALSE_OBJ
        elif operator == "!=":
            return FALSE_OBJ if self._is_equal(left, right) else TRUE_OBJ
        elif operator in ("&&", "އަދި"):
            return TRUE_OBJ if (self._is_truthy(left) and self._is_truthy(right)) else FALSE_OBJ
        elif operator in ("||", "ނުވަތަ"):
            return TRUE_OBJ if (self._is_truthy(left) or self._is_truthy(right)) else FALSE_OBJ

        return DhicodeError(f"ނޭނގޭ އޮޕަރޭޓަރ: {left.type_str()} {operator} {right.type_str()}")

    def _eval_numeric_infix(self, operator: str, left: DhicodeNumber, right: DhicodeNumber) -> DhicodeObject:
        l = left.value
        r = right.value
        if operator == "-":
            return DhicodeNumber(l - r)
        elif operator == "*":
            return DhicodeNumber(l * r)
        elif operator == "/":
            if r == 0:
                return DhicodeError("0 އަށް ބަހައެއް ނުލެވޭނެ (ZeroDivisionError)")
            return DhicodeNumber(l / r)
        elif operator == "%":
            return DhicodeNumber(l % r)
        elif operator == "**":
            try:
                res = l ** r
                if isinstance(res, complex):
                    return DhicodeError("މަންފީ ނަންބަރެއްގެ ފްރެކްޝަނަލް ޕަވަރ އެއް ނުހޯދޭނެ")
                return DhicodeNumber(res)
            except Exception as e:
                return DhicodeError(f"ޕަވަރ ހޯދުމުގައި މައްސަލައެއް: {e}")
        elif operator == "&":
            return DhicodeNumber(int(l) & int(r))
        elif operator == "|":
            return DhicodeNumber(int(l) | int(r))
        elif operator == "^":
            return DhicodeNumber(int(l) ^ int(r))
        elif operator == "<<":
            return DhicodeNumber(int(l) << int(r))
        elif operator == ">>":
            return DhicodeNumber(int(l) >> int(r))
        elif operator == "<":
            return TRUE_OBJ if l < r else FALSE_OBJ
        elif operator == ">":
            return TRUE_OBJ if l > r else FALSE_OBJ
        elif operator == "<=":
            return TRUE_OBJ if l <= r else FALSE_OBJ
        elif operator == ">=":
            return TRUE_OBJ if l >= r else FALSE_OBJ
        elif operator in ("==", "="):
            return TRUE_OBJ if l == r else FALSE_OBJ
        elif operator == "!=":
            return TRUE_OBJ if l != r else FALSE_OBJ
        return DhicodeError(f"ނަންބަރު ތަކަށް ނޭނގޭ އޮޕަރޭޓަރ: {operator}")

    def _is_equal(self, left: DhicodeObject, right: DhicodeObject) -> bool:
        if left is right:
            return True
        if isinstance(left, DhicodeNumber) and isinstance(right, DhicodeNumber):
            return left.value == right.value
        if isinstance(left, DhicodeString) and isinstance(right, DhicodeString):
            return left.value == right.value
        if isinstance(left, DhicodeBoolean) and isinstance(right, DhicodeBoolean):
            return left.value == right.value
        if isinstance(left, DhicodeList) and isinstance(right, DhicodeList):
            if len(left.elements) != len(right.elements):
                return False
            return all(self._is_equal(a, b) for a, b in zip(left.elements, right.elements))
        return False

    def _apply_function(self, fn: DhicodeObject, args: List[DhicodeObject]) -> DhicodeObject:
        if isinstance(fn, DhicodeClass):
            instance = DhicodeInstance(fn)
            ctor = None
            for name in ("constructor", "ހަދާ_ވަޒީފާ", "init"):
                ctor = fn.get_method(name)
                if ctor is not None:
                    break
            if ctor is not None:
                bound_ctor = DhicodeBoundMethod(instance, ctor)
                res = self._apply_function(bound_ctor, args)
                if isinstance(res, DhicodeError):
                    return res
            return instance

        elif isinstance(fn, DhicodeBoundMethod):
            method = fn.method
            extended_env = Environment(method.env)
            extended_env.set("މި", fn.instance)
            extended_env.set("this", fn.instance)
            extended_env.set("self", fn.instance)
            return self._bind_and_eval_function(method, args, extended_env)

        elif isinstance(fn, DhicodeFunction):
            extended_env = Environment(fn.env)
            return self._bind_and_eval_function(fn, args, extended_env)

        elif isinstance(fn, DhicodeBuiltin):
            return fn.fn(*args)

        return DhicodeError(f"މިއީ ވަޒީފާއެއް ނޫން: {fn.type_str()}")

    def _bind_and_eval_function(self, fn: 'DhicodeFunction', args: List[DhicodeObject], env: 'Environment') -> DhicodeObject:
        arg_idx = 0
        for param in fn.parameters:
            param_name = param.name.value if isinstance(param, Parameter) else (param.value if hasattr(param, 'value') else str(param))
            is_variadic = getattr(param, 'is_variadic', False)
            default_expr = getattr(param, 'default', None)

            if is_variadic:
                rest_args = args[arg_idx:] if arg_idx < len(args) else []
                env.set(param_name, DhicodeList(rest_args))
                arg_idx = len(args)
                break
            else:
                if arg_idx < len(args):
                    arg_val = args[arg_idx]
                    arg_idx += 1
                elif default_expr is not None:
                    arg_val = self.eval(default_expr, fn.env)
                    if isinstance(arg_val, DhicodeError):
                        return arg_val
                else:
                    arg_val = NULL_OBJ
                env.set(param_name, arg_val)

        evaluated = self.eval(fn.body, env)
        if isinstance(evaluated, DhicodeReturnValue):
            return evaluated.value
        return evaluated

    def _get_builtin(self, name: str) -> Optional[DhicodeBuiltin]:
        builtins = {
            "ދައްކާ": DhicodeBuiltin(self._builtin_print),
            "ލިޔޭ": DhicodeBuiltin(self._builtin_print),
            "އަހާ": DhicodeBuiltin(self._builtin_input),
            "ދިގުމިން": DhicodeBuiltin(self._builtin_len),
            "ބާވަތް": DhicodeBuiltin(self._builtin_type),
            "އަޅާ": DhicodeBuiltin(self._builtin_append),
            "ނަގާ": DhicodeBuiltin(self._builtin_pop),
            "ތަޅުދަނޑިތައް": DhicodeBuiltin(self._builtin_keys),
            "އަގުތައް": DhicodeBuiltin(self._builtin_values),
            # English aliases
            "print": DhicodeBuiltin(self._builtin_print),
            "input": DhicodeBuiltin(self._builtin_input),
            "len": DhicodeBuiltin(self._builtin_len),
            "type": DhicodeBuiltin(self._builtin_type),
            "append": DhicodeBuiltin(self._builtin_append),
            "push": DhicodeBuiltin(self._builtin_append),
            "pop": DhicodeBuiltin(self._builtin_pop),
            "keys": DhicodeBuiltin(self._builtin_keys),
            "values": DhicodeBuiltin(self._builtin_values),
        }
        return builtins.get(name)

    def _builtin_print(self, *args: DhicodeObject) -> DhicodeObject:
        output = " ".join(arg.inspect() for arg in args)
        self.output_callback(output)
        return NULL_OBJ

    def _builtin_input(self, *args: DhicodeObject) -> DhicodeObject:
        prompt = args[0].inspect() if args else ""
        try:
            val = input(prompt)
            return DhicodeString(val)
        except Exception:
            return DhicodeString("")

    def _builtin_len(self, *args: DhicodeObject) -> DhicodeObject:
        if not args:
            return DhicodeError("ދިގުމިން() ބޭނުންކުރާއިރު އެއްޗެއް ދޭންވާނެ")
        target = args[0]
        if isinstance(target, DhicodeString):
            return DhicodeNumber(len(target.value))
        if isinstance(target, DhicodeList):
            return DhicodeNumber(len(target.elements))
        if isinstance(target, DhicodeDict):
            return DhicodeNumber(len(target.pairs))
        return DhicodeError(f"{target.type_str()} ގެ ދިގުމިނެއް ނުހޯދޭނެ")

    def _builtin_type(self, *args: DhicodeObject) -> DhicodeObject:
        if not args:
            return DhicodeError("ބާވަތް() ބޭނުންކުރާއިރު އެއްޗެއް ދޭންވާނެ")
        return DhicodeString(args[0].type_str())

    def _builtin_append(self, *args: DhicodeObject) -> DhicodeObject:
        if len(args) < 2 or not isinstance(args[0], DhicodeList):
            return DhicodeError("އަޅާ() އަށް ލިސްޓަކާއި އެއްޗެއް ދޭންވާނެ")
        args[0].elements.append(args[1])
        return args[0]

    def _builtin_pop(self, *args: DhicodeObject) -> DhicodeObject:
        if not args or not isinstance(args[0], DhicodeList):
            return DhicodeError("ނަގާ() އަށް ލިސްޓެއް ދޭންވާނެ")
        lst = args[0]
        if not lst.elements:
            return DhicodeError("ހުސް ލިސްޓަކުން އެއްޗެއް ނުނެގޭނެ")
        idx = int(args[1].value) if len(args) > 1 and isinstance(args[1], DhicodeNumber) else -1
        try:
            return lst.elements.pop(idx)
        except IndexError:
            return DhicodeError("ލިސްޓުގެ އިންޑެކްސް އިމުން ބޭރުވެއްޖެ")

    def _builtin_keys(self, *args: DhicodeObject) -> DhicodeObject:
        if not args or not isinstance(args[0], DhicodeDict):
            return DhicodeError("ތަޅުދަނޑިތައް() އަށް ރަދީފެއް ދޭންވާނެ")
        return DhicodeList([DhicodeString(k) for k in args[0].pairs.keys()])

    def _builtin_values(self, *args: DhicodeObject) -> DhicodeObject:
        if not args or not isinstance(args[0], DhicodeDict):
            return DhicodeError("އަގުތައް() އަށް ރަދީފެއް ދޭންވާނެ")
        return DhicodeList(list(args[0].pairs.values()))

    def _interpolate_string(self, s: str, env: Environment) -> DhicodeObject:
        if "{" not in s:
            return DhicodeString(s)

        result = []
        i = 0
        n = len(s)
        while i < n:
            if s[i] == '\\' and i + 1 < n and s[i+1] in ('{', '}'):
                result.append(s[i+1])
                i += 2
            elif s[i] == '{':
                brace_count = 1
                j = i + 1
                in_quote = None
                while j < n and brace_count > 0:
                    ch = s[j]
                    if in_quote:
                        if ch == '\\' and j + 1 < n:
                            j += 1
                        elif ch == in_quote:
                            in_quote = None
                    else:
                        if ch in ('"', "'"):
                            in_quote = ch
                        elif ch == '{':
                            brace_count += 1
                        elif ch == '}':
                            brace_count -= 1
                    if brace_count > 0:
                        j += 1
                if brace_count == 0:
                    expr_str = s[i+1:j].strip()
                    if expr_str:
                        from lexer import Lexer
                        from parser import Parser, Precedence
                        sub_lexer = Lexer(expr_str)
                        sub_parser = Parser(sub_lexer)
                        sub_expr = sub_parser.parse_expression(Precedence.LOWEST)
                        if sub_parser.errors:
                            return DhicodeError(f"ސްޓްރިންގ އިންޓަޕޮލޭޝަން ކުށް: {sub_parser.errors[0]}")
                        val = self.eval(sub_expr, env)
                        if isinstance(val, DhicodeError):
                            return val
                        result.append(val.inspect())
                    i = j + 1
                else:
                    result.append(s[i])
                    i += 1
            else:
                result.append(s[i])
                i += 1

        return DhicodeString("".join(result))
