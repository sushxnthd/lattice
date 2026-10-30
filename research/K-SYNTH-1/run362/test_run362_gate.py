import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from run362_independent_gate import verify,EvidenceError,EXPECTED_GIT_BLOBS,TARGETS,CONTROLS,VARIANTS

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        cases=list(TARGETS)+list(CONTROLS)
        for v in VARIANTS:
            rows=[{'name':name,'kind':'target' if i<6 else 'control',
                   'passed':True,'error':None} for i,name in enumerate(cases)]
            (self.root/(v+'.json')).write_text(json.dumps({'schema':'lattice.run362.anyio.v1',
                'python':'3.11.9','anyio_path':'/src/anyio/__init__.py','outcomes':rows}))
        source=[{'side':s,'path':p,'git_blob':sha} for (s,p),sha in EXPECTED_GIT_BLOBS.items()]
        (self.root/'source_verification.json').write_text(json.dumps(source))
        (self.root/'pip_freeze.txt').write_text('idna==3.7\nsniffio==1.3.1\n')
        (self.root/'image_digest.txt').write_text('sha256:test\n')
        self.refresh()
    def tearDown(self):self.tmp.cleanup()
    def refresh(self):
        rows={v:json.loads((self.root/(v+'.json')).read_text())['outcomes'] for v in VARIANTS}
        counts={v:{k:sum(x['passed'] for x in rows[v] if x['kind']==k) for k in ('target','control')} for v in VARIANTS}
        interactions={rows['base'][i]['name']:int(rows['full'][i]['passed'])-int(rows['backend_only'][i]['passed'])-int(rows['memory_only'][i]['passed'])+int(rows['base'][i]['passed']) for i in range(12)}
        qualified=(counts['full']=={'target':6,'control':6} and counts['base']['target']<6 and counts['base']['control']==6 and all(counts[v]['target']<6 or counts[v]['control']<6 for v in ('backend_only','memory_only')) and any(rows['backend_only'][i]['passed']!=rows['memory_only'][i]['passed'] for i in range(12)))
        (self.root/'qualification_summary.json').write_text(json.dumps({'counts':counts,'qualified':qualified,'interactions':interactions,'case_count':12}))
        manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.iterdir() if p.is_file() and p.name!='sha256_manifest.json'}
        (self.root/'sha256_manifest.json').write_text(json.dumps(manifest))
    def rehash(self):
        manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.iterdir() if p.is_file() and p.name!='sha256_manifest.json'}
        (self.root/'sha256_manifest.json').write_text(json.dumps(manifest))
    def mutate(self,file,fn,refresh=True):
        p=self.root/file;v=json.loads(p.read_text());fn(v);p.write_text(json.dumps(v))
        if refresh:self.refresh()
        else:self.rehash()
    def test_valid_fixture(self):self.assertFalse(verify(self.root)['qualified'])
    def test_detect_hash_corruption(self):
        (self.root/'base.json').write_text('{}')
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_detect_rehashed_wrong_source(self):
        self.mutate('source_verification.json',lambda a:a[0].update(git_blob='0'*40))
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_detect_duplicate_source(self):
        self.mutate('source_verification.json',lambda a:a[0].update(side='head'))
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_detect_wrong_package(self):
        self.mutate('base.json',lambda a:a.update(anyio_path='/usr/local/lib/python3.11/site-packages/anyio/__init__.py'))
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_detect_wrong_python(self):
        self.mutate('base.json',lambda a:a.update(python='3.13.5'))
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_detect_case_reorder(self):
        self.mutate('base.json',lambda a:a['outcomes'].reverse())
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_detect_case_omission(self):
        self.mutate('base.json',lambda a:a['outcomes'].pop(),refresh=False)
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_detect_bad_kind(self):
        self.mutate('base.json',lambda a:a['outcomes'][0].update(kind='control'))
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_detect_status_error_disagreement(self):
        self.mutate('base.json',lambda a:a['outcomes'][0].update(error='AssertionError'))
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_detect_forged_summary(self):
        self.mutate('qualification_summary.json',lambda a:a.update(qualified=True),refresh=False)
        with self.assertRaises(EvidenceError):verify(self.root)
    def test_qualified_fixture(self):
        def fail_at(a,i):a['outcomes'][i].update(passed=False,error='AssertionError: expected')
        self.mutate('base.json',lambda a:fail_at(a,0))
        self.mutate('backend_only.json',lambda a:fail_at(a,0))
        self.mutate('memory_only.json',lambda a:fail_at(a,1))
        self.assertTrue(verify(self.root)['qualified'])
    def test_no_distinct_partial_fails(self):
        def fail_at(a):a['outcomes'][0].update(passed=False,error='AssertionError: expected')
        for v in ('base','backend_only','memory_only'):
            self.mutate(v+'.json',fail_at)
        self.assertFalse(verify(self.root)['qualified'])

if __name__=='__main__':unittest.main()
