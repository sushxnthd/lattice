# K-SYNTH-1 Run338 candidate lock — Rich PR3180 (prospective, before reference diff inspection)

Date: 2026-10-29 UTC. Candidate repository `Textualize/rich`, merged PR [#3180](https://github.com/Textualize/rich/pull/3180), pre-fix issue [#3176](https://github.com/Textualize/rich/issues/3176). This lock is a *candidate*, not a qualified fourth repair.

Historical base commit: `e76f3c3ea78481342e21a7b3328075462ab69c2b`. Historical PR head: `05c5dfc8fcbb1c967490540cc080c3d534a91a12`. Pinned baseline Git blob SHA-1: `rich/_wrap.py` = `c45f193f74ad7385c84f3b935663198415cfaa4b`; `rich/cells.py` = `9354f9e3140999702ec8c140636c511d71c340b2`. PR metadata lists both production files and tests, but **no reference patch was inspected before this lock**.

Original issue: Japanese/Chinese text disappears when wrapping. Original public repros: `アプリケーションは1670万色を使用でき` at console width 20; `TextualはPythonの高速アプリケーション開発フレームワークです` at width 20. Preserve the entire input string when rendered lines are concatenated, allowing only line-break insertion.

Prospectively specified oracle strata, to implement and SHA-freeze before reading reference changes:
- Public targets: the two exact issue repros at width 20.
- Heldout targets: `東京大阪京都123456789` at widths 6, 8, 10; `AB日本語CD東京EF` at widths 5, 7, 9; `漢字123ABC仮名456` at widths 4, 6, 8. All must preserve characters, in order, and satisfy each line's display-cell width <= the configured width (except any documented unsupported case, which must be excluded *before* outcome inspection).
- Nonregression controls: ASCII `hello world` at widths 5, 10, 20; `abc 123 def` at widths 5, 8, 12; CJK `日本語` at widths 6, 8; empty string at width 5. Controls must preserve content and avoid exceptions; width constraints apply.
- 2×2 source ablation: base/base, ref-wrap/base-cells, base-wrap/ref-cells, ref/ref. The baseline must fail at least one target; the complete reference must pass every target and control; **each single-component variant must fail at least one target or control**. A module-import error is a failure category, not a functional observation. If any criterion fails, record NOT QUALIFIED, with no retuning or promotion.
- Use original baseline files, pinned source blob identities, isolated interpreter, and independent read-only auditor. No model inference until qualification; no reference-derived localization, no retroactive oracle modification.
- One K-SYNTH-1 kernel, one OPEN/DRAFT/UNMERGED PR #9 on `research/exp003-context-order`; all 89 reserved boundary issues SEALED.
