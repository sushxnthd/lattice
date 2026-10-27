import unittest
from run282_interval_semantic_ir import CardinalityFacts, REQUIRED, classify, exact_pattern_match, verify

A={x:True for x in REQUIRED}
class Run282Tests(unittest.TestCase):
    def test_recognize_only_exact(self):
        self.assertTrue(exact_pattern_match())
        self.assertFalse(exact_pattern_match('len(xs)>k','sum(xs)>k'))
        self.assertFalse(exact_pattern_match('len([c.is_idle() for c in self._connections]) > self._max_keepalive_connections'))
    def test_must_agree(self):
        self.assertEqual(classify(CardinalityFacts(3,0,3,4,A)),'MUST_AGREE')
        self.assertEqual(classify(CardinalityFacts(3,2,3,1,A)),'MUST_AGREE')
    def test_must_diverge(self):
        self.assertEqual(classify(CardinalityFacts(3,0,1,1,A)),'MUST_DIVERGE')
    def test_may_diverge(self):
        self.assertEqual(classify(CardinalityFacts(3,0,2,1,A)),'MAY_DIVERGE')
    def test_unknown_contract(self):
        for key in REQUIRED:
            bad=A.copy();bad.pop(key)
            self.assertEqual(classify(CardinalityFacts(3,0,2,1,bad)),'UNKNOWN')
    def test_unknown_bounds(self):
        self.assertEqual(classify(CardinalityFacts(3,2,4,1,A)),'UNKNOWN')
        self.assertEqual(classify(CardinalityFacts(3,2,1,1,A)),'UNKNOWN')
        self.assertEqual(classify(CardinalityFacts(3,0,1,True,A)),'UNKNOWN')
    def test_views_equivalent(self):
        f=CardinalityFacts(3,0,2,1,A)
        self.assertEqual(f.to_ir()['facts'],f.to_python_baseline())
    def test_exhaustive_small(self):
        s=verify(5)
        self.assertEqual(s['oracle_mismatches'],0)
        self.assertGreater(s['interval_cases'],100)
if __name__=='__main__':unittest.main()
