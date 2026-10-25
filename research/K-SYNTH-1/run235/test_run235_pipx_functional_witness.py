import pathlib
import unittest

from run235_pipx_functional_witness import check


class Tests(unittest.TestCase):
    def test_actual_pipx_model_edit_does_not_fix_reported_path(self):
        root = pathlib.Path(__file__).parent/'repo4'
        if not root.exists():
            self.skipTest('original Run234 artifact unavailable locally')
        result = check(root)
        self.assertTrue(result['behavior_unchanged'])
        self.assertFalse(result['python_name_normalized'])
        self.assertEqual(result['model_edit']['python3.11']['argv'][1], '-python3.11')
        self.assertEqual(result['model_edit']['3.11']['argv'][1], '-3.11')


if __name__ == '__main__':
    unittest.main()
