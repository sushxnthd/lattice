#!/usr/bin/env python3
"""Frozen independent black-box console oracle for Rich #3176 / PR #3180.

Created from issue text before reference patch inspection. No reference internals.
Runs in a fresh isolated process with historical Rich import path.
"""
import json, os, sys, hashlib
from rich.console import Console
from rich.cells import cell_len

CASES = [
  # issue-reported public targets
  ('target_public', 'issue_numeric', 'アプリケーションは1670万色を使用でき',20),
  ('target_public', 'issue_textual', 'TextualはPythonの高速アプリケーション開発フレームワークです',20),
  ('target_public', 'issue_numeric_narrow', 'アプリケーションは1670万色を使用でき',13),
  ('target_public', 'issue_textual_narrow', 'TextualはPythonの高速アプリケーション開発フレームワークです',16),
  # independently written heldout targets, not used in prompt or for selection
  ('target_heldout','jp_kanji', '東京都内の公共交通機関を利用してください',11),
  ('target_heldout','cn_mixed', '数据库支持Python和高并发请求处理',12),
  ('target_heldout','jp_digits', '世界中の開発者が2026年に利用する',10),
  ('target_heldout','cn_long', '编程语言的语义必须在边界条件下保持一致',9),
  # nonregression controls, ASCII and mixed CJK, all without spaces
  ('control','ascii_short','hello',20),
  ('control','ascii_fold','abcdefghij1234567890',7),
  ('control','ascii_digits','12345678901234567890',9),
  ('control','ascii_punctuation','abc-xyz_0123456789',8),
  ('control','wide_exact','漢字漢字',8),
  ('control','wide_near','漢字漢字',7),
  ('control','mixed_ascii','abc漢字def',6),
  ('control','single_cjk','あいうえお',4),
]

def run():
    records=[]
    for group,name,source,width in CASES:
        console=Console(width=width, force_terminal=False, color_system=None, highlight=False, legacy_windows=False)
        with console.capture() as capture:
            console.print(source)
        rendered=capture.get()
        lines=rendered.rstrip('\n').split('\n')
        recovered=''.join(lines)
        widths=[cell_len(s) for s in lines]
        # An explicit invariant, not a reference patch comparison.
        passed=(recovered==source and all(w<=width for w in widths))
        records.append(dict(group=group,name=name,width=width,source=source,rendered=rendered,
                            recovered=recovered,line_cell_widths=widths,passed=passed))
    report={'oracle_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),
            'python':sys.version,'rich_module':__import__('rich').__file__,
            'records':records,'summary':{g:sum(r['passed'] for r in records if r['group']==g)
                                    for g in ('target_public','target_heldout','control')}}
    print(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2))
    return 0
if __name__=='__main__':sys.exit(run())
