"""All fixtures are synthetic unit tests, never model evidence."""
import unittest

import importlib.util
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'research' / 'run29' / 'independent_paired_checker.py'
spec = importlib.util.spec_from_file_location('lattice_run29_checker', MODULE)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
EvidenceError, analyze, _parse_line = checker.EvidenceError, checker.analyze, checker._parse_line

H = 'a' * 64


def sample(repos=('repo1', 'repo2', 'repo3'), seeds=(1, 2)):
    rows = []
    for i, repo in enumerate(repos):
        for seed in seeds:
            for arm in 'ABCD':
                success = (arm == 'C' and i != 2) or (arm == 'B' and i == 2)
                rows.append({
                    'task_id': 'task' + str(i), 'repository_id': repo, 'model_id': 'test-model',
                    'model_revision': H, 'seed': seed, 'arm': arm,
                    'feature_complete': success, 'hidden_tests_passed': success,
                    'perfect_repository': success, 'regressions': 0, 'forbidden_changes': 0,
                    'invalid_transitions': 0, 'permission_violations': 0,
                    'prompt_tokens': 100, 'completion_tokens': 20, 'repair_iterations': 0,
                    'wall_seconds': 1.0, 'transcript_sha256': H, 'candidate_sha256': H,
                    'evaluator_sha256': H, 'task_manifest_sha256': H,
                })
    return rows


class TestIndependentChecker(unittest.TestCase):
    def test_synthetic_clustered_results(self):
        out = analyze(sample(), bootstrap_replicates=500)
        self.assertEqual(out['n_repository_clusters'], 3)
        self.assertEqual(out['n_complete_four_arm_groups'], 6)
        self.assertAlmostEqual(out['C_minus_B_cluster_mean'], 1/3)
        self.assertEqual(out['bc_token_parity'], 'PASS')
        self.assertEqual(out['exact_two_sided_cluster_sign_test']['p_two_sided'], 1.0)
        self.assertEqual(out['arms']['C']['perfect_repository_count'], 4)
        self.assertEqual(out['evidence_claim_gate'][:7], 'BLOCKED')

    def test_single_repo_no_false_precision(self):
        out = analyze(sample(repos=('only',), seeds=tuple(range(50))), bootstrap_replicates=100)
        self.assertIsNone(out['bootstrap_95_percent_CI'])
        self.assertEqual(out['n_repository_clusters'], 1)

    def test_missing_arm_rejected(self):
        with self.assertRaises(EvidenceError):
            analyze(sample()[:-1])

    def test_duplicate_arm_rejected(self):
        x = sample()
        with self.assertRaises(EvidenceError):
            analyze(x + [x[0]])

    def test_inconsistent_success_rejected(self):
        x = sample()
        x[0]['perfect_repository'] = True
        with self.assertRaises(EvidenceError):
            analyze(x)

    def test_mismatched_manifest_rejected(self):
        x = sample()
        x[0]['task_manifest_sha256'] = 'b' * 64
        with self.assertRaises(EvidenceError):
            analyze(x)

    def test_token_imbalance_blocks_parity(self):
        x = sample()
        x[1]['prompt_tokens'] = 1000
        out = analyze(x, bootstrap_replicates=100)
        self.assertEqual(out['bc_token_parity'], 'FAIL')

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(EvidenceError):
            _parse_line('{"arm":"A","arm":"C"}')

    def test_nonfinite_json_rejected(self):
        with self.assertRaises(EvidenceError):
            _parse_line('{"x":NaN}')

    def test_seed_not_pseudoreplicated(self):
        a = analyze(sample(seeds=(1,)), bootstrap_replicates=100)
        b = analyze(sample(seeds=tuple(range(50))), bootstrap_replicates=100)
        self.assertEqual(a['n_repository_clusters'], b['n_repository_clusters'])
        self.assertEqual(a['C_minus_B_cluster_mean'], b['C_minus_B_cluster_mean'])


if __name__ == '__main__':
    unittest.main()
