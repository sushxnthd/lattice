import ast
import unittest
from run374_portable_certificate import certificate
from prior.run373_portable_certificate import certificate as previous

P='def produce(x,y):\n    return x and y\n'
PREFIX='from producer import produce as p\n'


class CertificateTests(unittest.TestCase):
    def test_direct(self):
        self.assertEqual(certificate(P,PREFIX+'def target(x,y):\n    return p(x,y)\n'),'MAY_DEPEND')

    def test_independent(self):
        self.assertEqual(certificate(P,PREFIX+'def target(x,y):\n    return x or y\n'),'NO_DEPENDENCE')

    def test_dynamic_unknown(self):
        self.assertEqual(certificate(P,PREFIX+'def target(x,y):\n    return globals()["p"](x,y)\n'),'UNKNOWN')

    def test_parameter_shadow_unknown(self):
        self.assertEqual(certificate(P,PREFIX+'def target(x,y):\n    return x(x,y)\n'),'UNKNOWN')

    def test_direct_cycle_masked_by_producer(self):
        src=PREFIX+'def target(x,y):\n    return p(x,y) or target(x,y)\n'
        self.assertEqual(previous(P,src),'MAY_DEPEND')
        self.assertEqual(certificate(P,src),'UNKNOWN')

    def test_two_node_cycle_masked(self):
        src=PREFIX+'def target(x,y):\n    return p(x,y) or f(x,y)\ndef f(x,y):\n    return target(x,y)\n'
        self.assertEqual(previous(P,src),'MAY_DEPEND')
        self.assertEqual(certificate(P,src),'UNKNOWN')

    def test_unreachable_cycle_is_unknown(self):
        src=PREFIX+'def target(x,y):\n    return x\ndef f(x,y):\n    return f(x,y)\n'
        self.assertEqual(previous(P,src),'NO_DEPENDENCE')
        self.assertEqual(certificate(P,src),'UNKNOWN')

    def test_false_and_cycle_still_unknown(self):
        src=PREFIX+'def target(x,y):\n    return False and target(x,y)\n'
        self.assertEqual(certificate(P,src),'UNKNOWN')

    def test_acyclic_two_hop(self):
        src=PREFIX+'def target(x,y):\n    return f(x,y)\ndef f(x,y):\n    return p(x,y)\n'
        self.assertEqual(certificate(P,src),'MAY_DEPEND')

    def test_alias(self):
        src=PREFIX+'q = p\ndef target(x,y):\n    return q(x,y)\n'
        self.assertEqual(certificate(P,src),'MAY_DEPEND')

    def test_noncallable_parameter(self):
        src=PREFIX+'def target(x,y):\n    return y(x,y)\n'
        self.assertEqual(certificate(P,src),'UNKNOWN')

    def test_reject_comprehension(self):
        src=PREFIX+'def target(x,y):\n    return [p(x,y)]\n'
        self.assertEqual(certificate(P,src),'UNKNOWN')

    def test_reject_decorator(self):
        src=PREFIX+'@p\ndef target(x,y):\n    return True\n'
        self.assertEqual(certificate(P,src),'UNKNOWN')

    def test_reject_import_side_effect(self):
        src='import os\n'+PREFIX+'def target(x,y):\n    return x\n'
        self.assertEqual(certificate(P,src),'UNKNOWN')

    def test_valid_no_graph(self):
        src=PREFIX+'def f(x,y):\n    return not x\ndef target(x,y):\n    return f(x,y) or y\n'
        self.assertEqual(certificate(P,src),'NO_DEPENDENCE')

    def test_long_source_unknown(self):
        self.assertEqual(certificate(P,PREFIX+'#'*70000),'UNKNOWN')


if __name__=='__main__':
    unittest.main(verbosity=2)
