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


def compare_fabric_analyses(
    analysis_a: Dict[str, Any],
    name_a: str,
    analysis_b: Dict[str, Any],
    name_b: str,
) -> Dict[str, Any]:
    llm_a = analysis_a.get("llm_analysis", {})
    llm_b = analysis_b.get("llm_analysis", {})

    fabric_a = llm_a.get("fabric_type", {}).get("primary", "Unknown")
    fabric_b = llm_b.get("fabric_type", {}).get("primary", "Unknown")
    pattern_a = llm_a.get("pattern", {}).get("type", "Unknown")
    pattern_b = llm_b.get("pattern", {}).get("type", "Unknown")
    weight_a = llm_a.get("texture", {}).get("weight", "Unknown")
    weight_b = llm_b.get("texture", {}).get("weight", "Unknown")
    quality_a = float(llm_a.get("quality_assessment", {}).get("score", 0) or 0)
    quality_b = float(llm_b.get("quality_assessment", {}).get("score", 0) or 0)
    color_a = analysis_a.get("color_palette", {}).get("dominant_color", {}) or {}
    color_b = analysis_b.get("color_palette", {}).get("dominant_color", {}) or {}
    dominant_a = color_a.get("name", "Unknown")
    dominant_b = color_b.get("name", "Unknown")
    price_a = llm_a.get("price_range", {}).get("category", "Unknown")
    price_b = llm_b.get("price_range", {}).get("category", "Unknown")

    similarities = []
    if fabric_a == fabric_b:
        similarities.append(f"Both images read as {fabric_a.lower()} fabrics.")
    if pattern_a == pattern_b:
        similarities.append(f"Both textiles share a {pattern_a.lower()} pattern direction.")
    if price_a == price_b:
        similarities.append(f"Both fall into the same estimated {price_a.lower()} price tier.")

    seasons_a = set(llm_a.get("season_recommendation", {}).get("best_seasons", []))
    seasons_b = set(llm_b.get("season_recommendation", {}).get("best_seasons", []))
    overlap = sorted(seasons_a & seasons_b)
    if overlap:
        similarities.append(f"Both are suited to {', '.join(overlap).lower()} use.")
    if not similarities:
        similarities.append("Both fabrics still support a structured visual analysis with identifiable color and texture signals.")

    differences = []
    if fabric_a != fabric_b:
        differences.append(f"{name_a} leans toward {fabric_a.lower()}, while {name_b} leans toward {fabric_b.lower()}.")
    if pattern_a != pattern_b:
        differences.append(f"Pattern direction differs: {name_a} is {pattern_a.lower()} and {name_b} is {pattern_b.lower()}.")
    if dominant_a != dominant_b:
        differences.append(f"The dominant color family shifts from {dominant_a.lower()} to {dominant_b.lower()}.")
    if weight_a != weight_b:
        differences.append(f"Fabric body differs: {name_a} reads {weight_a.lower()} and {name_b} reads {weight_b.lower()}.")
    if not differences:
        differences.append("The two fabrics are visually close, so the strongest differences are subtle rather than structural.")

    if quality_a > quality_b:
        winner = name_a
        winner_reason = f"{name_a} has the stronger visual quality score ({quality_a:.1f} vs {quality_b:.1f})."
    elif quality_b > quality_a:
        winner = name_b
        winner_reason = f"{name_b} has the stronger visual quality score ({quality_b:.1f} vs {quality_a:.1f})."
    else:
        winner = "Tie"
        winner_reason = f"Both fabrics land on the same visual quality score of {quality_a:.1f}."

    return {
        "winner": winner,
        "winner_reason": winner_reason,
        "similarities": similarities,
        "differences": differences,
        "score_a": quality_a,
        "score_b": quality_b,
        "fabric_a": fabric_a,
        "fabric_b": fabric_b,
        "pattern_a": pattern_a,
        "pattern_b": pattern_b,
        "dominant_a": dominant_a,
        "dominant_b": dominant_b,
        "price_a": price_a,
        "price_b": price_b,
    }
