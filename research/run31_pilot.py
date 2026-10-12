"""Free-cloud four-arm model feasibility pilot; not a final held-out evaluation.

No model-generated Python is executed. Published itsdangerous 2.2.0 excerpt.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import platform
import sys
import time
import urllib.request
from pathlib import Path

ARMS = 'ABCD'
SEED = 271828
MAX_OUTPUT_TOKENS = 512
MODEL_ID = 'Qwen2.5-Coder-7B-Instruct-GGUF-Q4_K_M'
SOURCE = '''import struct
_int64_struct = struct.Struct(">Q")
_int_to_bytes = _int64_struct.pack
_bytes_to_int = _int64_struct.unpack

def int_to_bytes(num: int) -> bytes:
    return _int_to_bytes(num).lstrip(b"\\x00")

def bytes_to_int(bytestr: bytes) -> int:
    return _bytes_to_int(bytestr.rjust(8, b"\\x00"))[0]
'''
INSTRUCTION = ('Extend int_to_bytes to arbitrary nonnegative integers while '
               'preserving existing <=64-bit outputs; negative inputs must raise '
               'ValueError. Keep bytes_to_int and all unrelated behavior unchanged.')
COMMON = {'package': 'itsdangerous', 'version': '2.2.0', 'file': 'encoding.py',
          'source_excerpt': SOURCE, 'instruction': INSTRUCTION,
          'editable': ['int_to_bytes'], 'protected': ['bytes_to_int'],
          'scope': 'one public-package source excerpt; no hidden tests'}
CONTRACTS = {
    'A': 'Return only a unified diff against encoding.py. No markdown.',
    'B': 'Return only JSON: {"interface":"python","symbol":"int_to_bytes","replacement":"def int_to_bytes(...): ..."}. No markdown.',
    'C': 'Return only JSON: {"interface":"lattice","scope":{"symbol":"int_to_bytes"},"change":{"source":"def int_to_bytes(...): ..."}}. No markdown.',
    'D': 'Return only JSON as in B. Executable invariants: for n in [0,1,255,256,2**64-1], old and new output equal; n=2**64 must encode; n=-1 raises ValueError. No markdown.',
}

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def make_prompts():
    return {a: ('You are editing an existing Python package. Respect the protected code.\n'
                + canonical(COMMON).decode() + '\n' + CONTRACTS[a]) for a in ARMS}

def run(out: Path, endpoint: str | None = None):
    if endpoint is not None and endpoint != 'http://127.0.0.1:8080/v1/chat/completions':
        raise ValueError('inference restricted to explicit loopback endpoint')
    if out.exists():
        raise ValueError('output already exists: never overwrite evidence')
    out.mkdir(parents=True)
    prompts = make_prompts()
    freeze = {'status': 'FROZEN_PILOT_NOT_FINAL_EVALUATION',
              'model': MODEL_ID, 'seed': SEED, 'temperature': 0.0, 'top_p': 1.0,
              'max_tokens': MAX_OUTPUT_TOKENS,
              'common_sha256': sha(canonical(COMMON)),
              'prompts_sha256': {a: sha(prompts[a].encode()) for a in ARMS},
              'python': sys.version, 'platform': platform.platform(),
              'model_weight_hashes': os.environ.get('LATTICE_MODEL_SHA256', 'NOT_ATTESTED'),
              'llama_commit': os.environ.get('LATTICE_LLAMA_COMMIT', 'NOT_ATTESTED')}
    (out / 'freeze.json').write_bytes(canonical(freeze) + b'\n')
    (out / 'prompts.json').write_bytes(canonical(prompts) + b'\n')
    rows = []
    for arm in ARMS:
        row = {'arm': arm, 'prompt_sha256': sha(prompts[arm].encode()),
               'status': 'PROMPT_ONLY_NOT_INFERENCE'}
        if endpoint:
            request = {'model': MODEL_ID, 'messages': [{'role': 'user', 'content': prompts[arm]}],
                       'temperature': 0.0, 'top_p': 1.0, 'seed': SEED,
                       'max_tokens': MAX_OUTPUT_TOKENS, 'stream': False}
            body = canonical(request)
            req = urllib.request.Request(endpoint, data=body, method='POST',
                                         headers={'Content-Type': 'application/json'})
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    raise RuntimeError('model endpoint redirected')
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
            started = time.monotonic()
            with opener.open(req, timeout=1200) as response:
                if response.status != 200:
                    raise RuntimeError('model server HTTP ' + str(response.status))
                raw = response.read(3_000_001)
            if len(raw) > 3_000_000:
                raise RuntimeError('oversized response')
            decoded = json.loads(raw)
            usage = decoded.get('usage')
            if (not isinstance(usage, dict) or
                not all(type(usage.get(k)) is int for k in ('prompt_tokens', 'completion_tokens'))):
                raise RuntimeError('model usage unavailable')
            (out / (arm + '_request.json')).write_bytes(body + b'\n')
            (out / (arm + '_response.json')).write_bytes(raw)
            row.update(status='MODEL_RESPONSE_NOT_HIDDEN_SCORED',
                       request_sha256=sha(body), response_sha256=sha(raw),
                       prompt_tokens=usage['prompt_tokens'],
                       completion_tokens=usage['completion_tokens'],
                       wall_seconds=round(time.monotonic() - started, 3))
        rows.append(row)
    result = {'status': 'MODEL_INFERENCE_PILOT_UNSCORED' if endpoint else 'DRY_RUN_NO_MODEL',
              'rows': rows, 'freeze_sha256': sha((out / 'freeze.json').read_bytes()),
              'no_hidden_tests': True, 'no_generated_code_executed': True}
    (out / 'result.json').write_bytes(canonical(result) + b'\n')
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--endpoint', default=None)
    args = parser.parse_args()
    print(json.dumps(run(args.output, args.endpoint), indent=2))

if __name__ == '__main__':
    main()
