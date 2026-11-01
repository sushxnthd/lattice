import ast,hashlib,unittest
from pathlib import Path
import run416_httpx_issue1404_oracle as oracle

class FrozenOracleContract(unittest.TestCase):
    def test_frozen_expected_rows(self):
        rows={'public_sync_302':{'path':'/pub-final','cookie':'sid=public-sync','marker':None},
              'public_async_302':{'path':'/pub-final','cookie':'sid=public-async','marker':None},
              'heldout_sync_307':{'path':'/held-final','cookie':'sid=held-sync','marker':'heldout'},
              'heldout_async_two_hops':{'path':'/held-final2','cookie':'sid=held-async','marker':'heldout-async'},
              'control_direct_cookie':{'path':'/direct','cookie':'sid=direct-control','marker':None},
              'control_no_cookie':{'path':'/direct','cookie':None,'marker':None}}
        self.assertEqual(oracle.classify(rows),{k:True for k in rows})
    def test_no_leak_control(self):
        rows={'control_no_cookie':{'path':'/direct','cookie':'sid=leak','marker':None}}
        self.assertFalse(oracle.classify(rows)['control_no_cookie'])
    def test_distinct_ast(self):
        source=Path(oracle.__file__).read_text()
        nodes={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
        self.assertNotEqual(nodes['public_cases'],nodes['heldout_cases'])
        self.assertNotEqual(nodes['public_async_case'],nodes['heldout_async_case'])
    def test_missing_row_fails(self):
        self.assertFalse(any(oracle.classify({}).values()))

if __name__=='__main__':unittest.main()
