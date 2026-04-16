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
from ui.styles import APP_CSS, DARK_MODE_CSS

NAV_ICONS = [
    "search",
    "layers",
    "arrow-left-right",
    "clock-history",
    "book",
    "flower1",
    "cpu",
    "info-circle",
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
    "dark_mode": False,
    "nav_page": "analyze",
}


def _initialize_session_state() -> None:
    for key, default_value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def _apply_dark_mode() -> None:
    if st.session_state.get("dark_mode"):
        st.markdown(DARK_MODE_CSS, unsafe_allow_html=True)


def _render_sidebar_navigation() -> str:
    with st.sidebar:
        render_sidebar_brand()
        dark_mode = bool(st.session_state.get("dark_mode", False))
        nav_styles = {
            "container": {
                "padding": "0 !important",
                "background-color": "transparent",
            },
            "icon": {
                "color": "#e8a07a" if dark_mode else "#bb6c3f",
                "font-size": "16px",
                "padding-right": "8px",
            },
            "nav-link": {
                "padding": "0.6rem 0.9rem",
                "margin": "0 0 0.3rem 0",
                "border-radius": "22px",
                "font-size": "0.92rem",
                "font-weight": "600",
                "color": "#c5cdd6" if dark_mode else "#243240",
                "background-color": "transparent",
                "border": "1px solid transparent",
                "transition": "all 200ms ease",
                "--hover-color": "rgba(212,136,92,0.10)"
                if dark_mode
                else "rgba(187,108,63,0.08)",
            },
            "nav-link-selected": {
                "background-color": "rgba(212,136,92,0.18)"
                if dark_mode
                else "rgba(187,108,63,0.14)",
                "font-weight": "800",
                "color": "#e8a07a" if dark_mode else "#9d5630",
                "border": "1px solid rgba(212,136,92,0.5)"
                if dark_mode
                else "1px solid rgba(187,108,63,0.35)",
                "box-shadow": "0 4px 16px rgba(0,0,0,0.18)"
                if dark_mode
                else "0 4px 16px rgba(187,108,63,0.10)",
            },
        }
        try:
            from streamlit_option_menu import option_menu

            selected = option_menu(
                None,
                NAV_LABELS,
                icons=NAV_ICONS,
                menu_icon=None,
                default_index=NAV_IDS.index(
                    st.session_state.get("nav_page", "analyze")
                ),
                key="nav_menu",
                styles=nav_styles,
            )
        except ImportError:
            selected = st.radio(
                "Navigate",
                NAV_LABELS,
                label_visibility="collapsed",
                index=NAV_IDS.index(st.session_state.get("nav_page", "analyze")),
            )
        st.divider()
        st.toggle(
            "\U0001f319 Dark Mode",
            key="dark_mode",
        )
        page_id = NAV_IDS[NAV_LABELS.index(selected)]
        if page_id != st.session_state.get("nav_page", "analyze"):
            st.session_state.nav_page = page_id
            st.rerun()
        st.caption(
            "Built for designers, textile students, sellers, and presentation-ready product demos."
        )
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
    _apply_dark_mode()

    page_id = _render_sidebar_navigation()
    _render_selected_page(page_id)


if __name__ == "__main__":
    main()
