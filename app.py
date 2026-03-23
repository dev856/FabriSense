from pathlib import Path

import streamlit as st

from ui.components import render_sidebar_brand
from ui.pages import (
    render_about_page,
    render_care_guide_page,
    render_compare_page,
    render_fabric_guide_page,
    render_home_page,
    render_results_page,
)
from ui.styles import APP_CSS


NAV_ITEMS = [
    "Analyze",
    "Compare Fabrics",
    "Fabric Guide",
    "Care Guide",
    "About",
]


def main() -> None:
    st.set_page_config(
        page_title="FabriSense",
        page_icon=str(Path("assets/favicon.ico")) if Path("assets/favicon.ico").exists() else None,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(APP_CSS, unsafe_allow_html=True)

    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    if "report_bytes" not in st.session_state:
        st.session_state.report_bytes = None
    if "image" not in st.session_state:
        st.session_state.image = None
    if "image_name" not in st.session_state:
        st.session_state.image_name = None
    if "comparison_bundle" not in st.session_state:
        st.session_state.comparison_bundle = None

    with st.sidebar:
        render_sidebar_brand()
        page = st.radio("Navigate", NAV_ITEMS, label_visibility="collapsed")
        st.caption("Built for designers, textile students, sellers, and presentation-ready product demos.")

    if page == "Analyze":
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

    if page == "Compare Fabrics":
        render_compare_page()
        return

    if page == "Fabric Guide":
        render_fabric_guide_page()
        return

    if page == "Care Guide":
        render_care_guide_page()
        return

    render_about_page()


if __name__ == "__main__":
    main()