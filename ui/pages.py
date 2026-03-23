"""Page-level rendering for the FabriSense app."""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st
from streamlit_lottie import st_lottie

from src.analyzer import FabricAnalyzer
from src.color_extractor import ColorExtractor
from src.image_preprocessor import ImagePreprocessor
from src.report_generator import ReportGenerator
from src.utils import format_analysis_for_display, get_random_fun_fact, load_json_asset
from ui.components import (
    render_color_palette,
    render_feature_strip,
    render_hero,
    render_key_value_block,
    render_list_block,
    render_metric_band,
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
    "AI Deep Analysis": "ai",
    "Local Analysis": "local",
}


def render_home_page() -> None:
    render_hero()
    render_feature_strip()
    st.write("")

    mode_label = st.radio("Analysis Mode", ["AI Deep Analysis", "Local Analysis"], horizontal=True)
    analysis_mode = MODE_LABELS[mode_label]

    if analysis_mode == "local":
        st.info(
            "Local Analysis runs fully inside the app with computer-vision heuristics. "
            "It does not require API keys and is best for fast baseline analysis."
        )
    else:
        st.caption("AI Deep Analysis uses Gemini, OpenAI, or Ollama for richer textile reasoning.")

    sample_choice = render_sample_gallery("assets/sample_fabrics")
    upload_choice = render_upload_panel()
    choice = upload_choice or sample_choice

    provider = None
    if analysis_mode == "ai":
        provider = st.selectbox("Model provider", ["gemini", "openai", "ollama"], index=0)

    if choice is None:
        st.info("Upload a fabric image or select a sample to begin.")
        return

    image, image_name = choice
    button_label = "Run Local Analysis" if analysis_mode == "local" else "Analyze Fabric"
    if st.button(button_label, type="primary", use_container_width=True):
        _run_analysis(image=image, image_name=image_name, provider=provider, analysis_mode=analysis_mode)


def _run_analysis(image, image_name: str, provider: str | None, analysis_mode: str) -> None:
    with st.container():
        loading_asset = load_json_asset("assets/lottie_loading.json")
        if loading_asset:
            st_lottie(loading_asset, height=140, key="loading-animation")
        st.markdown(f"<div class='loading-card'>{get_random_fun_fact()}</div>", unsafe_allow_html=True)
        spinner_text = "Running local vision heuristics..." if analysis_mode == "local" else "Inspecting weave, color, and fabric cues..."
        with st.spinner(spinner_text):
            try:
                analyzer = FabricAnalyzer(llm_provider=provider)
                analysis = analyzer.analyze(image, mode=analysis_mode)
                report_bytes = ReportGenerator().generate_pdf(analysis, image)
            except Exception as exc:
                prefix = "Local analysis failed." if analysis_mode == "local" else "Analysis failed. Check your `.env` provider credentials or local Ollama setup."
                st.error(f"{prefix} Details: {exc}")
                return

    st.session_state.analysis = analysis
    st.session_state.report_bytes = report_bytes
    st.session_state.image = image
    st.session_state.image_name = image_name
    st.rerun()


def render_results_page(analysis: Dict[str, Any], report_bytes: bytes | None, image, image_name: str) -> None:
    metadata = analysis.get("analysis_metadata", {})
    st.markdown("## Analysis Results")
    st.caption(
        f"Mode: {metadata.get('analysis_mode', 'unknown')} | Engine: {metadata.get('model_used', 'unknown')} | "
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
            "Fabric Snapshot",
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


def render_color_lab_page() -> None:
    st.markdown("## Color Lab")
    st.write("Use Color Lab when you only want the dominant palette and fabric image metadata without a live LLM call.")

    upload = render_upload_panel()
    if upload is None:
        st.info("Upload an image to extract its color palette locally.")
        return

    image, image_name = upload
    extractor = ColorExtractor(n_colors=6)
    palette = extractor.extract_palette(image)
    harmony = extractor.get_color_harmony(palette)
    info = ImagePreprocessor.get_image_info(image)

    left, right = st.columns((0.9, 1.1))
    with left:
        st.image(image, caption=image_name, use_container_width=True)
    with right:
        render_key_value_block(
            "Image Details",
            {
                "Width": info.get("width", "N/A"),
                "Height": info.get("height", "N/A"),
                "Mode": info.get("mode", "N/A"),
                "Aspect Ratio": info.get("aspect_ratio", "N/A"),
                "Harmony": harmony,
            },
        )

    render_color_palette(palette, harmony)


def render_fabric_guide_page() -> None:
    st.markdown("## Fabric Guide")
    st.write("A compact reference view for common textile families and the tradeoffs they usually bring.")

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
    st.markdown("## Care Guide")
    st.write("Quick handling defaults for common fabrics. Real garments can override these with trim, dye, or finishing requirements.")
    st.table(CARE_GUIDE)

    st.markdown("### Quick Rules")
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
    landing_asset = load_json_asset("assets/lottie_fabric.json")
    left, right = st.columns((0.7, 1.3))
    with left:
        if landing_asset:
            st_lottie(landing_asset, height=260, key="fabric-animation")
    with right:
        st.markdown("## About FabriSense")
        st.write(
            "FabriSense combines a vision-capable LLM with local image processing to turn a fabric image "
            "into a structured textile brief. The app is aimed at design teams, textile students, sellers, "
            "and decorators who need fast descriptive analysis from a single image."
        )
        st.write(
            "The pipeline preprocesses the image, extracts a computer-vision color palette, calls the selected "
            "LLM provider for structured analysis, and packages the result into an on-screen dashboard plus PDF report."
        )
