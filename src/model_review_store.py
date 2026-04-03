"""Persistence for human review records on trained-model predictions."""

from __future__ import annotations

import json
import os
import tempfile
import threading
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_MODEL_REVIEW_PATH = Path("data/model_reviews.json")
_MODEL_REVIEW_LOCK = threading.Lock()


class ModelReviewStore:
    def __init__(self, path: Path | str = DEFAULT_MODEL_REVIEW_PATH):
        self.path = Path(path)

    def load(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

    def append(self, entry: Dict[str, Any]) -> None:
        with _MODEL_REVIEW_LOCK:
            reviews = self.load()
            reviews.insert(0, entry)
            self._write(reviews[:500])

    def clear(self) -> None:
        with _MODEL_REVIEW_LOCK:
            self._write([])

    def _write(self, reviews: List[Dict[str, Any]]) -> None:
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
                json.dump(reviews, handle, indent=2)
            os.replace(handle.name, self.path)
        finally:
            if os.path.exists(handle.name):
                os.remove(handle.name)
