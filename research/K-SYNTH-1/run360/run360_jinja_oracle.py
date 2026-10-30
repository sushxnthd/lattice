"""Frozen public API oracle for historical Jinja PR1242. Do not edit after outcomes."""
import argparse
import hashlib
import json
import sys

CASES = [
    ("target_scoped_loop","target_public",'{% for i in ["foo", "bar"] %}{% block body scoped %}{{ loop.index }}){{ i }}{% if loop.last %}:last{% endif %};{% endblock %}{% endfor %}',"1)foo;2)bar:last;"),
    ("target_loop_local_context","target_public",'{% set i = 42 %}{% for idx in range(2) %}{% set i = idx %}{% set j = loop.index %}{{ read_ij() }};{% endfor %}{{ i }}',"01;12;42"),
    ("target_block_local_context","target_public",'{% set i = 42 %}{% block body %}{% set i = 24 %}{{ read_i() }}{% endblock %};{{ i }}',"24;42"),
    ("target_nested_scoped_context","target_public",'{% set i = 42 %}{% for idx in range(2) %}{% set i = idx %}{% block body scoped %}{{ read_i() }};{% endblock %}{% endfor %}{{ i }}',"0;1;42"),
    ("target_heldout_shadowed_assignment","target_heldout",'{% set outer = 9 %}{% for idx in [2,3] %}{% set outer = idx %}{{ read_outer() }};{% endfor %}{{ outer }}',"2;3;9"),
    ("target_heldout_block_shadow","target_heldout",'{% set outer = 7 %}{% block x %}{% set outer = 8 %}{{ read_outer() }};{% endblock %}{{ outer }}',"8;7"),
    ("control_plain_scope","control",'{% set i = 42 %}{% for i in [1,2] %}{{ i }};{% endfor %}{{ i }}',"1;2;42"),
    ("control_ordinary_loop_call","control",'{% for i in [1,2] %}{{ ordinary(i) }};{% endfor %}',"ordinary:1;ordinary:2;"),
    ("control_ordinary_block_call","control",'{% block x %}{{ ordinary() }}{% endblock %}',"ordinary:ok"),
    ("control_context_top_level","control",'{% set i = 5 %}{{ read_i() }}',"5"),
    ("control_empty_loop","control",'{% set i = 9 %}{% for idx in [] %}{% set i = idx %}{{ read_i() }}{% endfor %}{{ i }}',"9"),
    ("control_scoped_block_no_loop","control",'{% set i = 3 %}{% block x scoped %}{{ i }}{% endblock %}',"3"),
]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--variant",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    import jinja2
    from jinja2 import Environment
    try:
        from jinja2 import contextfunction
    except ImportError:
        from jinja2 import pass_context as contextfunction
    @contextfunction
    def read_i(ctx): return str(ctx["i"])
    @contextfunction
    def read_ij(ctx): return str(ctx["i"])+str(ctx["j"])
    @contextfunction
    def read_outer(ctx): return str(ctx["outer"])
    def ordinary(value="ok"): return "ordinary:"+str(value)
    records=[]
    for name,kind,template,expected in CASES:
        try:
            env=Environment(autoescape=False)
            env.globals.update(read_i=read_i,read_ij=read_ij,read_outer=read_outer,ordinary=ordinary)
            actual=env.from_string(template).render()
            status="PASS" if actual==expected else "FAIL"
            error=None
        except Exception as e:
            actual=None
            status="ERROR"
            error={"type":type(e).__name__,"message":str(e)}
        records.append({"name":name,"kind":kind,"template_sha256":hashlib.sha256(template.encode()).hexdigest(),"expected":expected,"actual":actual,"status":status,"error":error})
    data={"variant":a.variant,"python":sys.version,"jinja_version":jinja2.__version__,"records":records,"counts":{k:sum(r["status"]==k for r in records) for k in ("PASS","FAIL","ERROR")}}
    with open(a.output,"w",encoding="utf-8") as f:json.dump(data,f,indent=2,sort_keys=True)
    print(json.dumps({"variant":a.variant,"counts":data["counts"],"failures":[r["name"] for r in records if r["status"]!="PASS"]},sort_keys=True))

if __name__=="__main__":main()
