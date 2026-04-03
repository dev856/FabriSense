"""Shared helpers for display formatting and asset loading."""

from __future__ import annotations

import csv
import io
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


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


ANALYSIS_ENGINE_LABELS = {
    "ai": "AI-generated",
    "heuristic": "Local heuristics",
    "local": "Local heuristics",
    "trained": "Locally trained model",
}


def get_random_fun_fact() -> str:
    return random.choice(FABRIC_FUN_FACTS)


def analysis_engine_label(mode: str | None) -> str:
    return ANALYSIS_ENGINE_LABELS.get(mode or "", "Unknown engine")


def model_prediction_margin(prediction: Dict[str, Any]) -> float:
    top_predictions = prediction.get("top_predictions", []) or []
    if len(top_predictions) < 2:
        return 0.0
    first = float(top_predictions[0].get("confidence", 0) or 0)
    second = float(top_predictions[1].get("confidence", 0) or 0)
    return round(max(0.0, first - second), 4)


def model_prediction_warnings(prediction: Dict[str, Any]) -> list[str]:
    confidence = float(prediction.get("confidence", 0) or 0)
    margin = model_prediction_margin(prediction)
    warnings = []

    if confidence < 0.55:
        warnings.append("Low confidence prediction. This image should be reviewed manually before using the label as evidence.")
    elif confidence < 0.8:
        warnings.append("Moderate confidence prediction. Treat this as directional rather than final ground truth.")

    if margin and margin < 0.15:
        warnings.append("Top predictions are close together, which suggests class ambiguity in this image.")

    if not warnings:
        warnings.append("Prediction confidence and ranking look stable for this checkpoint.")
    return warnings


def classification_report_rows(metrics: Dict[str, Any]) -> list[Dict[str, Any]]:
    report = metrics.get("classification_report", {}) or {}
    rows = []
    for label, values in report.items():
        if label in {"accuracy", "macro avg", "weighted avg"}:
            continue
        if not isinstance(values, dict):
            continue
        rows.append(
            {
                "label": label,
                "precision": round(float(values.get("precision", 0) or 0), 3),
                "recall": round(float(values.get("recall", 0) or 0), 3),
                "f1_score": round(float(values.get("f1-score", 0) or 0), 3),
                "support": int(values.get("support", 0) or 0),
            }
        )
    return rows


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


def summarize_analysis(analysis: Dict[str, Any], image_name: str) -> Dict[str, Any]:
    llm = analysis.get("llm_analysis", {})
    metadata = analysis.get("analysis_metadata", {})
    dominant = analysis.get("color_palette", {}).get("dominant_color", {}) or {}
    season_block = llm.get("season_recommendation", {})
    prediction = llm.get("model_prediction", {}) or {}

    mode = metadata.get("analysis_mode", "unknown")
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "image_name": image_name,
        "mode": mode,
        "engine": analysis_engine_label(mode),
        "fabric": llm.get("fabric_type", {}).get("primary", "N/A"),
        "pattern": llm.get("pattern", {}).get("type", "N/A"),
        "texture": llm.get("texture", {}).get("primary", "N/A"),
        "weight": llm.get("texture", {}).get("weight", "N/A"),
        "dominant_color": dominant.get("name", "N/A"),
        "quality_score": float(llm.get("quality_assessment", {}).get("score", 0) or 0),
        "price_tier": llm.get("price_range", {}).get("category", "N/A"),
        "best_seasons": ", ".join(season_block.get("best_seasons", []) or []),
        "predicted_label": prediction.get("label", ""),
        "model_name": prediction.get("model_name", ""),
        "model_architecture": prediction.get("architecture", ""),
        "prediction_confidence": round(float(prediction.get("confidence", 0) or 0), 4) if prediction else 0.0,
        "prediction_margin": model_prediction_margin(prediction) if prediction else 0.0,
        "review_flag": "Needs review" if prediction and any(
            "review" in item.lower() or "ambiguity" in item.lower()
            for item in model_prediction_warnings(prediction)
        ) else "",
        "summary": llm.get("overall_summary", "N/A"),
    }


def analyses_to_csv(rows: Iterable[Dict[str, Any]]) -> bytes:
    rows_list = list(rows)
    if not rows_list:
        return b""
    fieldnames = list(rows_list[0].keys())
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows_list)
    return buffer.getvalue().encode("utf-8")


def history_entry_from_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
    return dict(summary)


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
