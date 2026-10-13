"""Validate paired pilot files without executing them."""
from pathlib import Path

def ready(root: Path) -> bool:
    return (root / 'research/run32_paired_pilot.py').is_file()
