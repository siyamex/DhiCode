# evaluator.py
from typing import Dict, Any, Optional, List
from ast_nodes import (
    Node, Program, BlockStatement, LetStatement, ReturnStatement,
    PrintStatement, ExpressionStatement, IfStatement, WhileStatement,
    FunctionStatement, Identifier, NumberLiteral, StringLiteral,
    BooleanLiteral, PrefixExpression, InfixExpression, CallExpression
)

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
    def __init__(self, message: str):
        self.message = message

    def type_str(self) -> str:
        return "ކުށް"

    def inspect(self) -> str:
        return f"ކުށް: {self.message}"

class DhicodeFunction(DhicodeObject):
    def __init__(self, parameters: List[Identifier], body: BlockStatement, env: 'Environment'):
        self.parameters = parameters
        self.body = body
        self.env = env

    def type_str(self) -> str:
        return "ވަޒީފާ"

    def inspect(self) -> str:
        params = ", ".join(p.value for p in self.parameters)
        return f"ވަޒީފާ({params})"

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
        self.outer = outer

    def get(self, name: str) -> Optional[DhicodeObject]:
        if name in self.store:
            return self.store[name]
        if self.outer is not None:
            return self.outer.get(name)
        return None

    def set(self, name: str, val: DhicodeObject) -> DhicodeObject:
        self.store[name] = val
        return val

# --- Evaluator ---

class Evaluator:
    def __init__(self, output_callback=None):
        self.output_callback = output_callback if output_callback else print

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
            env.set(node.name.value, val)
            return val

        elif isinstance(node, ReturnStatement):
            val = self.eval(node.return_value, env) if node.return_value else NULL_OBJ
            if isinstance(val, DhicodeError):
                return val
            return DhicodeReturnValue(val)

        elif isinstance(node, PrintStatement):
            val = self.eval(node.value, env)
            if isinstance(val, DhicodeError):
                return val
            self.output_callback(val.inspect())
            return NULL_OBJ

        elif isinstance(node, ExpressionStatement):
            return self.eval(node.expression, env)

        elif isinstance(node, IfStatement):
            return self._eval_if_statement(node, env)

        elif isinstance(node, WhileStatement):
            return self._eval_while_statement(node, env)

        elif isinstance(node, FunctionStatement):
            fn = DhicodeFunction(node.parameters, node.body, env)
            env.set(node.name.value, fn)
            return fn

        # Expressions
        elif isinstance(node, Identifier):
            return self._eval_identifier(node, env)

        elif isinstance(node, NumberLiteral):
            return DhicodeNumber(node.value)

        elif isinstance(node, StringLiteral):
            return DhicodeString(node.value)

        elif isinstance(node, BooleanLiteral):
            return TRUE_OBJ if node.value else FALSE_OBJ

        elif isinstance(node, PrefixExpression):
            right = self.eval(node.right, env)
            if isinstance(right, DhicodeError):
                return right
            return self._eval_prefix_expression(node.operator, right)

        elif isinstance(node, InfixExpression):
            left = self.eval(node.left, env)
            if isinstance(left, DhicodeError):
                return left
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

        return NULL_OBJ

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

    def _eval_identifier(self, node: Identifier, env: Environment) -> DhicodeObject:
        val = env.get(node.value)
        if val is not None:
            return val
        # Check builtins
        builtin = self._get_builtin(node.value)
        if builtin is not None:
            return builtin
        return DhicodeError(f"ނޭނގޭ ނަމެއް: '{node.value}'")

    def _is_truthy(self, obj: DhicodeObject) -> bool:
        if obj is NULL_OBJ:
            return False
        if isinstance(obj, DhicodeBoolean):
            return obj.value
        if isinstance(obj, DhicodeNumber):
            return obj.value != 0
        if isinstance(obj, DhicodeString):
            return len(obj.value) > 0
        return True

    def _eval_prefix_expression(self, operator: str, right: DhicodeObject) -> DhicodeObject:
        if operator == "!":
            return FALSE_OBJ if self._is_truthy(right) else TRUE_OBJ
        elif operator == "-":
            if not isinstance(right, DhicodeNumber):
                return DhicodeError(f"ނަންބަރެއް ނޫން އަދަދަކަށް '-' ބޭނުމެއް ނުކުރެވޭނެ: {right.type_str()}")
            return DhicodeNumber(-right.value)
        return DhicodeError(f"ނޭނގޭ އޮޕަރޭޓަރ: {operator}{right.type_str()}")

    def _eval_infix_expression(self, operator: str, left: DhicodeObject, right: DhicodeObject) -> DhicodeObject:
        # String concatenation or coercion
        if operator == "+":
            if isinstance(left, DhicodeString) or isinstance(right, DhicodeString):
                return DhicodeString(left.inspect() + right.inspect())
            if isinstance(left, DhicodeNumber) and isinstance(right, DhicodeNumber):
                return DhicodeNumber(left.value + right.value)
            return DhicodeError(f"'+' ބޭނުމެއް ނުކުރެވޭނެ {left.type_str()} އަދި {right.type_str()} އާ ދެމެދު")

        # Arithmetic
        if isinstance(left, DhicodeNumber) and isinstance(right, DhicodeNumber):
            return self._eval_numeric_infix(operator, left, right)

        # Boolean logic
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
                return DhicodeError("0 އަށް ބަހައެއް ނުލެވޭނެ")
            return DhicodeNumber(l / r)
        elif operator == "%":
            return DhicodeNumber(l % r)
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
        return False

    def _apply_function(self, fn: DhicodeObject, args: List[DhicodeObject]) -> DhicodeObject:
        if isinstance(fn, DhicodeFunction):
            extended_env = Environment(fn.env)
            for i, param in enumerate(fn.parameters):
                arg_val = args[i] if i < len(args) else NULL_OBJ
                extended_env.set(param.value, arg_val)

            evaluated = self.eval(fn.body, extended_env)
            if isinstance(evaluated, DhicodeReturnValue):
                return evaluated.value
            return evaluated
        elif isinstance(fn, DhicodeBuiltin):
            return fn.fn(*args)
        return DhicodeError(f"މިއީ ވަޒީފާއެއް ނޫން: {fn.type_str()}")

    def _get_builtin(self, name: str) -> Optional[DhicodeBuiltin]:
        builtins = {
            "ދައްކާ": DhicodeBuiltin(self._builtin_print),
            "ލިޔޭ": DhicodeBuiltin(self._builtin_print),
            "އަހާ": DhicodeBuiltin(self._builtin_input),
            "ދިގުމިން": DhicodeBuiltin(self._builtin_len),
            "ބާވަތް": DhicodeBuiltin(self._builtin_type),
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
        return DhicodeError(f"{target.type_str()} ގެ ދިގުމިނެއް ނުހޯދޭނެ")

    def _builtin_type(self, *args: DhicodeObject) -> DhicodeObject:
        if not args:
            return DhicodeError("ބާވަތް() ބޭނުންކުރާއިރު އެއްޗެއް ދޭންވާނެ")
        return DhicodeString(args[0].type_str())
