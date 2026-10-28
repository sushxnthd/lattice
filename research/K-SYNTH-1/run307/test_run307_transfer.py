import json,pathlib,unittest
from run307_versioned_transfer import classify

R=pathlib.Path(__file__).resolve().parent
C=json.loads((R/'RUN307_FROZEN_SOURCES.json').read_text())['cases']

class TransferTests(unittest.TestCase):
 def test_unsupported_version_is_unknown(self):
  r=classify(C[0]['source'],'3.15')
  self.assertEqual(r['status'],'UNSUPPORTED_RUNTIME_UNKNOWN')
  self.assertEqual(r['final_len'],'UNKNOWN')
 def test_313_eager(self):
  for c in C:
   f=classify(c['source'],'3.13')
   self.assertEqual(f['status'],'BOUNDED')
   self.assertEqual(f['mode'],'STRINGIFIED' if c['future'] else 'EAGER')
   self.assertEqual(f['final_len'],'NOT_KNOWN_TARGET' if c['future'] else 'UNKNOWN_DYNAMIC')
   n=sum(x['event']=='UNKNOWN_ANNOTATION_EFFECT' for x in f['events'])
   self.assertEqual(n,0 if c['future'] else 1)
 def test_314_deferred_access_and_cache(self):
  for c in C:
   f=classify(c['source'],'3.14')
   self.assertEqual(f['status'],'BOUNDED')
   n=sum(x['event']=='UNKNOWN_ANNOTATION_EFFECT' for x in f['events'])
   expected=not c['future'] and c['access']!='none'
   self.assertEqual(n,int(expected))
   self.assertEqual(f['final_len'],'UNKNOWN_DYNAMIC' if expected else 'NOT_KNOWN_TARGET')
   reads=sum(x['event']=='ANNOTATION_READ' for x in f['events'])
   self.assertEqual(reads,2 if c['access']=='repeat' else 0 if c['access']=='none' else 1)
 def test_source_hashes_unique(self):
  self.assertEqual(len({c['source_sha256'] for c in C}),256)

if __name__=='__main__':unittest.main()
