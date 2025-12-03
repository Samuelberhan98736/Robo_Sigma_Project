"""
utils.py
Generic helper functions.
"""

import json
from datetime import datetime
from pathlib import Path


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def load_json(path: str | Path):
    with open(path) as f:
        return json.load(f)
