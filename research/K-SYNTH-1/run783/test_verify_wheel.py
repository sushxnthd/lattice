import hashlib
import pathlib
import tempfile
import unittest
from verify_wheel import verify

class TestPin(unittest.TestCase):
    def test_pin(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/'example.whl'; p.write_bytes(b'original')
            pin=hashlib.sha256(b'original').hexdigest()
            self.assertEqual(verify(p,pin),pin)
            p.write_bytes(b'replacement')
            with self.assertRaisesRegex(ValueError,'differs'): verify(p,pin)
            with self.assertRaisesRegex(ValueError,'lowercase'): verify(p,'bad')
            with self.assertRaisesRegex(ValueError,'missing'): verify(pathlib.Path(d)/'missing.whl',pin)

if __name__=='__main__': unittest.main(verbosity=2)
