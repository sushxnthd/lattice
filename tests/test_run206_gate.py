"""Expose Run206's representation-independent safety tests to repository CI."""
import sys
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[1] / "research" / "K-SYNTH-1" / "run206"
sys.path.insert(0, str(RESEARCH))
from test_safety_gate import GateTests

class TestRun206SafetyGate(GateTests):
    pass
