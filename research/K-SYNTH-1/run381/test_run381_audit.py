import copy,io,json,sys,unittest,zipfile,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
import run381_independent_audit as a
B='/mnt/data/run381_original_baseline.zip'
F='/mnt/data/run381_original_factorial.zip'

class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b,_=a.readzip(B,a.BASE_ZIP_SHA)
        cls.f,_=a.readzip(F)
    def test_real_originals(self):
        self.assertEqual(len(a.audit_baseline_members(self.b)),12)
        self.assertEqual(a.audit_factorial_members(self.f)['aggregate_interaction'],1)
    def reject(self,fn):
        with self.assertRaises((AssertionError,KeyError,ValueError,TypeError)):
            fn()
    def test_tampered_baseline_sha(self):
        b=dict(self.b);s=json.loads(b['baseline_summary.json']);s['raw_sha256']='0'*64;b['baseline_summary.json']=json.dumps(s).encode()
        self.reject(lambda:a.audit_baseline_members(b))
    def test_duplicate_baseline_case(self):
        b=dict(self.b);r=json.loads(b['baseline_raw.json']);r['observations'][1]['case']=r['observations'][0]['case'];b['baseline_raw.json']=json.dumps(r).encode()
        self.reject(lambda:a.validate_records(r['observations']))
    def test_wrong_role(self):
        r=json.loads(self.b['baseline_raw.json']);r['observations'][0]['role']='control'
        self.reject(lambda:a.validate_records(r['observations']))
    def test_tampered_trace(self):
        r=json.loads(self.b['baseline_raw.json']);r['observations'][0]['trace']['status']=500
        self.reject(lambda:a.validate_records(r['observations']))
    def test_tampered_verdict(self):
        r=json.loads(self.b['baseline_raw.json']);r['observations'][0]['pass']=True
        self.reject(lambda:a.validate_records(r['observations']))
    def test_missing_case(self):
        r=json.loads(self.b['baseline_raw.json']);r['observations'].pop()
        self.reject(lambda:a.validate_records(r['observations']))
    def test_wrong_reference(self):
        f=dict(self.f);s=json.loads(f['summary.json']);s['reference']='0'*40;f['summary.json']=json.dumps(s).encode()
        self.reject(lambda:a.audit_factorial_members(f))
    def test_tampered_factorial_arm(self):
        f=dict(self.f);s=json.loads(f['summary.json']);s['arms']['full']['target_pass']=3;f['summary.json']=json.dumps(s).encode()
        self.reject(lambda:a.audit_factorial_members(f))
    def test_missing_factorial_arm(self):
        f=dict(self.f);s=json.loads(f['summary.json']);del s['arms']['async_only'];f['summary.json']=json.dumps(s).encode()
        self.reject(lambda:a.audit_factorial_members(f))
    def test_zip_sha_mismatch(self):
        self.reject(lambda:a.readzip(B,'0'*64))
    def test_zip_duplicate_member(self):
        bio=io.BytesIO()
        with zipfile.ZipFile(bio,'w') as z:
            z.writestr('duplicate','one');z.writestr('duplicate','two')
        p=pathlib.Path('/mnt/data/lattice_run381/test_duplicate.zip');p.write_bytes(bio.getvalue())
        try:self.reject(lambda:a.readzip(p))
        finally:p.unlink()

if __name__=='__main__':unittest.main(verbosity=2)
