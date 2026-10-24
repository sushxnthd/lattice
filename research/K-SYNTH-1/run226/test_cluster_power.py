import unittest
from cluster_power import simulate, SEED

class ClusterPowerTests(unittest.TestCase):
    def test_reproducible(self):
        args=(65,4,.3,.6,.3,2000,SEED)
        self.assertEqual(simulate(*args),simulate(*args))
    def test_no_clustering(self):
        r=simulate(65,4,.3,.6,0,2000,SEED)
        self.assertEqual(r["induced_issue_ICC"],0)
        self.assertEqual(r["design_effect"],1)
    def test_expected_icc(self):
        r=simulate(65,4,.3,.6,.3,2000,SEED)
        q,p,rho=.3,.6,.3
        expected=4*q*q*p*(1-p)*rho/(q-(q*(2*p-1))**2)
        self.assertAlmostEqual(r["induced_issue_ICC"],expected,places=4)
    def test_probability_validation(self):
        for q,p,rho in [(0,.6,0),(.3,.4,0),(.3,.6,1)]:
            with self.assertRaises(ValueError):
                simulate(65,4,q,p,rho,100,SEED)
    def test_power_range(self):
        r=simulate(65,4,.3,.6,.3,2000,SEED)
        self.assertGreaterEqual(r["power"],0)
        self.assertLessEqual(r["power"],1)
        self.assertGreater(r["mc_se"],0)

if __name__=="__main__":unittest.main()
