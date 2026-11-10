import ast, json
old = "A | (B | C)"
new = "A | B | C"
class Meta(type):
    def __or__(cls, other):
        trace.append((cls.__name__, getattr(other, "__name__", repr(other))))
        return cls
class A(metaclass=Meta): pass
class B(metaclass=Meta): pass
class C(metaclass=Meta): pass
records = []
for expression in (old, new):
    trace = []
    result = eval(compile(ast.parse(expression, mode="eval"), "<synthetic>", "eval"), {"A": A, "B": B, "C": C})
    records.append({"expression": expression, "trace": trace, "result": result.__name__})
assert records[0]["trace"] != records[1]["trace"]
assert all(r["result"] == "A" for r in records)
print(json.dumps(records, indent=2))
