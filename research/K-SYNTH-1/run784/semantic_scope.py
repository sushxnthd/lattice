"""Conservative syntactic MAY-dependency analyzer; primitive bool/int domain only."""
import ast
from dataclasses import dataclass

@dataclass(frozen=True)
class Result:
    status: str
    dependencies: tuple[str, ...]
    diagnostic: str

class Unknown(Exception):
    pass

def analyze(source: str, allowed: set[str]) -> Result:
    try:
        tree = ast.parse(source, mode="eval")
        def visit(node):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id not in allowed: raise Unknown("unbound name")
                return {node.id}
            if isinstance(node, ast.Constant) and type(node.value) in (bool, int): return set()
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.Not, ast.USub)):
                return visit(node.operand)
            if isinstance(node, ast.BoolOp) and isinstance(node.op, (ast.And, ast.Or)):
                return set().union(*(visit(x) for x in node.values))
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.Add, ast.Sub)):
                return visit(node.left) | visit(node.right)
            if isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(node.ops[0], (ast.Eq, ast.NotEq)):
                return visit(node.left) | visit(node.comparators[0])
            raise Unknown("unsupported syntax: " + type(node).__name__)
        return Result("CERTIFIED", tuple(sorted(visit(tree.body))), "bounded syntactic MAY-dependencies")
    except (SyntaxError, Unknown, RecursionError) as e:
        return Result("UNKNOWN", (), str(e))
