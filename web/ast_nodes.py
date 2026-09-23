# ast_nodes.py
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from lexer import Token

class Node(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    def __init__(self):
        self.statements: List[Statement] = []

    def token_literal(self) -> str:
        if self.statements:
            return self.statements[0].token_literal()
        return ""

    def __str__(self) -> str:
        return "\n".join(str(s) for s in self.statements)

class BlockStatement(Statement):
    def __init__(self, token: Token, statements: Optional[List[Statement]] = None):
        self.token = token
        self.statements: List[Statement] = statements if statements is not None else []

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return "\n".join(str(s) for s in self.statements)

class LetStatement(Statement):
    def __init__(self, token: Token, name: 'Identifier', value: Optional[Expression] = None):
        self.token = token
        self.name = name
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        val_str = str(self.value) if self.value else ""
        return f"{self.token_literal()} {str(self.name)} = {val_str};"

class ConstStatement(Statement):
    def __init__(self, token: Token, name: 'Identifier', value: Optional[Expression] = None):
        self.token = token
        self.name = name
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        val_str = str(self.value) if self.value else ""
        return f"{self.token_literal()} {str(self.name)} = {val_str};"

class AssignmentStatement(Statement):
    def __init__(self, token: Token, name: 'Identifier', operator: str, value: Expression):
        self.token = token
        self.name = name
        self.operator = operator
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"{str(self.name)} {self.operator} {str(self.value)};"

class IndexAssignmentStatement(Statement):
    def __init__(self, token: Token, target: Expression, index: Expression, operator: str, value: Expression):
        self.token = token
        self.target = target
        self.index = index
        self.operator = operator
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"{str(self.target)}[{str(self.index)}] {self.operator} {str(self.value)};"

class ReturnStatement(Statement):
    def __init__(self, token: Token, return_value: Optional[Expression] = None):
        self.token = token
        self.return_value = return_value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        val_str = str(self.return_value) if self.return_value else ""
        return f"{self.token_literal()} {val_str};"

class PrintStatement(Statement):
    def __init__(self, token: Token, value: Expression):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"{self.token_literal()} {str(self.value)};"

class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Optional[Expression] = None):
        self.token = token
        self.expression = expression

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return str(self.expression) if self.expression else ""

class IfStatement(Statement):
    def __init__(self, token: Token, condition: Expression, consequence: BlockStatement, alternative: Optional[BlockStatement] = None):
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        res = f"ނަމަ {str(self.condition)}\n{str(self.consequence)}"
        if self.alternative:
            res += f"\nނޫންނަމަ\n{str(self.alternative)}"
        res += "\nނިމުނީ"
        return res

class WhileStatement(Statement):
    def __init__(self, token: Token, condition: Expression, body: BlockStatement):
        self.token = token
        self.condition = condition
        self.body = body

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"ހިނދު {str(self.condition)}\n{str(self.body)}\nނިމުނީ"

class ForInStatement(Statement):
    def __init__(self, token: Token, item: 'Identifier', iterable: Expression, body: BlockStatement):
        self.token = token
        self.item = item
        self.iterable = iterable
        self.body = body

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"ކޮންމެ {str(self.item)} ތެރޭގައި {str(self.iterable)}\n{str(self.body)}\nނިމުނީ"

class FunctionStatement(Statement):
    def __init__(self, token: Token, name: 'Identifier', parameters: List['Identifier'], body: BlockStatement):
        self.token = token
        self.name = name
        self.parameters = parameters
        self.body = body

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        params = ", ".join(str(p) for p in self.parameters)
        return f"ވަޒީފާ {str(self.name)}({params})\n{str(self.body)}\nނިމުނީ"

class ImportStatement(Statement):
    def __init__(self, token: Token, path: str):
        self.token = token
        self.path = path

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f'ގެނޭ "{self.path}";'

class TryCatchStatement(Statement):
    def __init__(self, token: Token, try_block: BlockStatement, error_var: Optional['Identifier'], catch_block: BlockStatement):
        self.token = token
        self.try_block = try_block
        self.error_var = error_var
        self.catch_block = catch_block

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        var_str = f" {str(self.error_var)}" if self.error_var else ""
        return f"މަސައްކަތްކުރޭ\n{str(self.try_block)}\nކުށެއް_ފެނިއްޖެނަމަ{var_str}\n{str(self.catch_block)}\nނިމުނީ"

class ThrowStatement(Statement):
    def __init__(self, token: Token, expr: Expression):
        self.token = token
        self.expr = expr

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"އުކާލާ {str(self.expr)};"

# Expressions

class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.value

class NumberLiteral(Expression):
    def __init__(self, token: Token, value: float):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        if isinstance(self.value, (int, float)) and (isinstance(self.value, int) or self.value.is_integer()):
            return str(int(self.value))
        return str(self.value)

class StringLiteral(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f'"{self.value}"'

class BooleanLiteral(Expression):
    def __init__(self, token: Token, value: bool):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return "އާން" if self.value else "ނޫން"

class NullLiteral(Expression):
    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return "ހުސް"

class ListLiteral(Expression):
    def __init__(self, token: Token, elements: List[Expression]):
        self.token = token
        self.elements = elements

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        elems = ", ".join(str(e) for e in self.elements)
        return f"[{elems}]"

class DictLiteral(Expression):
    def __init__(self, token: Token, pairs: Dict[Expression, Expression]):
        self.token = token
        self.pairs = pairs

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        items = ", ".join(f"{str(k)}: {str(v)}" for k, v in self.pairs.items())
        return f"{{{items}}}"

class IndexExpression(Expression):
    def __init__(self, token: Token, left: Expression, index: Expression):
        self.token = token
        self.left = left
        self.index = index

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({str(self.left)}[{str(self.index)}])"

class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str, right: Expression):
        self.token = token
        self.operator = operator
        self.right = right

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({self.operator}{str(self.right)})"

class InfixExpression(Expression):
    def __init__(self, token: Token, left: Expression, operator: str, right: Expression):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({str(self.left)} {self.operator} {str(self.right)})"

class CallExpression(Expression):
    def __init__(self, token: Token, function: Expression, arguments: List[Expression]):
        self.token = token
        self.function = function
        self.arguments = arguments

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        args = ", ".join(str(a) for a in self.arguments)
        return f"{str(self.function)}({args})"