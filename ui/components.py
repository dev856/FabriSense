"""Reusable Streamlit UI components."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

import streamlit as st
from PIL import Image

from src.image_preprocessor import ImagePreprocessor


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero-shell">
            <div class="hero-copy">
                <p class="eyebrow">AI FABRIC ANALYZER</p>
                <h1>Turn a fabric photo into a detailed textile brief.</h1>
                <p class="hero-text">
                    Identify likely fabric type, pattern, texture, colors, care guidance,
                    styling direction, and a downloadable report from one image.
                </p>
            </div>
            <div class="hero-stats">
                <div class="stat-card"><span>6</span><small>dominant colors extracted</small></div>
                <div class="stat-card"><span>3</span><small>provider modes supported</small></div>
                <div class="stat-card"><span>1</span><small>report export flow</small></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_feature_strip() -> None:
    cols = st.columns(4)
    items = [
        ("Fabric Type", "Blend and subtype estimation"),
        ("Pattern Detail", "Print scale and repeat interpretation"),
        ("Color Palette", "Dominant swatches and harmony"),
        ("Report Export", "Downloadable PDF summary"),
    ]
    for col, (title, body) in zip(cols, items):
        with col:
            st.markdown(f"<div class='info-card'><h3>{title}</h3><p>{body}</p></div>", unsafe_allow_html=True)


def render_sample_gallery(sample_dir: str | Path) -> Optional[Tuple[Image.Image, str]]:
    sample_root = Path(sample_dir)
    sample_paths = sorted(sample_root.glob("*.jpg"))
    if not sample_paths:
        return None

    st.markdown("### Demo Samples")
    cols = st.columns(len(sample_paths))
    chosen: Optional[Tuple[Image.Image, str]] = None
    for col, path in zip(cols, sample_paths):
        with col:
            st.image(str(path), use_container_width=True)
            label = path.stem.replace("_", " ").title()
            if st.button(f"Use {label}", key=f"sample-{path.stem}", use_container_width=True):
                chosen = (Image.open(path).convert("RGB"), path.name)
    return chosen


def render_upload_panel() -> Optional[Tuple[Image.Image, str]]:
    st.markdown("### Upload Fabric Image")
    uploaded = st.file_uploader(
        "Upload a close-up or flat-lay textile image",
        type=sorted(ImagePreprocessor.SUPPORTED_FORMATS),
        accept_multiple_files=False,
    )
    if uploaded is None:
        return None

    valid, message = ImagePreprocessor.validate_image(uploaded)
    if not valid:
        st.error(message)
        return None

    image = ImagePreprocessor.load_image(uploaded)
    st.caption(message)
    st.image(ImagePreprocessor.resize_for_display(image), caption=uploaded.name, use_container_width=True)
    return image, uploaded.name


def render_metric_band(metrics: Dict[str, Any]) -> None:
    cols = st.columns(4)
    cards = [
        ("Quality", f"{metrics['score']}/10"),
        ("Rating", metrics["stars"]),
        ("Best Seasons", metrics["seasons"]),
        ("Eco Score", str(metrics["eco_score"])),
    ]
    for col, (title, value) in zip(cols, cards):
        with col:
            st.markdown(
                f"<div class='metric-card'><p>{title}</p><h3>{value}</h3></div>",
                unsafe_allow_html=True,
            )


def render_color_palette(colors: Iterable[Dict[str, Any]], harmony: str) -> None:
    st.markdown(f"### Color Palette  |  Harmony: `{harmony}`")
    cols = st.columns(3)
    for index, color in enumerate(colors):
        with cols[index % 3]:
            swatch = color["hex"]
            st.markdown(
                f"""
                <div class="color-card">
                    <div class="swatch" style="background:{swatch};"></div>
                    <div>
                        <h4>{color['name']}</h4>
                        <p>{swatch} • {color['percentage']}%</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_key_value_block(title: str, rows: Dict[str, Any]) -> None:
    st.markdown(f"### {title}")
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    for label, value in rows.items():
        st.markdown(f"**{label}**  \n{value}")
    st.markdown("</div>", unsafe_allow_html=True)


def render_list_block(title: str, items: Iterable[str]) -> None:
    st.markdown(f"### {title}")
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    values = list(items)
    if not values:
        st.write("No data available.")
    else:
        for item in values:
            st.write(f"- {item}")
    st.markdown("</div>", unsafe_allow_html=True)
