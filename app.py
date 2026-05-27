from pathlib import Path

import streamlit as st

from ui.components import render_sidebar_brand
from ui.pages import (
    render_about_page,
    render_batch_page,
    render_care_guide_page,
    render_compare_page,
    render_fabric_guide_page,
    render_history_page,
    render_home_page,
    render_model_info_page,
    render_results_page,
)
from ui.styles import APP_CSS, get_dynamic_theme_css

NAV_ICONS = [
    "search",
    "grid",
    "compare",
    "clock",
    "guide",
    "spark",
    "model",
    "info",
]
NAV_LABELS = [
    "Analyze",
    "Batch Analysis",
    "Compare",
    "History",
    "Guide",
    "Care",
    "Models",
    "About",
]
NAV_IDS = ["analyze", "batch", "compare", "history", "guide", "care", "models", "about"]

SESSION_DEFAULTS = {
    "analysis": None,
    "report_bytes": None,
    "image": None,
    "image_name": None,
    "comparison_bundle": None,
    "batch_bundle": None,
    "model_benchmark_bundle": None,
    "uploaded_benchmark_manifest": None,
    "home_selected_sample": None,
    "nav_page": "analyze",
}


def _initialize_session_state() -> None:
    for key, default_value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def _apply_dynamic_theme() -> None:
    if st.session_state.get("analysis"):
        palette = st.session_state.analysis.get("color_palette", {})
        dominant = palette.get("dominant_color", {})
        if dominant and dominant.get("hex"):
            hex_color = dominant.get("hex")
            dynamic_css = get_dynamic_theme_css(hex_color)
            st.markdown(dynamic_css, unsafe_allow_html=True)


def _render_sidebar_navigation() -> str:
    with st.sidebar:
        render_sidebar_brand()
        options = [
            "Analyze",
            "Batch",
            "Compare",
            "History",
            "Guide",
            "Care",
            "Models",
            "About",
        ]
        selected = st.radio(
            "Navigate",
            options,
            label_visibility="collapsed",
            index=NAV_IDS.index(st.session_state.get("nav_page", "analyze")),
        )
        page_id = NAV_IDS[options.index(selected)]
        if page_id != st.session_state.get("nav_page"):
            st.session_state.nav_page = page_id
            st.rerun()
    return page_id


def _render_selected_page(page_id: str) -> None:
    if page_id == "analyze":
        render_home_page()
        if st.session_state.analysis and st.session_state.image is not None:
            st.divider()
            render_results_page(
                analysis=st.session_state.analysis,
                report_bytes=st.session_state.report_bytes,
                image=st.session_state.image,
                image_name=st.session_state.image_name or "fabric-image",
            )
        return

    page_renderers = {
        "batch": render_batch_page,
        "compare": render_compare_page,
        "history": render_history_page,
        "guide": render_fabric_guide_page,
        "care": render_care_guide_page,
        "models": render_model_info_page,
        "about": render_about_page,
    }
    page_renderers[page_id]()


def main() -> None:
    st.set_page_config(
        page_title="FabriSense",
        page_icon=str(Path("assets/favicon.ico"))
        if Path("assets/favicon.ico").exists()
        else None,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(APP_CSS, unsafe_allow_html=True)
    _initialize_session_state()
    _apply_dynamic_theme()

    page_id = _render_sidebar_navigation()
    _render_selected_page(page_id)


if __name__ == "__main__":
    main()
