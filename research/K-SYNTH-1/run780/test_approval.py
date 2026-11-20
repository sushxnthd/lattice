import hashlib, unittest
from approval import sign, verify
KEY=b'publisher-independent-test-secret-32bytes!'
COMMIT='a'*40
TAG='v0.1.0a1'
WHEEL=b'approved wheel fixture'
P={'schema':'lattice-alpha-approval-v1','repository':'sushxnthd/lattice','source_commit':COMMIT,'artifact_sha256':hashlib.sha256(WHEEL).hexdigest(),'release_tag':TAG}
class Checks(unittest.TestCase):
 def test_valid(self): self.assertTrue(verify(P,sign(P,KEY),KEY,WHEEL,COMMIT,TAG))
 def test_changed_wheel(self): self.assertFalse(verify(P,sign(P,KEY),KEY,WHEEL+b'x',COMMIT,TAG))
 def test_producer_digest_substitution(self):
  p=dict(P,artifact_sha256=hashlib.sha256(WHEEL+b'x').hexdigest())
  self.assertFalse(verify(p,sign(P,KEY),KEY,WHEEL+b'x',COMMIT,TAG))
 def test_wrong_key(self): self.assertFalse(verify(P,sign(P,KEY),b'other-independent-secret-of-32-bytes',WHEEL,COMMIT,TAG))
 def test_replay_tag(self): self.assertFalse(verify(P,sign(P,KEY),KEY,WHEEL,COMMIT,'v0.1.0a2'))
 def test_replay_commit(self): self.assertFalse(verify(P,sign(P,KEY),KEY,WHEEL,'b'*40,TAG))
 def test_extra_field(self): self.assertFalse(verify(dict(P,debug=True),'0'*64,KEY,WHEEL,COMMIT,TAG))
 def test_missing_field(self):
  p=dict(P); del p['repository']
  self.assertFalse(verify(p,'0'*64,KEY,WHEEL,COMMIT,TAG))
 def test_malformed_signature(self): self.assertFalse(verify(P,'zz',KEY,WHEEL,COMMIT,TAG))
 def test_short_key(self): self.assertFalse(verify(P,'0'*64,b'weak',WHEEL,COMMIT,TAG))
if __name__=='__main__': unittest.main(verbosity=2)
