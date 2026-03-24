"""Page-level rendering for the FabriSense app."""

from __future__ import annotations

from html import escape as html_escape
from pathlib import Path
from typing import Any, Dict

import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie

from src.analyzer import FabricAnalyzer
from src.history_store import HistoryStore
from src.image_preprocessor import ImagePreprocessor
from src.report_generator import ReportGenerator
from src.utils import (
    analyses_to_csv,
    compare_fabric_analyses,
    format_analysis_for_display,
    get_random_fun_fact,
    history_entry_from_summary,
    load_json_asset,
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

MODE_LABELS = {
    "AI-generated": "ai",
    "Local Analysis": "local",
}

HISTORY = HistoryStore()


def _engine_label(metadata: Dict[str, Any]) -> str:
    return "AI-generated" if metadata.get("analysis_mode") == "ai" else "Local heuristics"


def _safe_text(value: Any) -> str:
    return html_escape("" if value is None else str(value), quote=True)


def render_home_page() -> None:
    render_hero()
    render_feature_strip()

    mode_label = st.radio("Analysis Mode", ["AI-generated", "Local Analysis"], horizontal=True)
    analysis_mode = MODE_LABELS[mode_label]

    if analysis_mode == "local":
        render_highlight_banner(
            "Local-first workflow",
            "Run a fast baseline material read without API keys. This mode is best for demos, privacy-sensitive work, and no-network usage.",
        )
    else:
        render_highlight_banner(
            "AI-generated workflow",
            "Use the guided model path when you want richer summary language, cleaner reasoning, and a more editorial material brief.",
        )

    sample_choice = render_sample_gallery("assets/sample_fabrics", state_key="home_selected_sample")
    upload_choice = render_upload_panel(
        title="Material Input",
        prompt="Drop a close-up or flat-lay textile image for analysis",
    )
    choice = upload_choice or sample_choice

    if choice is None:
        st.info("Choose a curated sample or upload an image to start a material read.")
        return

    image, image_name = choice
    button_label = "Run Local Analysis" if analysis_mode == "local" else "Generate AI Brief"
    if st.button(button_label, type="primary", use_container_width=True):
        _run_analysis(image=image, image_name=image_name, analysis_mode=analysis_mode)


def _run_analysis(image, image_name: str, analysis_mode: str) -> None:
    with st.container():
        loading_asset = load_json_asset("assets/lottie_loading.json")
        if loading_asset:
            st_lottie(loading_asset, height=140, key="loading-animation")
        st.markdown(f"<div class='loading-card'>{get_random_fun_fact()}</div>", unsafe_allow_html=True)
        spinner_text = "Running local vision heuristics..." if analysis_mode == "local" else "Building an AI-generated material brief..."
        with st.spinner(spinner_text):
            try:
                analyzer = FabricAnalyzer()
                analysis = analyzer.analyze(image, mode=analysis_mode)
            except Exception as exc:
                prefix = "Local analysis failed." if analysis_mode == "local" else "AI-generated analysis failed. Check your `.env` configuration."
                st.error(f"{prefix} Details: {exc}")
                return

            report_bytes = None
            try:
                report_bytes = ReportGenerator().generate_pdf(analysis, image)
            except Exception as exc:
                st.warning(f"Analysis completed, but PDF generation is unavailable. Details: {exc}")

    summary = summarize_analysis(analysis, image_name)
    HISTORY.append(history_entry_from_summary(summary))
    st.session_state.analysis = analysis
    st.session_state.report_bytes = report_bytes
    st.session_state.image = image
    st.session_state.image_name = image_name
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

    left, right = st.columns((0.95, 1.05))
    with left:
        st.image(image, caption=image_name, use_container_width=True)
        if report_bytes:
            st.download_button(
                "Download PDF Report",
                data=report_bytes,
                file_name=f"{image_name.rsplit('.', 1)[0]}-fabrisense-report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        if st.button("Start New Analysis", use_container_width=True):
            st.session_state.analysis = None
            st.session_state.report_bytes = None
            st.session_state.image = None
            st.session_state.image_name = None
            st.rerun()

    with right:
        llm = analysis.get("llm_analysis", {})
        fabric = llm.get("fabric_type", {})
        pattern = llm.get("pattern", {})
        texture = llm.get("texture", {})
        quality = llm.get("quality_assessment", {})
        care = llm.get("care_instructions", {})
        season = llm.get("season_recommendation", {})
        price = llm.get("price_range", {})
        sustainability = llm.get("sustainability", {})

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

        render_key_value_block(
            "Commercial Fit",
            {
                "Best Seasons": ", ".join(season.get("best_seasons", []) or ["N/A"]),
                "Avoid Seasons": ", ".join(season.get("avoid_seasons", []) or ["N/A"]),
                "Breathability": season.get("breathability", "N/A"),
                "Price Tier": price.get("category", "N/A"),
                "USD Range": price.get("estimated_per_meter_usd", "N/A"),
                "Value": price.get("value_for_money", "N/A"),
                "Eco Score": sustainability.get("eco_score", "N/A"),
                "Impact": sustainability.get("environmental_impact", "N/A"),
            },
        )

    palette = analysis.get("color_palette", {})
    render_color_palette(palette.get("colors", []), palette.get("harmony_type", "Unknown"))

    row_a, row_b = st.columns(2)
    with row_a:
        render_list_block("Quality Factors", quality.get("factors", []))
        render_list_block(
            "Occasion Suitability",
            [
                f"{item.get('occasion', 'N/A')} ({item.get('suitability_score', 'N/A')}/10): {item.get('note', 'N/A')}"
                for item in llm.get("occasion_suitability", [])
            ],
        )
        render_list_block(
            "Styling Suggestions",
            [
                f"{item.get('garment', 'N/A')}: {item.get('style', 'N/A')} for {item.get('target_audience', 'N/A')}"
                for item in llm.get("styling_suggestions", [])
            ],
        )

    with row_b:
        interior = llm.get("interior_use", {})
        render_list_block("Interior Uses", interior.get("suggestions", []))
        render_key_value_block(
            "Narrative Summary",
            {
                "Overall Summary": llm.get("overall_summary", "N/A"),
                "Fun Fact": llm.get("fun_fact", "N/A"),
                "Interior Notes": interior.get("notes", "N/A"),
                "Sustainability Notes": sustainability.get("notes", "N/A"),
            },
        )


def render_batch_page() -> None:
    render_page_intro(
        "MULTI-ITEM WORKFLOW",
        "Analyze a batch of fabric images in one run.",
        "Use batch mode to review seller catalogs, classroom submissions, or sourcing references and export the summary as CSV.",
    )
    mode_label = st.radio("Batch Mode", ["AI-generated", "Local Analysis"], horizontal=True, key="batch_mode")
    analysis_mode = MODE_LABELS[mode_label]

    if analysis_mode == "local":
        render_highlight_banner(
            "Fast catalog pass",
            "Local batch mode is the best fit for quick sorting, tagging, and review of many images at once.",
        )
    else:
        render_highlight_banner(
            "AI-generated batch run",
            "Use the AI path when the batch needs stronger descriptive language and a more refined brief per image.",
        )

    files = st.file_uploader(
        "Upload multiple fabric images",
        type=sorted(ImagePreprocessor.SUPPORTED_FORMATS),
        accept_multiple_files=True,
        key="batch_upload",
    )

    if files and st.button("Run Batch Analysis", type="primary", use_container_width=True):
        _run_batch_analysis(files, analysis_mode)

    bundle = st.session_state.batch_bundle
    if not bundle:
        st.info("Upload several textile images to generate a batch summary and CSV export.")
        return

    rows = bundle["rows"]
    st.caption(f"Batch size: {len(rows)} | Mode: {bundle['analysis_mode']} | Engine: {bundle['engine']}")
    st.download_button(
        "Download Batch CSV",
        data=analyses_to_csv(rows),
        file_name="fabrisense-batch-summary.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.dataframe(rows, use_container_width=True)

    for item in bundle["details"]:
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
                    "Summary": item["summary"],
                },
            )


def _run_batch_analysis(files: list[Any], analysis_mode: str) -> None:
    loading_asset = load_json_asset("assets/lottie_loading.json")
    if loading_asset:
        st_lottie(loading_asset, height=120, key="batch-loading")
    st.markdown(f"<div class='loading-card'>{get_random_fun_fact()}</div>", unsafe_allow_html=True)

    rows = []
    details = []
    with st.spinner("Running batch analysis across uploaded materials..."):
        analyzer = FabricAnalyzer()
        for uploaded in files:
            valid, message = ImagePreprocessor.validate_image(uploaded)
            if not valid:
                rows.append(
                    {
                        "timestamp": "",
                        "image_name": getattr(uploaded, "name", "unknown"),
                        "mode": analysis_mode,
                        "engine": "Error",
                        "fabric": "Invalid image",
                        "pattern": message,
                        "texture": "",
                        "weight": "",
                        "dominant_color": "",
                        "quality_score": 0,
                        "price_tier": "",
                        "best_seasons": "",
                        "summary": "Validation failed before analysis.",
                    }
                )
                continue

            try:
                image = ImagePreprocessor.load_image(uploaded)
                analysis = analyzer.analyze(image, mode=analysis_mode)
                row = summarize_analysis(analysis, uploaded.name)
                rows.append(row)
                details.append(row)
                HISTORY.append(history_entry_from_summary(row))
            except Exception as exc:
                rows.append(
                    {
                        "timestamp": "",
                        "image_name": getattr(uploaded, "name", "unknown"),
                        "mode": analysis_mode,
                        "engine": "Error",
                        "fabric": "Analysis failed",
                        "pattern": str(exc),
                        "texture": "",
                        "weight": "",
                        "dominant_color": "",
                        "quality_score": 0,
                        "price_tier": "",
                        "best_seasons": "",
                        "summary": "This file failed during analysis, but the batch continued.",
                    }
                )

    st.session_state.batch_bundle = {
        "rows": rows,
        "details": details,
        "analysis_mode": analysis_mode,
        "engine": "AI-generated" if analysis_mode == "ai" else "Local heuristics",
    }
    st.rerun()


def render_compare_page() -> None:
    render_page_intro(
        "SIDE-BY-SIDE REVIEW",
        "Compare two materials in one workspace.",
        "Use the comparison view to separate fabric family, pattern direction, palette shifts, and visual quality without jumping between tabs.",
    )

    mode_label = st.radio("Comparison Mode", ["AI-generated", "Local Analysis"], horizontal=True, key="compare_mode")
    analysis_mode = MODE_LABELS[mode_label]

    if analysis_mode == "local":
        render_highlight_banner(
            "Fast comparison mode",
            "No API setup required. Compare textile structure, color, and quality heuristics immediately.",
        )
    else:
        render_highlight_banner(
            "AI-generated comparison",
            "Use the guided AI path when you want more interpretive differences in material description and commercial framing.",
        )

    left, right = st.columns(2)
    with left:
        image_a, name_a = _render_compare_input("Material A", "compare_a")
    with right:
        image_b, name_b = _render_compare_input("Material B", "compare_b")

    if image_a is not None and image_b is not None:
        button_label = "Run Local Comparison" if analysis_mode == "local" else "Generate Comparison"
        if st.button(button_label, type="primary", use_container_width=True):
            _run_comparison(image_a, name_a, image_b, name_b, analysis_mode)

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

    if st.button("Clear Comparison", use_container_width=True):
        st.session_state.comparison_bundle = None
        st.rerun()


def _run_comparison(
    image_a: Image.Image,
    name_a: str,
    image_b: Image.Image,
    name_b: str,
    analysis_mode: str,
) -> None:
    loading_asset = load_json_asset("assets/lottie_loading.json")
    if loading_asset:
        st_lottie(loading_asset, height=120, key="comparison-loading")
    st.markdown(f"<div class='loading-card'>{get_random_fun_fact()}</div>", unsafe_allow_html=True)

    spinner_text = "Comparing local texture and color signals..." if analysis_mode == "local" else "Building an AI-generated side-by-side review..."
    with st.spinner(spinner_text):
        try:
            analyzer = FabricAnalyzer()
            analysis_a = analyzer.analyze(image_a, mode=analysis_mode)
            analysis_b = analyzer.analyze(image_b, mode=analysis_mode)
            summary = compare_fabric_analyses(analysis_a, name_a, analysis_b, name_b)
        except Exception as exc:
            prefix = "Local comparison failed." if analysis_mode == "local" else "AI-generated comparison failed. Check your `.env` configuration."
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
        st.image(ImagePreprocessor.resize_for_display(image), caption=name, use_container_width=True)

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
        use_container_width=True,
    )
    if st.button("Clear History", use_container_width=True):
        HISTORY.clear()
        st.rerun()

    st.dataframe(history, use_container_width=True)


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

