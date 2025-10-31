from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any, Dict

# ----- Element interface ------------------------------------------------------
class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor") -> Any:
        ...

# ----- Visitor interface ------------------------------------------------------
class Visitor(ABC):
    """Base visitor with a safe fallback."""
    def generic_visit(self, node: Expr) -> Any:
        raise NotImplementedError(f"No visit method for {type(node).__name__}")

    # Optional: generic dispatcher if a node forgets to override accept()
    def visit(self, node: Expr) -> Any:
        meth_name = f"visit_{type(node).__name__}"
        meth = getattr(self, meth_name, self.generic_visit)
        return meth(node)

# ----- Concrete nodes ---------------------------------------------------------
@dataclass(frozen=True)
class Number(Expr):
    value: float
    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_Number(self)

@dataclass(frozen=True)
class Var(Expr):
    name: str
    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_Var(self)

@dataclass(frozen=True)
class Add(Expr):
    left: Expr
    right: Expr
    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_Add(self)

@dataclass(frozen=True)
class Mul(Expr):
    left: Expr
    right: Expr
    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_Mul(self)

# ----- Concrete visitors ---------------------------------------------------------

class Evaluator(Visitor):
    def __init__(self, env: Dict[str, float] | None = None):
        self.env = env or {}

    def visit_Number(self, node: Number) -> float:
        return node.value

    def visit_Var(self, node: Var) -> float:
        if node.name not in self.env:
            raise NameError(f"Undefined variable: {node.name}")
        return self.env[node.name]

    def visit_Add(self, node: Add) -> float:
        return node.left.accept(self) + node.right.accept(self)

    def visit_Mul(self, node: Mul) -> float:
        return node.left.accept(self) * node.right.accept(self)

class PrettyPrinter(Visitor):
    def visit_Number(self, node: Number) -> str:
        # Render integers nicely (no trailing .0)
        v = int(node.value) if node.value.is_integer() else node.value
        return str(v)

    def visit_Var(self, node: Var) -> str:
        return node.name

    def visit_Add(self, node: Add) -> str:
        return f"({node.left.accept(self)} + {node.right.accept(self)})"

    def visit_Mul(self, node: Mul) -> str:
        # Multiplication binds tighter than addition, but we’re simple here
        return f"({node.left.accept(self)} * {node.right.accept(self)})"

class NodeCounter(Visitor):
    def __init__(self):
        self.counts: Dict[str, int] = {}

    def _bump(self, cls_name: str):
        self.counts[cls_name] = self.counts.get(cls_name, 0) + 1

    def visit_Number(self, node: Number) -> int:
        self._bump("Number")
        return 1

    def visit_Var(self, node: Var) -> int:
        self._bump("Var")
        return 1

    def visit_Add(self, node: Add) -> int:
        self._bump("Add")
        return 1 + node.left.accept(self) + node.right.accept(self)

    def visit_Mul(self, node: Mul) -> int:
        self._bump("Mul")
        return 1 + node.left.accept(self) + node.right.accept(self)

# Build a nested AST
ast = Mul(
    Add(Number(2), Var("x")),
    Add(Number(3), Number(4))
)

# Pretty print
pp = PrettyPrinter()
print("Expr:", ast.accept(pp))
# -> Expr: ((2 + x) * (3 + 4))

# Evaluate with a variable environment
ev = Evaluator({"x": 10})
print("Value:", ast.accept(ev))
# -> Value: 2 + 10 = 12; 3 + 4 = 7; 12 * 7 = 84

# Count nodes
nc = NodeCounter()
total = ast.accept(nc)
print("Total nodes:", total, "| breakdown:", nc.counts)