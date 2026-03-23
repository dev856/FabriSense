"""Reusable Streamlit UI components."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

import streamlit as st
from PIL import Image

from src.image_preprocessor import ImagePreprocessor


def render_sidebar_brand() -> None:
    st.markdown(
        """
        <div class="sidebar-brand-card">
            <p class="sidebar-kicker">FABRISENSE STUDIO</p>
            <h3>Commercial textile reads in one polished workspace.</h3>
            <p>Switch between local material heuristics and AI-generated reporting without exposing model internals.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_intro(kicker: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <section class="page-intro">
            <p class="eyebrow">{kicker}</p>
            <h2>{title}</h2>
            <p class="page-intro-text">{body}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero-shell">
            <div class="hero-copy">
                <p class="eyebrow">TEXTILE INTELLIGENCE</p>
                <h1>Turn a fabric image into a sharp, presentation-ready material brief.</h1>
                <p class="hero-text">
                    FabriSense blends visual fabric reading, side-by-side comparison, and PDF-ready reporting in a cleaner commercial workflow.
                </p>
                <div class="hero-tags">
                    <span>AI-generated</span>
                    <span>Local analysis</span>
                    <span>Fabric comparison</span>
                </div>
            </div>
            <div class="hero-stats">
                <div class="stat-card">
                    <div class="stat-icon">✦</div>
                    <h4>AI-generated briefing</h4>
                    <p>Use guided model output for richer summary language and commercial positioning.</p>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">▦</div>
                    <h4>Surface and pattern read</h4>
                    <p>Pick up texture, structure, and repeat cues from the image with a cleaner local read.</p>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">⇄</div>
                    <h4>Compare with clarity</h4>
                    <p>Place two materials side by side and explain the choice with a more useful summary layer.</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_feature_strip() -> None:
    cols = st.columns(4)
    items = [
        ("◫ Pattern Read", "Spot stripe, plaid, geometric, or textured-solid direction."),
        ("◌ Surface Feel", "Interpret texture, weight, drape, and finish cues from the image."),
        ("◈ Color Story", "Extract dominant swatches and the overall harmony direction."),
        ("↗ Report Flow", "Package findings into a cleaner material brief and downloadable output."),
    ]
    for col, (title, body) in zip(cols, items):
        with col:
            st.markdown(f"<div class='info-card'><h3>{title}</h3><p>{body}</p></div>", unsafe_allow_html=True)


def render_sample_gallery(sample_dir: str | Path) -> Optional[Tuple[Image.Image, str]]:
    sample_root = Path(sample_dir)
    sample_paths = sorted(sample_root.glob("*.jpg"))
    if not sample_paths:
        return None

    st.markdown("### Curated Samples")
    cols = st.columns(len(sample_paths))
    chosen: Optional[Tuple[Image.Image, str]] = None
    for col, path in zip(cols, sample_paths):
        with col:
            st.image(str(path), use_container_width=True)
            label = path.stem.replace("_", " ").title()
            if st.button(f"Use {label}", key=f"sample-{path.stem}", use_container_width=True):
                chosen = (Image.open(path).convert("RGB"), path.name)
    return chosen


def render_upload_panel(
    title: str = "Upload Fabric Image",
    prompt: str = "Upload a close-up or flat-lay textile image",
    key: str | None = None,
) -> Optional[Tuple[Image.Image, str]]:
    st.markdown(f"### {title}")
    st.markdown("<div class='upload-shell'>", unsafe_allow_html=True)
    uploaded = st.file_uploader(
        prompt,
        type=sorted(ImagePreprocessor.SUPPORTED_FORMATS),
        accept_multiple_files=False,
        key=key,
    )
    st.markdown("</div>", unsafe_allow_html=True)
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


def render_highlight_banner(title: str, body: str) -> None:
    st.markdown(
        f"<div class='highlight-banner'><strong>{title}</strong><p>{body}</p></div>",
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
                        <p>{swatch} &bull; {color['percentage']}%</p>
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