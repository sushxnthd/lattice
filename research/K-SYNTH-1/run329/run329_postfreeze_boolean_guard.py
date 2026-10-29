"""POSTFREEZE SECURITY CORRECTION: reject executable default expressions.

The original Run329 compiler and original frozen 256+128 outcomes remain unchanged.
This adapter is mandatory before any future untrusted model-output transaction.
"""
import ast
from run329_signature_editor import compile_transaction, Rejected


def compile_boolean_defaults(sources, authority, edits):
    for edit in edits:
        if not isinstance(edit, dict) or not isinstance(edit.get('new_expr'), str):
            raise Rejected('INVALID_BOOLEAN_EDIT')
        try:
            expr = ast.parse(edit['new_expr'], mode='eval').body
        except SyntaxError as exc:
            raise Rejected('INVALID_BOOLEAN_SYNTAX') from exc
        if not isinstance(expr, ast.Constant) or type(expr.value) is not bool:
            raise Rejected('NON_LITERAL_BOOLEAN_DEFAULT')
    return compile_transaction(sources, authority, edits)
