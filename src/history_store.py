"""Lightweight local persistence for FabriSense analysis history."""

from __future__ import annotations

import json
import os
import tempfile
import threading
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_HISTORY_PATH = Path("data/analysis_history.json")
_HISTORY_LOCK = threading.Lock()


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
        with _HISTORY_LOCK:
            history = self.load()
            history.insert(0, entry)
            self._write(history[:200])

    def clear(self) -> None:
        with _HISTORY_LOCK:
            self._write([])

    def _write(self, history: List[Dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=self.path.parent,
            prefix=f"{self.path.stem}-",
            suffix=".tmp",
        )
        try:
            with handle:
                json.dump(history, handle, indent=2)
            os.replace(handle.name, self.path)
        finally:
            if os.path.exists(handle.name):
                os.remove(handle.name)
