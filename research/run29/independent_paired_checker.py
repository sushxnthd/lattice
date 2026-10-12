"""Independent, fail-closed analysis of four-arm Lattice coding evaluations.

This module does not run models or hidden tests, and cannot attest that supplied
outcomes are truthful. It never turns a statistical contrast into a causal claim.
Only the exact registered four-arm schema is accepted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

ARMS = ('A', 'B', 'C', 'D')
HEX = re.compile(r'[0-9a-f]{64}\Z')
FIELDS = frozenset({
    'task_id', 'repository_id', 'model_id', 'model_revision', 'seed', 'arm',
    'feature_complete', 'hidden_tests_passed', 'perfect_repository',
    'regressions', 'forbidden_changes', 'invalid_transitions',
    'permission_violations', 'prompt_tokens', 'completion_tokens',
    'repair_iterations', 'wall_seconds', 'transcript_sha256',
    'candidate_sha256', 'evaluator_sha256', 'task_manifest_sha256',
})


class EvidenceError(ValueError):
    pass


def _parse_line(s: str):
    def unique(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise EvidenceError('duplicate JSON key: ' + k)
            d[k] = v
        return d
    return json.loads(s, object_pairs_hook=unique,
                      parse_constant=lambda v: (_ for _ in ()).throw(EvidenceError('nonfinite JSON: ' + v)))


def _validate(row):
    if type(row) is not dict or set(row) != FIELDS:
        raise EvidenceError('row has missing or extra fields')
    for k in ('task_id', 'repository_id', 'model_id'):
        if type(row[k]) is not str or not re.fullmatch(r'[A-Za-z0-9_.-]{1,120}', row[k]):
            raise EvidenceError('invalid identifier ' + k)
    if row['arm'] not in ARMS or type(row['arm']) is not str:
        raise EvidenceError('invalid arm')
    if type(row['seed']) is not int or row['seed'] < 0:
        raise EvidenceError('invalid seed')
    for k in ('model_revision', 'transcript_sha256', 'candidate_sha256',
              'evaluator_sha256', 'task_manifest_sha256'):
        if type(row[k]) is not str or not HEX.fullmatch(row[k]):
            raise EvidenceError('invalid SHA256 ' + k)
    for k in ('feature_complete', 'hidden_tests_passed', 'perfect_repository'):
        if type(row[k]) is not bool:
            raise EvidenceError('invalid Boolean ' + k)
    for k in ('regressions', 'forbidden_changes', 'invalid_transitions',
              'permission_violations', 'prompt_tokens', 'completion_tokens', 'repair_iterations'):
        if type(row[k]) is not int or row[k] < 0:
            raise EvidenceError('invalid count ' + k)
    if type(row['wall_seconds']) not in (float, int) or not math.isfinite(row['wall_seconds']) or row['wall_seconds'] < 0:
        raise EvidenceError('invalid wall_seconds')
    if row['perfect_repository'] and not (
        row['feature_complete'] and row['hidden_tests_passed'] and
        all(row[k] == 0 for k in ('regressions', 'forbidden_changes',
                                 'invalid_transitions', 'permission_violations'))
    ):
        raise EvidenceError('perfect_repository inconsistent with outcome fields')


def _quantile(xs, q):
    ys = sorted(xs)
    x = (len(ys) - 1) * q
    lo, hi = math.floor(x), math.ceil(x)
    return ys[lo] * (hi - x) + ys[hi] * (x - lo) if lo != hi else ys[lo]


def _sign_test(deltas):
    positive = sum(x > 0 for x in deltas)
    negative = sum(x < 0 for x in deltas)
    n = positive + negative
    if n == 0:
        return {'positive': 0, 'negative': 0, 'ties': len(deltas), 'p_two_sided': 1.0}
    k = min(positive, negative)
    p = min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / (2 ** n))
    return {'positive': positive, 'negative': negative, 'ties': len(deltas) - n,
            'p_two_sided': p}


def analyze(rows, max_prompt_imbalance=0.10, bootstrap_replicates=5000, seed=20261012):
    if not (type(max_prompt_imbalance) in (float, int) and
            0 <= max_prompt_imbalance <= 1 and math.isfinite(max_prompt_imbalance)):
        raise EvidenceError('invalid frozen token imbalance threshold')
    if type(bootstrap_replicates) is not int or not 100 <= bootstrap_replicates <= 100000:
        raise EvidenceError('invalid bootstrap count')
    if type(rows) is not list or not rows:
        raise EvidenceError('empty evidence')
    seen = {}
    task_repos = {}
    groups = defaultdict(dict)
    for row in rows:
        _validate(row)
        key = (row['task_id'], row['model_id'], row['model_revision'], row['seed'])
        if row['task_id'] in task_repos and task_repos[row['task_id']] != row['repository_id']:
            raise EvidenceError('task changes repository identity')
        task_repos[row['task_id']] = row['repository_id']
        unique = (*key, row['arm'])
        if unique in seen:
            raise EvidenceError('duplicate task/model/seed/arm')
        seen[unique] = row
        groups[key][row['arm']] = row
    for key, arms in groups.items():
        if set(arms) != set(ARMS):
            raise EvidenceError('missing four-arm outcome: ' + str(key))
        if len({r['evaluator_sha256'] for r in arms.values()}) != 1:
            raise EvidenceError('evaluator hash differs between arms')
        if len({r['task_manifest_sha256'] for r in arms.values()}) != 1:
            raise EvidenceError('task manifest differs between arms')
    pairs = []
    for key, arms in sorted(groups.items()):
        b, c = arms['B'], arms['C']
        denom = max(b['prompt_tokens'], c['prompt_tokens'], 1)
        imbalance = abs(b['prompt_tokens'] - c['prompt_tokens']) / denom
        pairs.append({'task_id': key[0], 'repository_id': b['repository_id'],
                      'model_id': key[1], 'seed': key[3],
                      'C_minus_B': int(c['perfect_repository']) - int(b['perfect_repository']),
                      'BC_prompt_imbalance': imbalance,
                      'token_budget_matched': imbalance <= max_prompt_imbalance})
    by_repo = defaultdict(list)
    for p in pairs:
        by_repo[p['repository_id']].append(p['C_minus_B'])
    cluster_effects = {repo: sum(v) / len(v) for repo, v in sorted(by_repo.items())}
    cluster_values = list(cluster_effects.values())
    delta = sum(cluster_values) / len(cluster_values)
    ci = None
    if len(cluster_values) >= 2:
        rng = random.Random(seed)
        n = len(cluster_values)
        samples = [sum(rng.choice(cluster_values) for _ in range(n)) / n
                   for _ in range(bootstrap_replicates)]
        ci = [_quantile(samples, 0.025), _quantile(samples, 0.975)]
    arms_summary = {}
    for arm in ARMS:
        arm_rows = [r for r in rows if r['arm'] == arm]
        arms_summary[arm] = {
            'n_task_seed_model_rows': len(arm_rows),
            'perfect_repository_count': sum(r['perfect_repository'] for r in arm_rows),
            'feature_complete_count': sum(r['feature_complete'] for r in arm_rows),
            'hidden_tests_passed_count': sum(r['hidden_tests_passed'] for r in arm_rows),
            'regressions_total': sum(r['regressions'] for r in arm_rows),
            'forbidden_changes_total': sum(r['forbidden_changes'] for r in arm_rows),
            'invalid_transitions_total': sum(r['invalid_transitions'] for r in arm_rows),
            'permission_violations_total': sum(r['permission_violations'] for r in arm_rows),
            'prompt_tokens_total': sum(r['prompt_tokens'] for r in arm_rows),
            'completion_tokens_total': sum(r['completion_tokens'] for r in arm_rows),
        }
    return {
        'status': 'STATISTICAL_RECOMPUTATION_ONLY_NOT_INDEPENDENT_OUTCOME_ATTESTATION',
        'evidence_claim_gate': 'BLOCKED_UNTIL_RAW_TRANSCRIPTS_HOLDOUTS_MODEL_AND_EVALUATOR_VERIFIED',
        'primary_contrast': 'C_vs_B', 'unit_of_uncertainty': 'repository_cluster',
        'n_repository_clusters': len(cluster_values), 'n_complete_four_arm_groups': len(groups),
        'C_minus_B_cluster_mean': delta, 'bootstrap_95_percent_CI': ci,
        'bootstrap_CI_status': 'AVAILABLE' if ci is not None else 'INSUFFICIENT_REPOSITORY_CLUSTERS',
        'repository_effects': cluster_effects, 'exact_two_sided_cluster_sign_test': _sign_test(cluster_values),
        'bc_token_parity': 'PASS' if all(p['token_budget_matched'] for p in pairs) else 'FAIL',
        'max_bc_prompt_imbalance_fraction': max(p['BC_prompt_imbalance'] for p in pairs),
        'registered_imbalance_threshold': max_prompt_imbalance,
        'information_parity': 'NOT_ATTESTED_BY_THIS_CHECKER',
        'arms': arms_summary,
        'note': 'Repeated seeds and tasks within a repository are not independent clusters. CI is descriptive; not a proof of causal representation advantage.'
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('results_jsonl', type=Path)
    p.add_argument('output_json', type=Path)
    p.add_argument('--frozen-bc-token-threshold', type=float, required=True)
    args = p.parse_args(argv)
    if args.output_json.exists():
        raise EvidenceError('refuse to overwrite evidence')
    data = args.results_jsonl.read_bytes()
    rows = [_parse_line(line) for line in data.decode('utf-8').splitlines() if line.strip()]
    result = analyze(rows, max_prompt_imbalance=args.frozen_bc_token_threshold)
    result['input_sha256'] = hashlib.sha256(data).hexdigest()
    args.output_json.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'n_groups': result['n_complete_four_arm_groups'],
                      'n_clusters': result['n_repository_clusters']}))


if __name__ == '__main__':
    main()
