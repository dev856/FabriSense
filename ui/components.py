"""Reusable Streamlit UI components."""

from __future__ import annotations

from html import escape as html_escape
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

import streamlit as st
from PIL import Image

from src.image_preprocessor import ImagePreprocessor


def _safe_text(value: Any) -> str:
    return html_escape("" if value is None else str(value), quote=True)


def _safe_hex(value: Any) -> str:
    text = str(value or "#000000")
    if text.startswith("#") and len(text) in {4, 7}:
        return text
    return "#000000"


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
                    <div class="stat-icon">&#10022;</div>
                    <h4>AI-generated briefing</h4>
                    <p>Use guided model output for richer summary language and commercial positioning.</p>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">&#9646;</div>
                    <h4>Surface and pattern read</h4>
                    <p>Pick up texture, structure, and repeat cues from the image with a cleaner local read.</p>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">&#8644;</div>
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
        ("Pattern Read", "Spot stripe, plaid, geometric, or textured-solid direction."),
        ("Surface Feel", "Interpret texture, weight, drape, and finish cues from the image."),
        ("Color Story", "Extract dominant swatches and the overall harmony direction."),
        ("Report Flow", "Package findings into a cleaner material brief and downloadable output."),
    ]
    for col, (title, body) in zip(cols, items):
        with col:
            st.markdown(f"<div class='info-card'><h3>{title}</h3><p>{body}</p></div>", unsafe_allow_html=True)


def render_sample_gallery(
    sample_dir: str | Path,
    state_key: str = "selected_sample",
) -> Optional[Tuple[Image.Image, str]]:
    sample_root = Path(sample_dir)
    sample_paths = sorted(sample_root.glob("*.jpg"))
    if not sample_paths:
        return None

    st.markdown("### Curated Samples")
    cols = st.columns(len(sample_paths))
    selected_name = st.session_state.get(state_key)

    for col, path in zip(cols, sample_paths):
        with col:
            st.image(str(path), use_container_width=True)
            label = path.stem.replace("_", " ").title()
            is_selected = selected_name == path.name
            button_label = f"Using {label}" if is_selected else f"Use {label}"
            if st.button(button_label, key=f"sample-{state_key}-{path.stem}", use_container_width=True):
                st.session_state[state_key] = path.name
                selected_name = path.name

    if not selected_name:
        return None

    selected_path = next((path for path in sample_paths if path.name == selected_name), None)
    if selected_path is None:
        st.session_state.pop(state_key, None)
        return None

    info_col, clear_col = st.columns((4, 1))
    with info_col:
        st.caption(f"Selected sample: {selected_path.name}")
    with clear_col:
        if st.button("Clear", key=f"clear-{state_key}", use_container_width=True):
            st.session_state.pop(state_key, None)
            return None

    return Image.open(selected_path).convert("RGB"), selected_path.name


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
            swatch = _safe_hex(color.get("hex"))
            st.markdown(
                f"""
                <div class="color-card">
                    <div class="swatch" style="background:{swatch};"></div>
                    <div>
                        <h4>{_safe_text(color.get('name', 'Unknown'))}</h4>
                        <p>{_safe_text(swatch)} &bull; {_safe_text(color.get('percentage', 'N/A'))}%</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_mini_palette(colors: Iterable[Dict[str, Any]]) -> None:
    chips = []
    for color in list(colors)[:4]:
        hex_code = _safe_hex(color.get("hex"))
        chips.append(
            f"<span class='mini-swatch' title='{_safe_text(color.get('name', 'Unknown'))} {hex_code}' style='background:{hex_code};'></span>"
        )
    if chips:
        st.markdown(f"<div class='mini-swatch-row'>{''.join(chips)}</div>", unsafe_allow_html=True)


def render_compare_card(title: str, analysis: Dict[str, Any], image: Image.Image) -> None:
    llm = analysis.get("llm_analysis", {})
    dominant = analysis.get("color_palette", {}).get("dominant_color", {}) or {}
    quality = llm.get("quality_assessment", {})
    texture = llm.get("texture", {})
    fabric = llm.get("fabric_type", {})
    pattern = llm.get("pattern", {})

    st.image(image, caption=title, use_container_width=True)
    st.markdown(
        f"""
        <div class="compare-card">
            <h3>{_safe_text(title)}</h3>
            <div class="compare-card-grid">
                <div><span>Fabric</span><strong>{_safe_text(fabric.get('primary', 'N/A'))}</strong></div>
                <div><span>Pattern</span><strong>{_safe_text(pattern.get('type', 'N/A'))}</strong></div>
                <div><span>Texture</span><strong>{_safe_text(texture.get('primary', 'N/A'))}</strong></div>
                <div><span>Weight</span><strong>{_safe_text(texture.get('weight', 'N/A'))}</strong></div>
                <div><span>Quality</span><strong>{_safe_text(quality.get('score', 'N/A'))} / 10</strong></div>
                <div><span>Color</span><strong>{_safe_text(dominant.get('name', 'N/A'))}</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_mini_palette(analysis.get("color_palette", {}).get("colors", []))


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
