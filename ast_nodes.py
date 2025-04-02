# ast_nodes.py
from abc import ABC, abstractmethod
from lexer import Token # We need the Token class for holding token info

# --- Base Nodes ---
# Using Abstract Base Classes (ABC) to define interfaces

class Node(ABC):
    """Base class for all AST nodes."""
    @abstractmethod
    def token_literal(self) -> str:
        """Returns the literal value of the token associated with this node."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Provides a string representation of the node (for debugging)."""
        pass

class Statement(Node):
    """Base class for all statement nodes."""
    # Statements don't produce values (unlike expressions)
    pass

class Expression(Node):
    """Base class for all expression nodes."""
    # Expressions produce values
    pass

# --- Concrete Node Classes ---

class Program(Node):
    """The root node of the entire program AST."""
    def __init__(self):
        self.statements: list[Statement] = []

    def token_literal(self) -> str:
        if self.statements:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self) -> str:
        return "".join(str(stmt) for stmt in self.statements)

# --- Statement Nodes ---

class LetStatement(Statement):
    """Represents a 'ކަނޑައަޅާ' statement."""
    def __init__(self, token: Token, name: 'Identifier', value: Expression):
        self.token = token # The 'ކަނޑައަޅާ' token
        self.name = name   # The Identifier node (e.g., for 'އުމުރު')
        self.value = value # The Expression node being assigned

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"{self.token_literal()} {str(self.name)} = {str(self.value)};" # Adding ; for clarity

# Maybe add ReturnStatement, BlockStatement later

class ExpressionStatement(Statement):
    """Represents a statement that consists of a single expression."""
    # e.g., "ދައްކާ(...)" or just "5 + 10" on a line
    def __init__(self, token: Token, expression: Expression):
        self.token = token # The first token of the expression
        self.expression = expression

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return str(self.expression)

# --- Expression Nodes ---

class Identifier(Expression):
    """Represents an identifier used as an expression."""
    def __init__(self, token: Token, value: str):
        self.token = token # The IDENTIFIER token
        self.value = value # The actual name (e.g., 'އުމުރު')

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.value

class NumberLiteral(Expression):
    """Represents a numeric literal."""
    def __init__(self, token: Token, value: float):
        self.token = token # The NUMBER token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        # Avoid ".0" for integers in string representation
        if isinstance(self.value, int) or self.value.is_integer():
             return str(int(self.value))
        return str(self.value)


class StringLiteral(Expression):
    """Represents a string literal."""
    def __init__(self, token: Token, value: str):
        self.token = token # The STRING token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        # Return the raw string value for representation
        # Could also return f'"{self.value}"' if quotes are desired
        return f'"{self.value}"'


# --- Compound Expressions ---

class InfixExpression(Expression):
    """Represents an infix operation (e.g., x + y, a > b)."""
    def __init__(self, token: Token, left: Expression, operator: str, right: Expression):
        self.token = token     # The operator token (e.g., +, >)
        self.left = left       # The expression on the left
        self.operator = operator # The operator string (e.g., "+", ">")
        self.right = right     # The expression on the right

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({str(self.left)} {self.operator} {str(self.right)})"

# Add PrefixExpression (e.g., -5, !true) later if needed
# Add CallExpression (for function calls like ދައްކާ(...)) later