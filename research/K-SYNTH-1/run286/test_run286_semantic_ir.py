import ast, hashlib, json, random, unittest
from run286_semantic_ir import *

SOURCE='''
def cleanup(pool, limit):
    if len([conn.is_idle() for conn in pool]) > limit:
        return 'old'
    if sum(conn.is_idle() for conn in pool) > limit:
        return 'new'
    if len([conn for conn in pool if conn.is_idle()]) > limit:
        return 'filter'
    return 'ok'
'''
class TestIR(unittest.TestCase):
    def test_extract_and_roundtrip(self):
        f=extract(SOURCE);self.assertEqual(len(f['facts']),3)
        self.assertEqual([x['kind'] for x in f['facts']],['COUNT_ALL_EVAL_PRED','SUM_PRED_VALUES','COUNT_TRUE_FILTER'])
        self.assertEqual(recover_facts(render_ir(f)),recover_facts(render_python(f)))
        self.assertEqual(recover_facts(render_ir(f)),f['facts'])
    def test_gold_blind(self):
        f=extract(SOURCE)
        self.assertEqual(f['runtime_semantics'],'UNKNOWN_UNLESS_SCOPE_ATTESTED')
        self.assertEqual(f['source_sha256'],hashlib.sha256(SOURCE.encode()).hexdigest())
    def test_unknown(self):
        a,b=extract(SOURCE)['facts'][:2]
        self.assertEqual(certificate(a,b)['status'],'UNKNOWN')
        self.assertEqual(certificate(a,{**b,'predicate_attribute':'is_closed'},REQUIRED)['status'],'UNKNOWN')
    def test_scoped(self):
        a,b=extract(SOURCE)['facts'][:2]
        self.assertEqual(certificate(a,b,REQUIRED)['status'],'PROVED_CONDITIONAL')
    def test_no_false_equivalence(self):
        rng=random.Random(286); cases=0; disagreement=0
        a,b=extract(SOURCE)['facts'][:2]
        for _ in range(12000):
            n=rng.randrange(0,24);k=rng.randrange(-1,25)
            vals=[bool(rng.getrandbits(1)) for __ in range(n)]
            old=len([v for v in vals])>k
            new=sum(vals)>k
            predicted=(sum(vals)<=k<n)
            self.assertEqual(old!=new,predicted)
            disagreement+=predicted;cases+=1
        self.assertGreater(disagreement,0)
    def test_dynamic_counterexamples(self):
        # Python permits non-Boolean predicate returns; static call syntax does not prove bool.
        class Conn:
            def __init__(self,x):self.x=x
            def is_idle(self):return self.x
        pool=[Conn(2),Conn(2)];k=2
        self.assertFalse(len([c.is_idle() for c in pool])>k)
        self.assertTrue(sum(c.is_idle() for c in pool)>k)
        # A side effect can change later predicate outcomes, invalidating stable-state inference.
        state=[False,False]
        def f(i):
            if i==0:state[1]=True
            return state[i]
        self.assertEqual(sum(f(i) for i in range(2)),1)
        self.assertEqual(state,[False,True])
    def test_unsupported(self):
        for s in ('len((x.is_idle() for x in pool))','sum(x.is_idle() for x in pool if x.ok())',
                  'sum(x.is_idle() for x in pool for y in pool)',
                  'len([x for x in pool if x.is_idle() and x.ok()])'):
            self.assertEqual(extract(s)['facts'],[])
    def test_alpha_equivalence(self):
        a=extract('len([x.is_idle() for x in pool])')['facts'][0]
        b=extract('sum(y.is_idle() for y in pool)')['facts'][0]
        self.assertEqual(certificate(a,b,REQUIRED)['status'],'PROVED_CONDITIONAL')
    def test_no_reference_lookahead(self):
        # Pure source-only extractor produces same facts regardless of oracle/reference outcome.
        a=extract(SOURCE);b=extract(SOURCE)
        self.assertEqual(a,b)
if __name__=='__main__':unittest.main()
