from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


def load_jsonl(path: str | Path) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

