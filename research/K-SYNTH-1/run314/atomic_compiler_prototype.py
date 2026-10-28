"""Bounded, byte-safe atomic constant edit compiler; never executes model code.

This is an experimental component, not a general-purpose Python editor.
"""
import ast
import hashlib


class PatchRejected(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_python_ast_action(expression: str) -> int:
    """Accept only literal ast.Constant(value=INTEGER) constructor syntax."""
    try:
        node = ast.parse(expression, mode="eval").body
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "ast" and node.func.attr == "Constant"
                and not node.args and len(node.keywords) == 1
                and node.keywords[0].arg == "value"
                and isinstance(node.keywords[0].value, ast.Constant)
                and type(node.keywords[0].value.value) is int):
            raise PatchRejected("unsupported AST action")
        return node.keywords[0].value.value
    except (SyntaxError, TypeError) as exc:
        raise PatchRejected("invalid AST action") from exc


def compile_replace_constant(source: bytes, *, expected_source_sha: str,
                             expected_node_sha: str, old: int, new: int) -> bytes:
    """Return complete patched bytes or reject; caller decides whether to write.

    Reject ambiguous targets and stale preconditions. AST offsets are UTF-8 bytes.
    """
    if digest(source) != expected_source_sha:
        raise PatchRejected("stale source")
    if type(old) is not int or type(new) is not int or not (0 <= new < 100000):
        raise PatchRejected("invalid edit value")
    try:
        tree = ast.parse(source.decode("utf-8"))
    except (SyntaxError, UnicodeError) as exc:
        raise PatchRejected("invalid source") from exc
    nodes = [node for node in ast.walk(tree)
             if isinstance(node, ast.Constant) and type(node.value) is int
             and node.value == old]
    if len(nodes) != 1:
        raise PatchRejected("ambiguous or absent anchor")
    node = nodes[0]
    if digest(ast.dump(node, include_attributes=False).encode()) != expected_node_sha:
        raise PatchRejected("stale AST node")
    if node.lineno != node.end_lineno:
        raise PatchRejected("multiline node unsupported")
    lines = source.splitlines(keepends=True)
    start = sum(map(len, lines[:node.lineno - 1])) + node.col_offset
    stop = sum(map(len, lines[:node.end_lineno - 1])) + node.end_col_offset
    if source[start:stop] != str(old).encode("ascii"):
        raise PatchRejected("source span not a canonical integer literal")
    patched = source[:start] + str(new).encode("ascii") + source[stop:]
    try:
        ast.parse(patched.decode("utf-8"))
    except (SyntaxError, UnicodeError) as exc:
        raise PatchRejected("invalid compiled patch") from exc
    return patched
