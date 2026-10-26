import ast
import random
import re
import unittest
from slash_quantifier_ir import transfer, classify_call

class CertifiedSlashTransducer(unittest.TestCase):
    def test_1024_deterministic_equivalence(self):
        rng = random.Random(2782026)
        for i in range(1024):
            s = ''.join(rng.choice('/ab0._') for _ in range(rng.randrange(0, 300)))
            for p in ('/{2,}?', '/{2,}'):
                r = transfer(p, '/', s)
                self.assertEqual(r.kind, 'EXACT')
                self.assertEqual(r.value, re.sub(p, '/', s), (i, p))

    def test_512_all_slash_runs(self):
        for n in range(513):
            self.assertEqual(transfer('/{2,}?', '/', '/'*n).value, '/'*((n+1)//2))
            self.assertEqual(transfer('/{2,}', '/', '/'*n).value, '/'*min(n,1))

    def test_open_world_unknown(self):
        for args in [('/+', '/', '//'), ('/{2,}?', 'X', '//'), ('/{2,}?', '/', None)]:
            self.assertEqual(transfer(*args).kind, 'UNKNOWN')
        self.assertEqual(transfer('/{2,}?', '/', '//', flags=1).kind, 'UNKNOWN')

    def test_binding_not_assumed(self):
        a = ast.parse("re.sub('/{2,}?', '/', path)", mode='eval').body
        self.assertEqual(classify_call(a), 'MAY_LITERAL_RE_SUB_UNRESOLVED_BINDING')
        b = ast.parse("something.sub('/{2,}?', '/', path)", mode='eval').body
        self.assertEqual(classify_call(b), 'UNKNOWN')

    def test_non_monotone_odd_slashes(self):
        self.assertEqual(transfer('/{2,}?', '/', '///').value, '//')
        self.assertEqual(transfer('/{2,}', '/', '///').value, '/')

if __name__ == '__main__':
    unittest.main()
