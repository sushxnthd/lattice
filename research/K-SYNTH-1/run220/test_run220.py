"""Run220 prospective design checks; no model calls."""
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import run220
import run217_matched_pilot as old
import paired_repo_pilot as prior
from repo_transaction import digest

class Run220Design(unittest.TestCase):
    def setUp(self):
        self.cohort=json.loads(pathlib.Path("cohort.json").read_text())
    def test_frozen_cohort(self):
        self.assertEqual(tuple(x["instance_id"] for x in self.cohort),run220.COHORT_IDS)
        self.assertEqual(len({x["repo"] for x in self.cohort}),8)
        self.assertTrue(all(x["split"]=="discovery" for x in self.cohort))
        self.assertEqual(digest(pathlib.Path("cohort.json").read_bytes()),run220.COHORT_SHA)
    def test_matched_schema_and_information(self):
        issue=self.cohort[0]
        target={"target_id":"1"*24,"kind":"FunctionDef","name":"scan_local",
                "start_line":1,"end_line":2,"old_text":"def scan_local():\n    pass\n"}
        facts={"guarddog/scanners/scanner.py":{
            "file_sha256":"0"*64,"full_source_bytes":27,
            "targets":[target],"source_excerpt":"1: def scan_local():\n"}}
        self.assertEqual(json.loads(json.dumps(facts)),old.parse_python_view(old.python_view(facts)))
        for arm in run220.ARMS:
            prompt=run220.prompt(issue,facts,arm)
            self.assertIn(issue["problem_statement"],prompt)
            self.assertIn("target_id",prompt)
        self.assertEqual(set(prior.response_format("python_short_id")["json_schema"]["schema"]["properties"]),{"actions"})
    def test_seed_per_issue_and_freeze(self):
        seeds=[int(digest((run220.PROTOCOL+x["instance_id"]).encode())[:8],16) for x in self.cohort]
        self.assertEqual(len(set(seeds)),8)
        with tempfile.TemporaryDirectory() as tmp:
            for i in range(8):
                with patch("sys.argv",["run220.py","--cohort","cohort.json","--out",tmp+"/t"+str(i),
                                       "--task-index",str(i),"--freeze-only"]):
                    run220.main()
                record=json.loads((pathlib.Path(tmp)/("t"+str(i))/"freeze.json").read_text())
                self.assertEqual(record["issue"],self.cohort[i]["instance_id"])
                self.assertEqual(record["cohort_sha256"],run220.COHORT_SHA)
                self.assertIn("NOT YET EVALUATED",record["primary"])
    def test_boundary_excluded(self):
        self.assertNotIn("boundary",set(x["split"] for x in self.cohort))
if __name__=="__main__":unittest.main()
