"""Page-level rendering for the FabriSense app."""

from __future__ import annotations

import json
from datetime import datetime
from html import escape as html_escape
from pathlib import Path
from typing import Any, Dict

import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie

from src.analyzer import FabricAnalyzer
from src.history_store import HistoryStore
from src.image_preprocessor import ImagePreprocessor
from src.model_benchmark import (
    compare_checkpoints_on_manifest,
    create_uploaded_benchmark_manifest,
    list_manifest_directories,
)
from src.local_model import LocalFabricModel, get_local_model_client, list_available_local_models
from src.model_review_store import ModelReviewStore
from src.report_generator import ReportGenerator
from src.utils import (
    analysis_engine_label,
    analyses_to_csv,
    classification_report_rows,
    compare_fabric_analyses,
    format_analysis_for_display,
    get_random_fun_fact,
    history_entry_from_summary,
    load_json_asset,
    model_prediction_warnings,
    summarize_analysis,
)
from ui.components import (
    render_color_palette,
    render_compare_card,
    render_feature_strip,
    render_hero,
    render_highlight_banner,
    render_key_value_block,
    render_list_block,
    render_metric_band,
    render_page_intro,
    render_sample_gallery,
    render_upload_panel,
)


FABRIC_GUIDE = [
    {
        "name": "Cotton",
        "feel": "Soft, breathable, dependable",
        "best_for": "Shirting, dresses, bedding, everyday casual wear",
        "watch_for": "Wrinkles easily and can shrink without pre-treatment",
    },
    {
        "name": "Linen",
        "feel": "Cool, crisp, airy",
        "best_for": "Summer tailoring, relaxed separates, table and home textiles",
        "watch_for": "Creases fast and usually benefits from steaming",
    },
    {
        "name": "Silk",
        "feel": "Smooth, fluid, refined sheen",
        "best_for": "Scarves, occasionwear, blouses, elevated linings",
        "watch_for": "Water spotting and abrasion on delicate weaves",
    },
    {
        "name": "Wool",
        "feel": "Warm, resilient, structured to plush",
        "best_for": "Coats, suiting, knitwear, upholstery accents",
        "watch_for": "Felting, pilling, and heat sensitivity",
    },
    {
        "name": "Denim",
        "feel": "Sturdy twill with visible grain",
        "best_for": "Jeans, jackets, workwear, utility pieces",
        "watch_for": "Color crocking and stiffness in heavier weights",
    },
    {
        "name": "Polyester",
        "feel": "Varies widely from crisp to silky",
        "best_for": "Easy-care garments, sportswear, blends, drapey prints",
        "watch_for": "Heat damage and lower breathability in dense weaves",
    },
]

CARE_GUIDE = [
    {
        "fabric": "Cotton",
        "wash": "Machine wash cold to warm",
        "dry": "Low tumble or line dry",
        "iron": "Medium to high heat",
    },
    {
        "fabric": "Linen",
        "wash": "Cold gentle wash",
        "dry": "Line dry preferred",
        "iron": "High heat with steam",
    },
    {
        "fabric": "Silk",
        "wash": "Hand wash or delicate bag",
        "dry": "Air dry flat or hung away from sun",
        "iron": "Low heat on reverse side",
    },
    {
        "fabric": "Wool",
        "wash": "Cool hand wash or wool cycle",
        "dry": "Flat dry only",
        "iron": "Low heat with pressing cloth",
    },
    {
        "fabric": "Polyester",
        "wash": "Machine wash cool",
        "dry": "Low tumble",
        "iron": "Low heat only",
    },
]

ANALYSIS_OPTIONS = ["AI-generated", "Local Heuristics", "Local Trained Model"]
MODE_LABELS = {
    "AI-generated": "ai",
    "Local Heuristics": "heuristic",
    "Local Trained Model": "trained",
}
WORKFLOW_BANNERS = {
    "analysis": {
        "heuristic": (
            "Local heuristic workflow",
            "Run the rule-based fabric brief without API keys. This mode is best for fast demos, privacy-sensitive work, and no-network usage.",
        ),
        "trained": (
            "Locally trained model workflow",
            "Use your trained classifier for fabric-family prediction, then let FabriSense build the rest of the brief with local rules and palette analysis.",
        ),
        "ai": (
            "AI-generated workflow",
            "Use the guided model path when you want richer summary language, cleaner reasoning, and a more editorial material brief.",
        ),
    },
    "batch": {
        "heuristic": (
            "Heuristic batch pass",
            "Use the rule-based local engine for fast sorting, tagging, and review of many images at once.",
        ),
        "trained": (
            "Local model batch pass",
            "Run your trained fabric classifier across a set of images while keeping the rest of the brief local and API-free.",
        ),
        "ai": (
            "AI-generated batch run",
            "Use the AI path when the batch needs stronger descriptive language and a more refined brief per image.",
        ),
    },
    "comparison": {
        "heuristic": (
            "Fast heuristic comparison",
            "No API setup required. Compare textile structure, color, and quality heuristics immediately.",
        ),
        "trained": (
            "Local model comparison",
            "Compare fabrics with the locally trained classifier while keeping the analysis fully offline.",
        ),
        "ai": (
            "AI-generated comparison",
            "Use the guided AI path when you want more interpretive differences in material description and commercial framing.",
        ),
    },
}

HISTORY = HistoryStore()
MODEL_REVIEWS = ModelReviewStore()


def _engine_label(metadata: Dict[str, Any]) -> str:
    return analysis_engine_label(metadata.get("analysis_mode"))


def _mode_spinner(mode: str, context: str = "analysis") -> str:
    if context == "comparison":
        if mode == "heuristic":
            return "Comparing local texture and color heuristics..."
        if mode == "trained":
            return "Comparing fabrics with the local trained model..."
        return "Building an AI-generated side-by-side review..."
    if mode == "heuristic":
        return "Running local vision heuristics..."
    if mode == "trained":
        return "Running the local trained model and building the brief..."
    return "Building an AI-generated material brief..."


def _mode_button_label(mode: str, context: str = "analysis") -> str:
    if context == "comparison":
        if mode == "heuristic":
            return "Run Heuristic Comparison"
        if mode == "trained":
            return "Run Local Model Comparison"
        return "Generate Comparison"
    if mode == "heuristic":
        return "Run Heuristic Analysis"
    if mode == "trained":
        return "Run Local Model Analysis"
    return "Generate AI Brief"


def _available_local_models() -> list[Dict[str, Any]]:
    return list_available_local_models()


def _create_analyzer(checkpoint_path: str | None = None) -> FabricAnalyzer:
    local_model_client = LocalFabricModel(checkpoint_path) if checkpoint_path else None
    return FabricAnalyzer(local_model_client=local_model_client)


def _render_loading_state(animation_key: str, height: int = 120) -> None:
    loading_asset = load_json_asset("assets/lottie_loading.json")
    if loading_asset:
        st_lottie(loading_asset, height=height, key=animation_key)
    st.markdown(f"<div class='loading-card'>{get_random_fun_fact()}</div>", unsafe_allow_html=True)


def _comma_list(values: list[str] | None, default: str = "N/A") -> str:
    if not values:
        return default
    return ", ".join(values)


def _render_workflow_banner(workflow: str, analysis_mode: str) -> None:
    banner_title, banner_body = WORKFLOW_BANNERS[workflow][analysis_mode]
    render_highlight_banner(banner_title, banner_body)


def _append_history_entry(analysis: Dict[str, Any], image_name: str) -> Dict[str, Any]:
    summary = summarize_analysis(analysis, image_name)
    HISTORY.append(history_entry_from_summary(summary))
    return summary


def _set_single_analysis_state(
    analysis: Dict[str, Any],
    report_bytes: bytes | None,
    image: Image.Image,
    image_name: str,
) -> None:
    st.session_state.analysis = analysis
    st.session_state.report_bytes = report_bytes
    st.session_state.image = image
    st.session_state.image_name = image_name


def _clear_single_analysis_state() -> None:
    st.session_state.analysis = None
    st.session_state.report_bytes = None
    st.session_state.image = None
    st.session_state.image_name = None


def _analysis_error_message(analysis_mode: str, context: str) -> str:
    if analysis_mode == "ai":
        return f"AI-generated {context} failed. Check your `.env` configuration."
    return f"Local {context} failed."


def _batch_error_row(
    image_name: str,
    analysis_mode: str,
    fabric: str,
    pattern: str,
    summary: str,
) -> Dict[str, Any]:
    return {
        "timestamp": "",
        "image_name": image_name,
        "mode": analysis_mode,
        "engine": "Error",
        "fabric": fabric,
        "pattern": pattern,
        "texture": "",
        "weight": "",
        "dominant_color": "",
        "quality_score": 0,
        "price_tier": "",
        "best_seasons": "",
        "predicted_label": "",
        "model_name": "",
        "model_architecture": "",
        "prediction_confidence": 0.0,
        "prediction_margin": 0.0,
        "review_flag": "",
        "summary": summary,
    }


def _render_local_model_selector(key: str) -> str | None:
    models = _available_local_models()
    if not models:
        st.warning("No trained local checkpoints were found in models/ or artifacts/.")
        return None

    labels = [item["display_name"] for item in models]
    selected_label = st.selectbox("Choose trained model", labels, key=key)
    selected_model = models[labels.index(selected_label)]
    metrics = selected_model.get("metrics", {}) or {}
    accuracy = metrics.get("accuracy")
    macro_f1 = metrics.get("macro_f1")
    caption_parts = [f"Architecture: {selected_model['architecture']}"]
    if accuracy is not None:
        caption_parts.append(f"Accuracy: {accuracy:.3f}")
    if macro_f1 is not None:
        caption_parts.append(f"Macro F1: {macro_f1:.3f}")
    st.caption(" | ".join(caption_parts))
    return selected_model["checkpoint_path"]


def _persist_uploaded_benchmark_zip(uploaded_file: Any) -> Path:
    incoming_dir = Path("data/benchmark_uploads/_incoming")
    incoming_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(getattr(uploaded_file, "name", "benchmark.zip")).name
    target_path = incoming_dir / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{safe_name}"
    target_path.write_bytes(uploaded_file.getvalue())
    return target_path


def _load_manifest_metadata(manifest_dir: str | Path | None) -> Dict[str, Any]:
    if not manifest_dir:
        return {}

    labels_path = Path(manifest_dir) / "labels.json"
    if not labels_path.exists():
        return {}

    try:
        return json.loads(labels_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _dataset_summary(metadata: Dict[str, Any]) -> Dict[str, str]:
    if not metadata:
        return {}

    class_counts = metadata.get("class_counts", {}) or {}
    total_images = sum(int(value) for value in class_counts.values()) if class_counts else 0
    summary = {
        "Dataset Root": metadata.get("dataset_root", "N/A"),
        "Labels": str(len(metadata.get("labels", []))),
        "Total Images": str(total_images or sum(int(value) for value in (metadata.get("counts", {}) or {}).values())),
        "Train / Val / Test": (
            f"{metadata.get('counts', {}).get('train', 0)} / "
            f"{metadata.get('counts', {}).get('val', 0)} / "
            f"{metadata.get('counts', {}).get('test', 0)}"
        ),
        "Scope": "Curated subset" if metadata.get("included_classes") else "Full manifest",
    }

    if class_counts:
        smallest_label = min(class_counts, key=class_counts.get)
        largest_label = max(class_counts, key=class_counts.get)
        summary["Smallest Class"] = f"{smallest_label} ({class_counts[smallest_label]})"
        summary["Largest Class"] = f"{largest_label} ({class_counts[largest_label]})"

    return summary


def _comparison_story_rows() -> list[Dict[str, Any]]:
    return [
        {
            "model": "model_b_resnet18_v2",
            "architecture": "resnet18",
            "role": "Best overall",
            "benchmark": "phase1 curated 10-class",
            "accuracy": 0.821,
            "macro_f1": 0.830,
            "weighted_f1": 0.823,
        },
        {
            "model": "model_c_mobilenet_v3_small_v2",
            "architecture": "mobilenet_v3_small",
            "role": "Lightweight option",
            "benchmark": "phase1 curated 10-class",
            "accuracy": 0.806,
            "macro_f1": 0.818,
            "weighted_f1": 0.808,
        },
        {
            "model": "model_a_scratch_v2",
            "architecture": "scratch_cnn",
            "role": "Baseline",
            "benchmark": "phase1 curated 10-class",
            "accuracy": 0.316,
            "macro_f1": 0.438,
            "weighted_f1": 0.227,
        },
    ]


def _render_analysis_guide(analysis_mode: str) -> None:
    mode_title = {
        "ai": "AI-generated",
        "heuristic": "Local Heuristics",
        "trained": "Local Trained Model",
    }.get(analysis_mode, "Analysis")
    with st.expander("Guide: choosing an analysis mode", expanded=False):
        st.markdown(
            f"""
Use `{mode_title}` when it matches your goal.

- `AI-generated`: best for polished summaries, richer narrative, and presentation-ready language.
- `Local Heuristics`: best for fast offline demos and explainable baseline behavior.
- `Local Trained Model`: best when you want your own benchmarked classifier in the loop.

Recommended flow:

1. Start with `Local Trained Model` for the strongest offline prediction path.
2. Check confidence warnings and top alternatives in the results.
3. Switch to `AI-generated` if you want a more editorial brief for presentation.
4. Use `Compare Fabrics` or `Models` when you need evidence rather than only a single result.
"""
        )


def _render_results_guide(model_prediction: Dict[str, Any] | None = None) -> None:
    with st.expander("Guide: how to read these results", expanded=False):
        lines = [
            "- `Overview` is the fastest summary for fabric family, texture, quality, and commercial fit.",
            "- `Material Read` is where you inspect structure, surface behavior, and model evidence.",
            "- `Commercial Fit` is where you decide whether the fabric makes sense for season, care, and price tier.",
            "- `Narrative` is the presentation layer for explaining the fabric to a non-technical audience.",
        ]
        if model_prediction:
            lines.extend(
                [
                    "- `Model Review` is where you confirm or correct the trained-model prediction.",
                    "- Confidence is useful, but it is not proof. Read it together with the top alternative labels and the visible fabric cues.",
                ]
            )
        st.markdown("\n".join(lines))


def _render_model_guide() -> None:
    with st.expander("Guide: models, benchmarks, and comparison study", expanded=True):
        st.markdown(
            """
Use this page in three layers.

1. `Curated Phase1 Benchmark`
   Read the headline comparison on the curated `phase1` 10-class benchmark. This is the cleanest presentation story.
2. `Checkpoint Leaderboard`
   Inspect saved checkpoints, metrics, and per-class strengths or weaknesses.
3. `Benchmark Lab`
   Run a fair comparison by evaluating multiple checkpoints on the same manifest or on a new uploaded labeled ZIP.

How to explain the study:

- `scratch_cnn` is the learned baseline.
- `mobilenet_v3_small` is the lightweight deployment candidate.
- `resnet18` is the best overall local classifier.
- `AI-generated` mode helps narration, but it is not the benchmark source of truth.

How to compare responsibly:

- Use the same benchmark split for every checkpoint.
- Prefer `macro F1` over accuracy when class balance is uneven.
- Mention that the current headline results come from the curated `phase1` 10-class benchmark.
- If you prepare a new ZIP benchmark, keep it fully unseen relative to training images.
"""
        )


def _model_entry_for_checkpoint(checkpoint_path: str | None) -> Dict[str, Any] | None:
    if not checkpoint_path:
        return None
    for model in _available_local_models():
        if model.get("checkpoint_path") == checkpoint_path:
            return model
    return None


def _labels_for_prediction(prediction: Dict[str, Any]) -> list[str]:
    checkpoint_path = prediction.get("checkpoint_path")
    model_entry = _model_entry_for_checkpoint(checkpoint_path)
    if model_entry and model_entry.get("labels"):
        return list(model_entry["labels"])

    labels = [prediction.get("label", "")]
    labels.extend(item.get("label", "") for item in prediction.get("top_predictions", []))
    unique_labels = []
    for label in labels:
        if label and label not in unique_labels:
            unique_labels.append(label)
    return unique_labels


def _review_entry_from_analysis(
    analysis: Dict[str, Any],
    image_name: str,
    corrected_label: str,
    notes: str,
) -> Dict[str, Any]:
    prediction = analysis.get("llm_analysis", {}).get("model_prediction", {}) or {}
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "image_name": image_name,
        "predicted_label": prediction.get("label", ""),
        "corrected_label": corrected_label,
        "confidence": round(float(prediction.get("confidence", 0) or 0), 4),
        "model_name": prediction.get("model_name", ""),
        "architecture": prediction.get("architecture", ""),
        "checkpoint_path": prediction.get("checkpoint_path", ""),
        "notes": notes.strip(),
    }


def _model_warning_rows(prediction: Dict[str, Any]) -> list[str]:
    return model_prediction_warnings(prediction)


def _safe_text(value: Any) -> str:
    return html_escape("" if value is None else str(value), quote=True)


def render_home_page() -> None:
    render_hero()
    render_feature_strip()

    mode_label = st.radio("Analysis Mode", ANALYSIS_OPTIONS, horizontal=True)
    analysis_mode = MODE_LABELS[mode_label]
    _render_analysis_guide(analysis_mode)

    _render_workflow_banner("analysis", analysis_mode)

    input_left, input_right = st.columns((1.05, 0.95))
    with input_left:
        upload_choice = render_upload_panel(
            title="Upload a fabric image",
            prompt="Drop a close-up or flat-lay textile image for analysis",
        )
    with input_right:
        sample_choice = render_sample_gallery("assets/sample_fabrics", state_key="home_selected_sample")
    choice = upload_choice or sample_choice

    if choice is None:
        st.info("Choose a curated sample or upload an image to start a material read.")
        return

    image, image_name = choice
    selected_checkpoint = _render_local_model_selector("home_trained_model") if analysis_mode == "trained" else None
    button_label = _mode_button_label(analysis_mode)
    if st.button(
        button_label,
        type="primary",
        width="stretch",
        disabled=analysis_mode == "trained" and not selected_checkpoint,
    ):
        _run_analysis(
            image=image,
            image_name=image_name,
            analysis_mode=analysis_mode,
            checkpoint_path=selected_checkpoint,
        )


def _run_analysis(image, image_name: str, analysis_mode: str, checkpoint_path: str | None = None) -> None:
    with st.container():
        _render_loading_state("loading-animation", height=140)
        spinner_text = _mode_spinner(analysis_mode)
        with st.spinner(spinner_text):
            try:
                analyzer = _create_analyzer(checkpoint_path)
                analysis = analyzer.analyze(image, mode=analysis_mode)
            except Exception as exc:
                prefix = _analysis_error_message(analysis_mode, "analysis")
                st.error(f"{prefix} Details: {exc}")
                return

            report_bytes = None
            try:
                report_bytes = ReportGenerator().generate_pdf(analysis, image)
            except Exception as exc:
                st.warning(f"Analysis completed, but PDF generation is unavailable. Details: {exc}")

    _append_history_entry(analysis, image_name)
    _set_single_analysis_state(analysis, report_bytes, image, image_name)
    st.rerun()


def render_results_page(analysis: Dict[str, Any], report_bytes: bytes | None, image, image_name: str) -> None:
    metadata = analysis.get("analysis_metadata", {})
    render_page_intro(
        "ANALYSIS OUTPUT",
        "Material brief ready for review.",
        "The result below combines structure, palette, surface behavior, and commercial guidance into one presentation layer.",
    )
    st.caption(
        f"Mode: {metadata.get('analysis_mode', 'unknown')} | Engine: {_engine_label(metadata)} | "
        f"Color clusters: {metadata.get('color_clusters', 'N/A')}"
    )
    display = format_analysis_for_display(analysis)
    render_metric_band(display)

    llm = analysis.get("llm_analysis", {})
    fabric = llm.get("fabric_type", {})
    pattern = llm.get("pattern", {})
    texture = llm.get("texture", {})
    quality = llm.get("quality_assessment", {})
    care = llm.get("care_instructions", {})
    season = llm.get("season_recommendation", {})
    price = llm.get("price_range", {})
    sustainability = llm.get("sustainability", {})
    model_prediction = llm.get("model_prediction", {})
    palette = analysis.get("color_palette", {})
    interior = llm.get("interior_use", {})
    _render_results_guide(model_prediction if model_prediction else None)

    tab_labels = ["Overview", "Material Read", "Commercial Fit", "Narrative"]
    if model_prediction:
        tab_labels.append("Model Review")
    tabs = st.tabs(tab_labels)
    overview_tab, material_tab, commercial_tab, narrative_tab = tabs[:4]
    model_review_tab = tabs[4] if model_prediction else None

    with overview_tab:
        left, right = st.columns((0.95, 1.05))
        with left:
            st.image(image, caption=image_name, width="stretch")
            action_cols = st.columns(2)
            with action_cols[0]:
                if report_bytes:
                    st.download_button(
                        "Download PDF Report",
                        data=report_bytes,
                        file_name=f"{image_name.rsplit('.', 1)[0]}-fabrisense-report.pdf",
                        mime="application/pdf",
                        width="stretch",
                    )
            with action_cols[1]:
                if st.button("Start New Analysis", width="stretch"):
                    _clear_single_analysis_state()
                    st.rerun()

        with right:
            render_key_value_block(
                "Material Snapshot",
                {
                    "Primary Fabric": fabric.get("primary", "N/A"),
                    "Subtype": fabric.get("sub_type", "N/A"),
                    "Estimated Blend": fabric.get("blend_composition", "N/A"),
                    "Confidence": fabric.get("confidence", "N/A"),
                    "Pattern": f"{pattern.get('type', 'N/A')} / {pattern.get('sub_type', 'N/A')}",
                    "Texture": texture.get("primary", "N/A"),
                    "Hand Feel": texture.get("hand_feel", "N/A"),
                    "Weight": texture.get("weight", "N/A"),
                    "Drape": texture.get("drape", "N/A"),
                },
            )
            render_key_value_block(
                "Commercial Snapshot",
                {
                    "Price Tier": price.get("category", "N/A"),
                    "USD Range": price.get("estimated_per_meter_usd", "N/A"),
                    "Best Seasons": _comma_list(season.get("best_seasons")),
                    "Eco Score": sustainability.get("eco_score", "N/A"),
                },
            )

        render_color_palette(palette.get("colors", []), palette.get("harmony_type", "Unknown"))

    with material_tab:
        left, right = st.columns(2)
        with left:
            render_key_value_block(
                "Structure and Surface",
                {
                    "Primary Fabric": fabric.get("primary", "N/A"),
                    "Subtype": fabric.get("sub_type", "N/A"),
                    "Pattern": pattern.get("type", "N/A"),
                    "Pattern Detail": pattern.get("sub_type", "N/A"),
                    "Texture": texture.get("primary", "N/A"),
                    "Hand Feel": texture.get("hand_feel", "N/A"),
                    "Weight": texture.get("weight", "N/A"),
                    "Drape": texture.get("drape", "N/A"),
                },
            )
            render_list_block("Quality Factors", quality.get("factors", []))

        with right:
            if model_prediction:
                render_list_block(
                    "Model Prediction",
                    [
                        f"Model: {model_prediction.get('model_name', 'N/A')} ({model_prediction.get('architecture', 'N/A')})",
                        f"Primary label: {model_prediction.get('label', 'N/A')} ({round(float(model_prediction.get('confidence', 0)) * 100, 1)}%)",
                        *[
                            f"Alt: {item.get('label', 'N/A')} ({round(float(item.get('confidence', 0)) * 100, 1)}%)"
                            for item in model_prediction.get('top_predictions', [])[1:]
                        ],
                        f"Checkpoint: {model_prediction.get('checkpoint_path', 'N/A')}",
                    ],
                )
                render_list_block("Prediction Warnings", _model_warning_rows(model_prediction))
                st.caption("Trained-model confidence is a softmax score. It can still be overconfident on images unlike the training set.")
            render_list_block(
                "Styling Suggestions",
                [
                    f"{item.get('garment', 'N/A')}: {item.get('style', 'N/A')} for {item.get('target_audience', 'N/A')}"
                    for item in llm.get("styling_suggestions", [])
                ],
            )

    with commercial_tab:
        left, right = st.columns(2)
        with left:
            render_key_value_block(
                "Quality and Care",
                {
                    "Quality Score": f"{quality.get('score', 'N/A')} / 10",
                    "Grade": quality.get("grade", "N/A"),
                    "Durability": quality.get("durability_estimate", "N/A"),
                    "Pilling Tendency": quality.get("pilling_tendency", "N/A"),
                    "Washing": care.get("washing", "N/A"),
                    "Drying": care.get("drying", "N/A"),
                    "Ironing": care.get("ironing", "N/A"),
                    "Special Care": care.get("special_care", "N/A"),
                },
            )
            render_list_block(
                "Occasion Suitability",
                [
                    f"{item.get('occasion', 'N/A')} ({item.get('suitability_score', 'N/A')}/10): {item.get('note', 'N/A')}"
                    for item in llm.get("occasion_suitability", [])
                ],
            )

        with right:
            render_key_value_block(
                "Commercial Fit",
                {
                    "Best Seasons": _comma_list(season.get("best_seasons")),
                    "Avoid Seasons": _comma_list(season.get("avoid_seasons")),
                    "Breathability": season.get("breathability", "N/A"),
                    "Price Tier": price.get("category", "N/A"),
                    "USD Range": price.get("estimated_per_meter_usd", "N/A"),
                    "Value": price.get("value_for_money", "N/A"),
                    "Eco Score": sustainability.get("eco_score", "N/A"),
                    "Impact": sustainability.get("environmental_impact", "N/A"),
                },
            )
            render_list_block("Interior Uses", interior.get("suggestions", []))

    with narrative_tab:
        left, right = st.columns(2)
        with left:
            render_key_value_block(
                "Narrative Summary",
                {
                    "Overall Summary": llm.get("overall_summary", "N/A"),
                    "Fun Fact": llm.get("fun_fact", "N/A"),
                    "Interior Notes": interior.get("notes", "N/A"),
                    "Sustainability Notes": sustainability.get("notes", "N/A"),
                },
            )
        with right:
            render_list_block(
                "Decision Notes",
                [
                    f"Blend estimate: {fabric.get('blend_composition', 'N/A')}",
                    f"Dominant color: {palette.get('dominant_color', {}).get('name', 'N/A')}",
                    f"Pattern direction: {pattern.get('type', 'N/A')}",
                    f"Commercial value: {price.get('value_for_money', 'N/A')}",
                ],
            )

    if model_review_tab is not None:
        with model_review_tab:
            review_left, review_right = st.columns((1.05, 0.95))
            with review_left:
                render_key_value_block(
                    "Model Evidence",
                    {
                        "Predicted Label": model_prediction.get("label", "N/A"),
                        "Confidence": f"{round(float(model_prediction.get('confidence', 0) or 0) * 100, 1)}%",
                        "Architecture": model_prediction.get("architecture", "N/A"),
                        "Model Name": model_prediction.get("model_name", "N/A"),
                        "Checkpoint": model_prediction.get("checkpoint_path", "N/A"),
                    },
                )
                render_list_block("Warnings", _model_warning_rows(model_prediction))

            with review_right:
                review_labels = _labels_for_prediction(model_prediction)
                predicted_label = model_prediction.get("label", "")
                default_index = review_labels.index(predicted_label) if predicted_label in review_labels else 0
                corrected_label = st.selectbox(
                    "Reviewed Label",
                    review_labels or [predicted_label or "Unknown"],
                    index=default_index,
                    key=f"model-review-label-{image_name}",
                )
                review_notes = st.text_area(
                    "Reviewer Notes",
                    placeholder="Add why you agree, disagree, or want to revisit this prediction.",
                    key=f"model-review-notes-{image_name}",
                )
                if st.button("Save Model Review", type="primary", width="stretch", key=f"save-review-{image_name}"):
                    MODEL_REVIEWS.append(_review_entry_from_analysis(analysis, image_name, corrected_label, review_notes))
                    st.success("Model review saved to the local review log.")


def render_batch_page() -> None:
    render_page_intro(
        "MULTI-ITEM WORKFLOW",
        "Analyze a batch of fabric images in one run.",
        "Use batch mode to review seller catalogs, classroom submissions, or sourcing references and export the summary as CSV.",
    )
    mode_label = st.radio("Batch Mode", ANALYSIS_OPTIONS, horizontal=True, key="batch_mode")
    analysis_mode = MODE_LABELS[mode_label]

    _render_workflow_banner("batch", analysis_mode)

    files = st.file_uploader(
        "Upload multiple fabric images",
        type=sorted(ImagePreprocessor.SUPPORTED_FORMATS),
        accept_multiple_files=True,
        key="batch_upload",
    )

    selected_checkpoint = _render_local_model_selector("batch_trained_model") if analysis_mode == "trained" else None
    if files and st.button(
        "Run Batch Analysis",
        type="primary",
        width="stretch",
        disabled=analysis_mode == "trained" and not selected_checkpoint,
    ):
        _run_batch_analysis(files, analysis_mode, checkpoint_path=selected_checkpoint)

    bundle = st.session_state.batch_bundle
    if not bundle:
        st.info("Upload several textile images to generate a batch summary and CSV export.")
        return

    rows = bundle["rows"]
    st.caption(f"Batch size: {len(rows)} | Mode: {bundle['analysis_mode']} | Engine: {bundle['engine']}")
    displayed_rows = rows
    if any(row.get("model_name") for row in rows):
        filter_left, filter_right = st.columns(2)
        with filter_left:
            min_confidence = st.slider("Minimum prediction confidence", 0, 100, 0, key="batch-confidence-filter")
        with filter_right:
            needs_review_only = st.checkbox("Show only rows flagged for review", key="batch-review-filter")

        displayed_rows = [
            row
            for row in rows
            if float(row.get("prediction_confidence", 0) or 0) * 100 >= min_confidence
            and (not needs_review_only or bool(row.get("review_flag")))
        ]
        st.caption(f"Visible rows after filters: {len(displayed_rows)}")

    st.download_button(
        "Download Batch CSV",
        data=analyses_to_csv(displayed_rows),
        file_name="fabrisense-batch-summary.csv",
        mime="text/csv",
        width="stretch",
    )
    st.dataframe(displayed_rows, width="stretch")

    for item in displayed_rows:
        with st.expander(item["image_name"]):
            render_key_value_block(
                "Batch Summary",
                {
                    "Fabric": item["fabric"],
                    "Pattern": item["pattern"],
                    "Texture": item["texture"],
                    "Dominant Color": item["dominant_color"],
                    "Quality": item["quality_score"],
                    "Price Tier": item["price_tier"],
                    "Best Seasons": item["best_seasons"] or "N/A",
                    "Predicted Label": item.get("predicted_label") or "N/A",
                    "Prediction Confidence": (
                        f"{round(float(item.get('prediction_confidence', 0) or 0) * 100, 1)}%"
                        if item.get("predicted_label")
                        else "N/A"
                    ),
                    "Review Flag": item.get("review_flag") or "Clear",
                    "Summary": item["summary"],
                },
            )


def _run_batch_analysis(files: list[Any], analysis_mode: str, checkpoint_path: str | None = None) -> None:
    _render_loading_state("batch-loading")

    rows = []
    details = []
    with st.spinner("Running batch analysis across uploaded materials..."):
        analyzer = _create_analyzer(checkpoint_path)
        for uploaded in files:
            valid, message = ImagePreprocessor.validate_image(uploaded)
            if not valid:
                rows.append(
                    _batch_error_row(
                        image_name=getattr(uploaded, "name", "unknown"),
                        analysis_mode=analysis_mode,
                        fabric="Invalid image",
                        pattern=message,
                        summary="Validation failed before analysis.",
                    )
                )
                continue

            try:
                image = ImagePreprocessor.load_image(uploaded)
                analysis = analyzer.analyze(image, mode=analysis_mode)
                row = _append_history_entry(analysis, uploaded.name)
                rows.append(row)
                details.append(row)
            except Exception as exc:
                rows.append(
                    _batch_error_row(
                        image_name=getattr(uploaded, "name", "unknown"),
                        analysis_mode=analysis_mode,
                        fabric="Analysis failed",
                        pattern=str(exc),
                        summary="This file failed during analysis, but the batch continued.",
                    )
                )

    st.session_state.batch_bundle = {
        "rows": rows,
        "details": details,
        "analysis_mode": analysis_mode,
        "engine": analysis_engine_label(analysis_mode),
    }
    st.rerun()


def render_compare_page() -> None:
    render_page_intro(
        "SIDE-BY-SIDE REVIEW",
        "Compare two materials in one workspace.",
        "Use the comparison view to separate fabric family, pattern direction, palette shifts, and visual quality without jumping between tabs.",
    )

    mode_label = st.radio("Comparison Mode", ANALYSIS_OPTIONS, horizontal=True, key="compare_mode")
    analysis_mode = MODE_LABELS[mode_label]

    _render_workflow_banner("comparison", analysis_mode)

    left, right = st.columns(2)
    with left:
        image_a, name_a = _render_compare_input("Material A", "compare_a")
    with right:
        image_b, name_b = _render_compare_input("Material B", "compare_b")

    selected_checkpoint = _render_local_model_selector("compare_trained_model") if analysis_mode == "trained" else None
    if image_a is not None and image_b is not None:
        button_label = _mode_button_label(analysis_mode, context="comparison")
        if st.button(
            button_label,
            type="primary",
            width="stretch",
            disabled=analysis_mode == "trained" and not selected_checkpoint,
        ):
            _run_comparison(image_a, name_a, image_b, name_b, analysis_mode, checkpoint_path=selected_checkpoint)

    bundle = st.session_state.comparison_bundle
    if not bundle:
        return

    st.divider()
    render_page_intro(
        "COMPARISON RESULT",
        "A clearer read on which material performs better visually.",
        "Review the recommendation, inspect each textile panel, and use the differences list to explain the selection with confidence.",
    )
    st.caption(f"Mode: {bundle.get('analysis_mode', 'unknown')} | Engine: {_engine_label(bundle)}")

    summary = bundle["summary"]
    winner = summary["winner"]
    winner_text = f"Recommended option: {winner}" if winner != "Tie" else "Recommended option: Tie"
    render_highlight_banner(winner_text, summary["winner_reason"])

    score_cols = st.columns(2)
    score_cols[0].metric(bundle["name_a"], f"{summary['score_a']:.1f}/10")
    score_cols[1].metric(bundle["name_b"], f"{summary['score_b']:.1f}/10")

    compare_summary_cols = st.columns(2)
    with compare_summary_cols[0]:
        st.markdown(
            f"""
            <div class="compare-summary-card">
                <p class="compare-summary-label">Fabric Direction</p>
                <div class="compare-summary-flow">
                    <div><span>{_safe_text(bundle['name_a'])}</span><strong>{_safe_text(summary['fabric_a'])}</strong></div>
                    <div><span>{_safe_text(bundle['name_b'])}</span><strong>{_safe_text(summary['fabric_b'])}</strong></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with compare_summary_cols[1]:
        st.markdown(
            f"""
            <div class="compare-summary-card">
                <p class="compare-summary-label">Pattern Direction</p>
                <div class="compare-summary-flow">
                    <div><span>{_safe_text(bundle['name_a'])}</span><strong>{_safe_text(summary['pattern_a'])}</strong></div>
                    <div><span>{_safe_text(bundle['name_b'])}</span><strong>{_safe_text(summary['pattern_b'])}</strong></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    left_result, right_result = st.columns(2)
    with left_result:
        render_compare_card(bundle["name_a"], bundle["analysis_a"], bundle["image_a"])
    with right_result:
        render_compare_card(bundle["name_b"], bundle["analysis_b"], bundle["image_b"])

    list_left, list_right = st.columns(2)
    with list_left:
        render_list_block("Shared Signals", summary["similarities"])
    with list_right:
        render_list_block("Meaningful Differences", summary["differences"])

    if st.button("Clear Comparison", width="stretch"):
        st.session_state.comparison_bundle = None
        st.rerun()


def _run_comparison(
    image_a: Image.Image,
    name_a: str,
    image_b: Image.Image,
    name_b: str,
    analysis_mode: str,
    checkpoint_path: str | None = None,
) -> None:
    _render_loading_state("comparison-loading")

    spinner_text = _mode_spinner(analysis_mode, context="comparison")
    with st.spinner(spinner_text):
        try:
            analyzer = _create_analyzer(checkpoint_path)
            analysis_a = analyzer.analyze(image_a, mode=analysis_mode)
            analysis_b = analyzer.analyze(image_b, mode=analysis_mode)
            summary = compare_fabric_analyses(analysis_a, name_a, analysis_b, name_b)
        except Exception as exc:
            prefix = _analysis_error_message(analysis_mode, "comparison")
            st.error(f"{prefix} Details: {exc}")
            return

    st.session_state.comparison_bundle = {
        "analysis_a": analysis_a,
        "analysis_b": analysis_b,
        "image_a": image_a,
        "image_b": image_b,
        "name_a": name_a,
        "name_b": name_b,
        "summary": summary,
        "analysis_mode": analysis_mode,
        "model_used": analysis_a.get("analysis_metadata", {}).get("model_used", "unknown"),
    }
    st.rerun()


def _render_compare_input(title: str, key_prefix: str) -> tuple[Image.Image | None, str | None]:
    st.markdown(f"### {title}")
    uploaded = st.file_uploader(
        f"Upload image for {title}",
        type=sorted(ImagePreprocessor.SUPPORTED_FORMATS),
        key=f"{key_prefix}_upload",
        accept_multiple_files=False,
    )

    sample_paths = sorted(Path("assets/sample_fabrics").glob("*.jpg"))
    sample_labels = ["None"] + [path.stem.replace("_", " ").title() for path in sample_paths]
    selected_label = st.selectbox(f"Or choose a curated sample for {title}", sample_labels, key=f"{key_prefix}_sample")

    image = None
    name = None

    if uploaded is not None:
        valid, message = ImagePreprocessor.validate_image(uploaded)
        if not valid:
            st.error(message)
            return None, None
        image = ImagePreprocessor.load_image(uploaded)
        name = uploaded.name
        st.caption(message)
    elif selected_label != "None":
        selected_path = sample_paths[sample_labels.index(selected_label) - 1]
        image = Image.open(selected_path).convert("RGB")
        name = selected_path.name

    if image is not None and name is not None:
        st.image(ImagePreprocessor.resize_for_display(image), caption=name, width="stretch")

    return image, name


def render_history_page() -> None:
    render_page_intro(
        "WORKING HISTORY",
        "Review recent material reads without re-uploading.",
        "History keeps a compact local log of prior runs so the app works more like a real review workspace.",
    )
    history = HISTORY.load()
    if not history:
        st.info("No saved analysis history yet. Run a single or batch analysis first.")
        return

    st.download_button(
        "Download History CSV",
        data=analyses_to_csv(history),
        file_name="fabrisense-history.csv",
        mime="text/csv",
        width="stretch",
    )
    if st.button("Clear History", width="stretch"):
        HISTORY.clear()
        st.rerun()

    st.dataframe(history, width="stretch")


def render_fabric_guide_page() -> None:
    render_page_intro(
        "REFERENCE LIBRARY",
        "A compact guide to common fabric families.",
        "Use this page as a quick working reference when you need plain-language reminders about feel, use cases, and caution points.",
    )

    cols = st.columns(2)
    for index, item in enumerate(FABRIC_GUIDE):
        with cols[index % 2]:
            render_key_value_block(
                item["name"],
                {
                    "Feel": item["feel"],
                    "Best For": item["best_for"],
                    "Watch For": item["watch_for"],
                },
            )


def render_care_guide_page() -> None:
    render_page_intro(
        "CARE DEFAULTS",
        "Fast handling guidance for common material families.",
        "These are general defaults for textile handling. Final garment care still depends on dye, finish, trims, and construction.",
    )
    st.table(CARE_GUIDE)

    render_list_block(
        "Good Habits",
        [
            "Test a hidden spot before washing delicate or richly dyed textiles.",
            "Use lower heat first. Heat damage is harder to reverse than under-drying.",
            "Store natural fibers dry and breathable to avoid mildew or distortion.",
            "When unsure, follow the garment care label over generic fabric guidance.",
        ],
    )


def render_model_info_page() -> None:
    model_info = get_local_model_client().describe()
    available_models = _available_local_models()
    reviews = MODEL_REVIEWS.load()
    render_page_intro(
        "MODEL STACK",
        "How FabriSense separates heuristics, trained models, and AI-generated analysis.",
        "Use this page to explain the technical difference between the local heuristic engine, the locally trained model, and the optional AI-generated workflow.",
    )
    _render_model_guide()

    render_key_value_block(
        "Current Local Model Status",
        {
            "Availability": "Ready" if model_info["available"] else "Not available",
            "Model Name": model_info["model_name"],
            "Architecture": model_info["architecture"],
            "Class Count": model_info["class_count"],
            "Checkpoint": model_info["checkpoint_path"] or "No checkpoint found in models/ or artifacts/",
        },
    )

    left, right = st.columns(2)
    with left:
        render_key_value_block(
            "Local Heuristics",
            {
                "What It Uses": "Palette extraction, contrast, edge density, repeat cues, and rule-based scoring.",
                "Strength": "Fast, explainable, offline, and no extra model files required.",
                "Limitation": "Fabric-family prediction is approximate because it is inferred from handcrafted rules.",
            },
        )
        render_key_value_block(
            "Locally Trained Model",
            {
                "What It Uses": "A trained classifier predicts fabric family from the uploaded image.",
                "Strength": "Prediction layer belongs to the project and is measurable with accuracy and macro F1.",
                "Limitation": "Only the fabric-family field comes from the trained model today; the rest of the brief still uses local rules.",
            },
        )
    with right:
        render_key_value_block(
            "AI-generated Analysis",
            {
                "What It Uses": "A multimodal provider generates the material brief from the image and prompt.",
                "Strength": "Best for polished language, richer narrative, and more editorial summaries.",
                "Limitation": "Depends on provider availability and is not the source of truth for research evaluation.",
            },
        )
        render_list_block(
            "Recommended Usage",
            [
                "Use Local Heuristics for quick offline demos and baseline comparisons.",
                "Use Locally Trained Model when you want your own classifier in the loop.",
                "Use AI-generated Analysis when the presentation needs richer natural-language output.",
            ],
        )

    if model_info["labels"]:
        render_list_block("Default Model Labels", model_info["labels"])

    if available_models:
        st.markdown("### Curated Phase1 Benchmark")
        st.caption(
            "These headline results come from the curated `phase1` 10-class benchmark after switching to a group-aware split that keeps same-sample image variants in one split."
        )
        st.dataframe(_comparison_story_rows(), width="stretch")

        leaderboard_rows = []
        for model in available_models:
            metrics = model.get("metrics", {}) or {}
            leaderboard_rows.append(
                {
                    "model_name": model["model_name"],
                    "architecture": model["architecture"],
                    "pretrained": model["pretrained"],
                    "accuracy": round(float(metrics.get("accuracy", 0) or 0), 3) if metrics.get("accuracy") is not None else None,
                    "macro_f1": round(float(metrics.get("macro_f1", 0) or 0), 3) if metrics.get("macro_f1") is not None else None,
                    "weighted_f1": round(float(metrics.get("weighted_f1", 0) or 0), 3) if metrics.get("weighted_f1") is not None else None,
                    "loss": round(float(metrics.get("loss", 0) or 0), 3) if metrics.get("loss") is not None else None,
                    "class_count": model["class_count"],
                    "checkpoint_path": model["checkpoint_path"],
                }
            )

        st.markdown("### Checkpoint Leaderboard")
        st.dataframe(leaderboard_rows, width="stretch")

        selected_model_name = st.selectbox(
            "Inspect checkpoint",
            [model["display_name"] for model in available_models],
            key="model-dashboard-selection",
        )
        selected_model = available_models[[model["display_name"] for model in available_models].index(selected_model_name)]
        selected_metrics = selected_model.get("metrics", {}) or {}
        selected_rows = classification_report_rows(selected_metrics)
        config_path = Path(selected_model["checkpoint_path"]).parent / "config.json"
        selected_config = {}
        if config_path.exists():
            try:
                selected_config = json.loads(config_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                selected_config = {}
        selected_manifest_metadata = _load_manifest_metadata(selected_config.get("manifest_dir"))

        overview_left, overview_right = st.columns(2)
        with overview_left:
            render_key_value_block(
                "Selected Checkpoint",
                {
                    "Model": selected_model["model_name"],
                    "Architecture": selected_model["architecture"],
                    "Pretrained": selected_model["pretrained"],
                    "Accuracy": (
                        f"{selected_metrics.get('accuracy', 0):.3f}" if selected_metrics.get("accuracy") is not None else "N/A"
                    ),
                    "Macro F1": (
                        f"{selected_metrics.get('macro_f1', 0):.3f}" if selected_metrics.get("macro_f1") is not None else "N/A"
                    ),
                    "Weighted F1": (
                        f"{selected_metrics.get('weighted_f1', 0):.3f}" if selected_metrics.get("weighted_f1") is not None else "N/A"
                    ),
                    "Loss": f"{selected_metrics.get('loss', 0):.3f}" if selected_metrics.get("loss") is not None else "N/A",
                    "Class Count": selected_model["class_count"],
                    "Checkpoint": selected_model["checkpoint_path"],
                },
            )
            if selected_manifest_metadata:
                render_key_value_block("Training Dataset", _dataset_summary(selected_manifest_metadata))
        with overview_right:
            render_key_value_block(
                "Research Framing",
                {
                    "Baseline": "Local Heuristics or scratch CNN",
                    "Comparison Goal": "Show how transfer learning improves macro F1 on the same benchmark split",
                    "Presentation Layer": "AI-generated mode adds narrative polish but is not the benchmark source of truth",
                    "Key Caution": "Read macro F1 together with dataset scope and class balance",
                },
            )
            if selected_rows:
                strongest_rows = sorted(selected_rows, key=lambda row: row["f1_score"], reverse=True)[:5]
                weakest_rows = sorted(selected_rows, key=lambda row: row["f1_score"])[:5]
                st.markdown("### Strongest Classes")
                st.dataframe(strongest_rows, width="stretch")
                st.markdown("### Weakest Classes")
                st.dataframe(weakest_rows, width="stretch")

        confusion_matrix = selected_metrics.get("confusion_matrix", []) or []
        if confusion_matrix:
            st.caption(
                f"Confusion matrix shape: {len(confusion_matrix)} x {len(confusion_matrix[0]) if confusion_matrix else 0}"
            )

        st.markdown("### Benchmark Lab")
        manifest_entries = list_manifest_directories()
        uploaded_manifest = st.session_state.get("uploaded_benchmark_manifest")
        if uploaded_manifest and Path(uploaded_manifest.get("manifest_dir", "")).exists():
            existing_dirs = {item["manifest_dir"] for item in manifest_entries}
            if uploaded_manifest["manifest_dir"] not in existing_dirs:
                manifest_entries.insert(0, uploaded_manifest)
        elif uploaded_manifest:
            st.session_state.uploaded_benchmark_manifest = None

        st.markdown("#### Evaluate New Labeled ZIP")
        st.caption("Upload a ZIP where each top-level folder is a label, for example `Cotton/*.jpg` and `Denim/*.png`.")
        uploaded_zip = st.file_uploader(
            "Upload labeled benchmark ZIP",
            type=["zip"],
            key="benchmark-zip-upload",
            accept_multiple_files=False,
        )
        upload_actions = st.columns(2)
        with upload_actions[0]:
            if st.button(
                "Prepare Uploaded Benchmark Set",
                width="stretch",
                disabled=uploaded_zip is None,
                key="prepare-uploaded-benchmark",
            ):
                zip_path = _persist_uploaded_benchmark_zip(uploaded_zip)
                try:
                    uploaded_bundle = create_uploaded_benchmark_manifest(zip_path)
                except Exception as exc:
                    st.error(f"Uploaded benchmark preparation failed. Details: {exc}")
                else:
                    st.session_state.uploaded_benchmark_manifest = {
                        **uploaded_bundle,
                        "display_name": (
                            f"uploaded::{Path(uploaded_zip.name).stem} "
                            f"[{uploaded_bundle['label_count']} labels / {uploaded_bundle['image_count']} images]"
                        ),
                    }
                    st.rerun()
        with upload_actions[1]:
            if st.button("Forget Uploaded Benchmark Set", width="stretch", key="clear-uploaded-benchmark"):
                st.session_state.uploaded_benchmark_manifest = None
                st.rerun()

        if not manifest_entries:
            st.info("No manifest directories were found under `data/`. Add labels.json plus train/val/test CSV manifests to enable in-app benchmarking.")
        else:
            manifest_labels = [item["display_name"] for item in manifest_entries]
            selected_manifest_label = st.selectbox("Benchmark dataset", manifest_labels, key="benchmark-manifest")
            selected_manifest = manifest_entries[manifest_labels.index(selected_manifest_label)]

            benchmark_left, benchmark_right = st.columns(2)
            with benchmark_left:
                benchmark_split = st.selectbox("Benchmark split", ["test", "val", "train"], key="benchmark-split")
                max_examples = st.number_input(
                    "Max examples (0 = full split)",
                    min_value=0,
                    max_value=5000,
                    value=250,
                    step=50,
                    key="benchmark-max-examples",
                )
            with benchmark_right:
                checkpoint_options = {model["display_name"]: model["checkpoint_path"] for model in available_models}
                default_selection = list(checkpoint_options.keys())[: min(2, len(checkpoint_options))]
                selected_checkpoints = st.multiselect(
                    "Checkpoints to compare",
                    list(checkpoint_options.keys()),
                    default=default_selection,
                    key="benchmark-checkpoints",
                )
                st.caption(
                    f"Manifest labels: {selected_manifest['label_count']} | Counts: {selected_manifest.get('counts', {})}"
                )
                class_counts = selected_manifest.get("class_counts", {}) or {}
                if class_counts:
                    smallest_label = min(class_counts, key=class_counts.get)
                    largest_label = max(class_counts, key=class_counts.get)
                    st.caption(
                        f"Class balance: smallest={smallest_label} ({class_counts[smallest_label]}) | "
                        f"largest={largest_label} ({class_counts[largest_label]})"
                    )
                if str(selected_manifest.get("display_name", "")).startswith("uploaded::"):
                    st.caption("Uploaded benchmark sets are best evaluated on the `test` split because train/val were mirrored from the uploaded sample.")
                elif selected_manifest.get("benchmark_mode") == "standard":
                    st.caption("Prefer curated subsets for headline comparisons when the full dataset is heavily imbalanced.")

            if st.button(
                "Run Checkpoint Benchmark",
                type="primary",
                width="stretch",
                disabled=not selected_checkpoints,
            ):
                try:
                    benchmark_results = compare_checkpoints_on_manifest(
                        checkpoint_paths=[checkpoint_options[label] for label in selected_checkpoints],
                        manifest_dir=selected_manifest["manifest_dir"],
                        split=benchmark_split,
                        max_examples=None if max_examples == 0 else int(max_examples),
                    )
                except Exception as exc:
                    st.error(f"Benchmarking failed. Details: {exc}")
                else:
                    st.session_state.model_benchmark_bundle = {
                        "manifest_dir": selected_manifest["manifest_dir"],
                        "split": benchmark_split,
                        "max_examples": int(max_examples),
                        "results": benchmark_results,
                    }
                    st.rerun()

            benchmark_bundle = st.session_state.get("model_benchmark_bundle")
            if benchmark_bundle:
                st.caption(
                    f"Latest benchmark: {benchmark_bundle['manifest_dir']} | split={benchmark_bundle['split']} | max_examples={benchmark_bundle['max_examples']}"
                )
                benchmark_rows = [
                    {
                        "model_name": result["model_name"],
                        "architecture": result["architecture"],
                        "accuracy": round(float(result.get("accuracy", 0) or 0), 3),
                        "macro_f1": round(float(result.get("macro_f1", 0) or 0), 3),
                        "weighted_f1": round(float(result.get("weighted_f1", 0) or 0), 3),
                        "loss": round(float(result.get("loss", 0) or 0), 3),
                        "evaluated_examples": result.get("evaluated_examples", 0),
                        "checkpoint_path": result["checkpoint_path"],
                    }
                    for result in benchmark_bundle.get("results", [])
                ]
                st.dataframe(benchmark_rows, width="stretch")

                inspected_result_name = st.selectbox(
                    "Inspect benchmark result",
                    [result["model_name"] for result in benchmark_bundle.get("results", [])],
                    key="benchmark-result-selection",
                )
                inspected_result = next(
                    result
                    for result in benchmark_bundle.get("results", [])
                    if result["model_name"] == inspected_result_name
                )
                inspected_rows = classification_report_rows(inspected_result)
                if inspected_rows:
                    inspect_left, inspect_right = st.columns(2)
                    with inspect_left:
                        st.markdown("### Benchmark Strongest Classes")
                        st.dataframe(
                            sorted(inspected_rows, key=lambda row: row["f1_score"], reverse=True)[:5],
                            width="stretch",
                        )
                    with inspect_right:
                        st.markdown("### Benchmark Weakest Classes")
                        st.dataframe(
                            sorted(inspected_rows, key=lambda row: row["f1_score"])[:5],
                            width="stretch",
                        )

                st.download_button(
                    "Download Benchmark CSV",
                    data=analyses_to_csv(benchmark_rows),
                    file_name="fabrisense-benchmark-results.csv",
                    mime="text/csv",
                    width="stretch",
                )

    review_summary = [
        {
            "timestamp": item.get("timestamp", ""),
            "image_name": item.get("image_name", ""),
            "predicted_label": item.get("predicted_label", ""),
            "corrected_label": item.get("corrected_label", ""),
            "confidence": item.get("confidence", 0),
            "model_name": item.get("model_name", ""),
            "architecture": item.get("architecture", ""),
        }
        for item in reviews
    ]
    st.markdown("### Review Feedback Loop")
    if not review_summary:
        st.info("No manual model reviews have been saved yet. Save corrections from trained-model runs to build a feedback loop.")
    else:
        summary_left, summary_right = st.columns(2)
        with summary_left:
            render_key_value_block(
                "Review Summary",
                {
                    "Saved Reviews": len(review_summary),
                    "Distinct Predicted Labels": len({item["predicted_label"] for item in review_summary if item["predicted_label"]}),
                    "Distinct Corrected Labels": len({item["corrected_label"] for item in review_summary if item["corrected_label"]}),
                    "Latest Review": review_summary[0]["timestamp"],
                },
            )
        with summary_right:
            st.download_button(
                "Download Review Log CSV",
                data=analyses_to_csv(review_summary),
                file_name="fabrisense-model-reviews.csv",
                mime="text/csv",
                width="stretch",
            )
            if st.button("Clear Review Log", width="stretch"):
                MODEL_REVIEWS.clear()
                st.rerun()
        st.dataframe(review_summary, width="stretch")


def render_about_page() -> None:
    render_page_intro(
        "PLATFORM OVERVIEW",
        "FabriSense combines visual fabric reading with presentation-ready output.",
        "The app is designed for designers, textile learners, sellers, and merchandisers who need a polished way to translate fabric imagery into useful product language.",
    )
    landing_asset = load_json_asset("assets/lottie_fabric.json")
    left, right = st.columns((0.7, 1.3))
    with left:
        if landing_asset:
            st_lottie(landing_asset, height=260, key="fabric-animation")
    with right:
        render_key_value_block(
            "How It Works",
            {
                "Input": "A textile image from upload or sample library.",
                "Core Processing": "Image preparation, palette extraction, and either local or AI-generated interpretation.",
                "Outputs": "Material summary, comparison view, batch export, and downloadable PDF report.",
                "Best Use": "Presentations, educational demos, catalog review, and exploratory textile analysis workflows.",
            },
        )

