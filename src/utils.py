"""Shared helpers for display formatting and asset loading."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Dict, Optional


FABRIC_FUN_FACTS = [
    "Silk production started in ancient China thousands of years ago.",
    "Denim gets its name from 'serge de Nimes' in France.",
    "Linen is made from flax and is stronger than cotton.",
    "Wool can hold moisture without feeling wet to the touch.",
    "Egyptian cotton is known for extra-long staple fibers.",
    "Velvet was once considered a luxury textile reserved for royalty.",
    "Lyocell is produced from wood pulp using a closed-loop process.",
    "Cashmere fibers are finer and warmer than standard sheep wool.",
]


def get_random_fun_fact() -> str:
    return random.choice(FABRIC_FUN_FACTS)


def load_json_asset(path: str | Path) -> Optional[Dict[str, Any]]:
    asset_path = Path(path)
    if not asset_path.exists():
        return None
    try:
        return json.loads(asset_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def format_analysis_for_display(analysis: Dict[str, Any]) -> Dict[str, Any]:
    llm = analysis.get("llm_analysis", {})
    quality = llm.get("quality_assessment", {})
    season_block = llm.get("season_recommendation", {})
    price = llm.get("price_range", {})
    sustainability = llm.get("sustainability", {})

    score = float(quality.get("score", 0) or 0)
    stars = "*" * max(1, min(5, round(score / 2))) if score else "Not rated"
    seasons = ", ".join(season_block.get("best_seasons", []) or ["Not specified"])

    return {
        "score": score,
        "stars": stars,
        "seasons": seasons,
        "price_category": price.get("category", "N/A"),
        "eco_score": sustainability.get("eco_score", "N/A"),
    }
