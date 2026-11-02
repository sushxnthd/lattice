# K-SYNTH-1 Run430 prospective issue-first freeze

## Freeze boundary
Authored before consulting fixing pull requests, historical reference diffs or later-version behavior. Primary HTTPX #911; secondary #318 and #1833, predeclared in that order. This is candidate screening, not a model trial. Never change criteria after reference exposure.

## Issue-only source
1. [HTTPX #911](https://github.com/encode/httpx/issues/911), reported 2020-04-26: AsyncClient with forward HTTP proxy returns proxy URL instead of destination; reproduction on 0.12.1.
2. [HTTPX #318](https://github.com/encode/httpx/issues/318), reported 2019-09-05: cross-origin redirect should set new Host header.
3. [HTTPX #1833](https://github.com/encode/httpx/issues/1833), reported 2021-09-03: relative join of URL with unescaped query brackets raises ResolutionError.

## Primary HTTPX #911 frozen public contract
Positive A: proxied GET to http://target.invalid/start returns response.url equal to target URL, not proxy.
Positive B: proxied 302 to http://target.invalid/next yields final URL /next and history[0].url /start.
Positive C: two target hosts sharing one proxy retain distinct response URLs.
Control D: proxy receives absolute-form request-target bytes and target Host header, with correct response body/status.
Control E: direct non-proxied HTTP request returns destination URL without unsolicited redirect.
Control F: no Proxy-Authorization sent in no-credentials configuration.
Oracle: in-process loopback forward proxy captures raw request-line bytes, Host and public response.url/history. Independent raw-socket replay checks proxy parsing; no external network.

## Secondary frozen contracts
#318: redirect origin A to B must set B Host; same-origin Host correct; old Authorization not forwarded.
#1833: URL('https://example.com/?[]').join('/') yields https://example.com/ without exception; valid query/path joins unaffected.

## Qualification and rejection
Exact immutable first-parent base/ref, >=2 changed production Python files, independent public/heldout/nonregression, base-negative/ref-positive, joint target-plus-control ablation necessity. Import-only ablation is not sufficient. Check one-file alternatives. Reject reference-policy mismatch, after-reference retuning, source import leakage and newer-release calibration. All 89 reserved issues sealed. Qualified count stays two unless all conditions verified.

## Limits
A finite oracle does not prove irreducible source cardinality. Compiler acceptance is not repair success. No IR superiority without matched functional open-model inference.