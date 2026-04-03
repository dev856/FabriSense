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
from ui.styles import APP_CSS


NAV_ITEMS = {
    "Analyze": "analyze",
    "Batch Analysis": "batch",
    "Compare Fabrics": "compare",
    "History": "history",
    "Fabric Guide": "guide",
    "Care Guide": "care",
    "Models": "models",
    "About": "about",
}

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
}


def _initialize_session_state() -> None:
    for key, default_value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def _render_sidebar_navigation() -> str:
    with st.sidebar:
        render_sidebar_brand()
        selected_page = st.radio("Navigate", list(NAV_ITEMS.keys()), label_visibility="collapsed")
        st.caption("Built for designers, textile students, sellers, and presentation-ready product demos.")
    return NAV_ITEMS[selected_page]


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
        page_icon=str(Path("assets/favicon.ico")) if Path("assets/favicon.ico").exists() else None,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(APP_CSS, unsafe_allow_html=True)
    _initialize_session_state()

    page_id = _render_sidebar_navigation()
    _render_selected_page(page_id)


if __name__ == "__main__":
    main()
