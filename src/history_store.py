"""Lightweight local persistence for FabriSense analysis history."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_HISTORY_PATH = Path("data/analysis_history.json")


class HistoryStore:
    def __init__(self, path: Path | str = DEFAULT_HISTORY_PATH):
        self.path = Path(path)

    def load(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

    def append(self, entry: Dict[str, Any]) -> None:
        history = self.load()
        history.insert(0, entry)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(history[:200], indent=2), encoding="utf-8")

    def clear(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("[]", encoding="utf-8")