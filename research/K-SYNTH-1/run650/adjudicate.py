"""Fail-closed Run650 candidate-only adjudication. Requires independent upstream verification."""
import json
from verify import verify
BASE="2adaad1ab68312fa46efb07ff072b15b720e2444"
HEAD="1e15a0322ff951e4bdcb7a74ee6c5c99d584caa1"
KEYS=("plain_initial","plain_changed","client_initial","client_changed")
EXPECTED={"plain_initial":{"value":"alpha"},"plain_changed":{"value":"beta"},"client_initial":{"value":"alpha"},"client_changed":{"value":"beta"}}
def adjudicate(transcript,repo,oracle_sha):
    status=verify(transcript,repo,BASE,HEAD,oracle_sha)
    if status!="STRUCTURALLY_VERIFIED_NOT_QUALIFIED":return {"status":"UNKNOWN","reason":status}
    arms={k:json.loads(v["observation"]["stdout"]) for k,v in transcript["arms"].items()}
    outcomes={arm:{key:(obs[key]==EXPECTED[key]) for key in KEYS} for arm,obs in arms.items()}
    candidate=(all(outcomes["full"].values()) and not all(outcomes["base"].values())
               and not all(outcomes["parent"].values()) and not all(outcomes["subclass"].values()))
    return {"status":"CANDIDATE_ONLY" if candidate else "NOT_QUALIFIED","outcomes":outcomes,
            "warning":"No independent heldout/nonregression oracle; never promote candidate to qualified."}
