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
            <h3>Material analysis, checkpoint evidence, and review workflows in one place.</h3>
            <p>Move from polished fabric briefs to trained-model benchmarking without leaving the workspace.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_intro(title: str, body: str | None = None, legacy_body: str | None = None) -> None:
    if legacy_body is not None:
        title, body = str(body or ""), legacy_body
    st.markdown(
        f"""
        <section class="page-intro ivory-card">
            <h2>{title}</h2>
            <p class="page-intro-text">{body}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero-shell atelier-home-card ivory-card">
            <div class="hero-copy">
                <h1>Turn a fabric image into a material passport.</h1>
                <p class="hero-text">
                    Upload a close-up textile image and generate a polished read on fabric family,
                    surface feel, color palette, care, quality, and local model evidence.
                </p>
                <div class="hero-tags">
                    <span>Local model</span>
                    <span>Palette story</span>
                    <span>Export ready</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_feature_strip() -> None:
    items = [
        ("Pattern Read", "Spot stripe, plaid, geometric, or textured-solid direction."),
        (
            "Surface Feel",
            "Interpret texture, weight, drape, and finish cues from the image.",
        ),
        ("Color Story", "Extract dominant swatches and the overall harmony direction."),
        (
            "Report Flow",
            "Package findings into a cleaner material brief and downloadable output.",
        ),
    ]
    cards = []
    for title, body in items:
        cards.append(
            "<div class='info-card ivory-card'>"
            f"<h3>{_safe_text(title)}</h3>"
            f"<p>{_safe_text(body)}</p>"
            "</div>"
        )
    st.markdown(
        f"<section class='feature-strip'><div class='feature-card-grid'>{''.join(cards)}</div></section>",
        unsafe_allow_html=True,
    )


def render_client_workflow() -> None:
    steps = [
        ("1", "Choose", "Upload one textile image or pick a built-in sample."),
        ("2", "Analyze", "Run the local model to create the material brief."),
        ("3", "Review", "Scan fabric, color, care, quality, and confidence evidence."),
        ("4", "Share", "Download the report or compare fabrics for a buying decision."),
    ]
    cards = []
    for number, title, body in steps:
        cards.append(
            "<div class='workflow-step ivory-card'>"
            f"<span>{_safe_text(number)}</span>"
            f"<strong>{_safe_text(title)}</strong>"
            f"<p>{_safe_text(body)}</p>"
            "</div>"
        )
    st.markdown(
        "<div class='workflow-strip'>"
        "<div class='workflow-strip-head'>"
        "<h3>Show the journey, then let the result explain itself.</h3>"
        "</div>"
        f"<div class='workflow-step-grid'>{''.join(cards)}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_demo_scenarios() -> None:
    scenarios = [
        (
            "Single Fabric Brief",
            "Best for a quick client demo: one image, one polished material read, one downloadable report.",
        ),
        (
            "Compare Two Options",
            "Best for selection meetings: show which textile is stronger for the target use case.",
        ),
        (
            "Batch Catalog Review",
            "Best for sellers or sourcing teams: process many images and export a compact CSV.",
        ),
    ]
    cards = []
    for title, body in scenarios:
        cards.append(
            f"<div class='scenario-card ivory-card'><h4>{_safe_text(title)}</h4><p>{_safe_text(body)}</p></div>"
        )
    st.markdown(
        f"<div class='scenario-grid'>{''.join(cards)}</div>",
        unsafe_allow_html=True,
    )


def render_sample_gallery(
    sample_dir: str | Path,
    state_key: str = "selected_sample",
) -> Optional[Tuple[Image.Image, str]]:
    sample_root = Path(sample_dir)
    sample_paths = sorted(sample_root.glob("*.jpg"))
    if not sample_paths:
        return None

    st.markdown(
        """
        <div class="input-section-head">
            <h3>Use a curated textile reference</h3>
            <p>Start quickly with one of the built-in swatches and switch anytime.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_name = st.session_state.get(state_key)

    cols = st.columns(3)
    for index, path in enumerate(sample_paths):
        col = cols[index % 3]
        with col:
            st.image(str(path), width="stretch")
            label = path.stem.replace("_", " ").title()
            st.markdown(
                f"<p class='sample-card-title'>{label}</p>", unsafe_allow_html=True
            )
            is_selected = selected_name == path.name
            button_label = f"Using {label}" if is_selected else f"Use {label}"
            if st.button(
                button_label, key=f"sample-{state_key}-{path.stem}", width="stretch"
            ):
                st.session_state[state_key] = path.name
                selected_name = path.name

    if not selected_name:
        return None

    selected_path = next(
        (path for path in sample_paths if path.name == selected_name), None
    )
    if selected_path is None:
        st.session_state.pop(state_key, None)
        return None

    info_col, clear_col = st.columns((4, 1))
    with info_col:
        st.caption(f"Selected sample: {selected_path.name}")
    with clear_col:
        if st.button("Clear", key=f"clear-{state_key}", width="stretch"):
            st.session_state.pop(state_key, None)
            return None

    return Image.open(selected_path).convert("RGB"), selected_path.name


def render_upload_panel(
    title: str = "Upload Fabric Image",
    prompt: str = "Upload a close-up or flat-lay textile image",
    key: str | None = None,
) -> Optional[Tuple[Image.Image, str]]:
    st.markdown(
        f"""
        <div class="input-section-head">
            <h3>{_safe_text(title)}</h3>
            <p>Drop a flat-lay, close-up, or catalog crop to generate a material read.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded = st.file_uploader(
        prompt,
        type=sorted(ImagePreprocessor.SUPPORTED_FORMATS),
        accept_multiple_files=False,
        key=key,
    )
    if uploaded is None:
        return None

    valid, message = ImagePreprocessor.validate_image(uploaded)
    if not valid:
        st.error(message)
        return None

    image = ImagePreprocessor.load_image(uploaded)
    st.caption(message)
    st.image(
        ImagePreprocessor.resize_for_display(image),
        caption=uploaded.name,
        width="stretch",
    )
    return image, uploaded.name


def metric_card(label: str, value: Any, sub: str = "") -> None:
    """Render a compact metric card."""
    st.markdown(
        f"""
        <div class="metric-card fs-metric-card ivory-card">
            <div class="metric-label">{_safe_text(label)}</div>
            <div class="fs-metric-value">{_safe_text(value)}</div>
            <div class="fs-metric-sub">{_safe_text(sub)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def palette_bar(colors: Iterable[Dict[str, Any]] | Iterable[str]) -> None:
    """Render a compact segmented palette bar from color dicts or hex strings."""
    color_list = list(colors)
    if not color_list:
        return

    chips = []
    for item in color_list:
        if isinstance(item, dict):
            hex_code = _safe_hex(item.get("hex"))
            label = f"{item.get('name', 'Unknown')} {hex_code}"
        else:
            hex_code = _safe_hex(item)
            label = hex_code
        chips.append(
            f'<div class="fs-palette-chip" style="background:{hex_code};" title="{_safe_text(label)}"></div>'
        )

    st.markdown(
        f'<div class="fs-palette-bar">{"".join(chips)}</div>',
        unsafe_allow_html=True,
    )


def material_passport(title: str, rows: Dict[str, Any]) -> None:
    """Render the ivory two-column Material Passport card with hairline dividers."""
    items = []
    for label, value in rows.items():
        items.append(
            "<div class='fs-passport-item'>"
            f"<div class='fs-passport-label'>{_safe_text(label)}</div>"
            f"<strong class='fs-passport-value'>{_safe_text(value)}</strong>"
            "</div>"
        )
    st.markdown(
        f"""
        <section class="fs-card fs-passport ivory-card">
            <div>
                <h3>{_safe_text(title)}</h3>
            </div>
            <div class="fs-passport-grid">{''.join(items)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_metric_band(metrics: Dict[str, Any]) -> None:
    cols = st.columns(4)
    cards = [
        (
            "Quality",
            f"{metrics.get('score', 'N/A')}/10"
            if isinstance(metrics.get("score"), (int, float))
            else str(metrics.get("score", "N/A")),
        ),
        ("Rating", metrics.get("stars", "N/A")),
        ("Best Seasons", metrics.get("seasons", "N/A")),
        ("Eco Score", str(metrics.get("eco_score", "N/A"))),
    ]
    for col, (title, value) in zip(cols, cards):
        with col:
            metric_card(title, value)


def render_highlight_banner(title: str, body: str) -> None:
    st.markdown(
        f"<div class='highlight-banner'><strong>{title}</strong><p>{body}</p></div>",
        unsafe_allow_html=True,
    )


def render_color_palette(colors: Iterable[Dict[str, Any]], harmony: str) -> None:
    color_list = list(colors)
    if not color_list:
        return
    st.markdown(f"### Color Palette  |  Harmony: `{harmony}`")
    cols = st.columns(3)
    for index, color in enumerate(color_list):
        with cols[index % 3]:
            swatch = _safe_hex(color.get("hex"))
            st.markdown(
                f"""
                <div class="color-card ivory-card">
                    <div class="swatch" style="background:{swatch};"></div>
                    <div>
                        <h4>{_safe_text(color.get("name", "Unknown"))}</h4>
                        <p>{_safe_text(swatch)} &bull; {_safe_text(color.get("percentage", "N/A"))}%</p>
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
        st.markdown(
            f"<div class='mini-swatch-row'>{''.join(chips)}</div>",
            unsafe_allow_html=True,
        )


def _get_drape_percentage(drape_val: Any) -> int:
    drape_str = str(drape_val or "").strip().lower()
    if "fluid" in drape_str:
        return 85
    elif "moderate" in drape_str:
        return 60
    elif "structured" in drape_str:
        return 40
    elif "stiff" in drape_str:
        return 20
    elif "high" in drape_str:
        return 80
    elif "medium" in drape_str:
        return 50
    elif "low" in drape_str:
        return 30
    return 50


def _get_texture_percentage(texture_val: Any, hand_feel_val: Any, hand_feel_score_val: Any = None) -> int:
    if isinstance(hand_feel_score_val, (int, float)):
        return min(max(int(float(hand_feel_score_val) * 10), 0), 100)

    if hand_feel_score_val:
        try:
            val_str = str(hand_feel_score_val).split("/")[0].strip().rstrip("%")
            val_f = float(val_str)
            return min(max(int(val_f * 10) if val_f <= 10 else int(val_f), 0), 100)
        except ValueError:
            pass

    text = str(hand_feel_val or texture_val or "").strip().lower()
    if not text:
        return 50

    if "excellent" in text or "very high" in text:
        return 90
    elif "high" in text or "dense" in text or "thick" in text:
        return 80
    elif "good" in text or "moderate" in text or "medium" in text:
        return 60
    elif "fair" in text or "average" in text:
        return 45
    elif "low" in text or "thin" in text or "soft" in text:
        return 30
    elif "very low" in text or "fine" in text:
        return 15
    return 50


def _build_circular_svg(percentage: int, color_var: str = "var(--accent)") -> str:
    return f"""
    <svg width="70" height="70" viewBox="0 0 36 36" style="filter: drop-shadow(0 4px 10px rgba(18,28,36,0.08));">
      <path
        d="M18 2.0845
          a 15.9155 15.9155 0 0 1 0 31.831
          a 15.9155 15.9155 0 0 1 0 -31.831"
        fill="none"
        stroke="rgba(19, 37, 40, 0.08)"
        stroke-width="3"
      />
      <path
        stroke-dasharray="{percentage}, 100"
        d="M18 2.0845
          a 15.9155 15.9155 0 0 1 0 31.831
          a 15.9155 15.9155 0 0 1 0 -31.831"
        fill="none"
        stroke="{color_var}"
        stroke-width="3"
        stroke-linecap="round"
        style="transition: stroke-dasharray 0.6s cubic-bezier(0.16, 1, 0.3, 1);"
      />
      <text x="18" y="20.35" font-family="'Manrope', sans-serif" font-size="8" font-weight="800" text-anchor="middle" fill="var(--ink-strong)">{percentage}%</text>
    </svg>
    """


def render_compare_card(
    title: str, analysis: Dict[str, Any], image: Image.Image
) -> None:
    llm = analysis.get("llm_analysis", {})
    dominant = analysis.get("color_palette", {}).get("dominant_color", {}) or {}
    quality = llm.get("quality_assessment", {})
    texture = llm.get("texture", {})
    fabric = llm.get("fabric_type", {})
    pattern = llm.get("pattern", {})

    drape_pct = _get_drape_percentage(texture.get("drape"))
    texture_pct = _get_texture_percentage(texture.get("primary"), texture.get("hand_feel"), texture.get("hand_feel_score"))

    texture_svg = _build_circular_svg(texture_pct, "var(--accent)")
    drape_svg = _build_circular_svg(drape_pct, "var(--accent-cool)")

    st.image(image, caption=title, width="stretch")
    st.markdown(
        f"""
        <div class="compare-card ivory-card">
            <h3>{_safe_text(title)}</h3>
            <div class="compare-card-grid">
                <div><span>Fabric</span><strong>{_safe_text(fabric.get("primary", "N/A"))}</strong></div>
                <div><span>Pattern</span><strong>{_safe_text(pattern.get("type", "N/A"))}</strong></div>
                <div><span>Texture</span><strong>{_safe_text(texture.get("primary", "N/A"))}</strong></div>
                <div><span>Weight</span><strong>{_safe_text(texture.get("weight", "N/A"))}</strong></div>
                <div><span>Quality</span><strong>{_safe_text(quality.get("score", "N/A"))} / 10</strong></div>
                <div><span>Color</span><strong>{_safe_text(dominant.get("name", "N/A"))}</strong></div>
            </div>
            <div style="display: flex; justify-content: space-around; margin-top: 1rem; padding: 0.75rem 0 0.25rem; border-top: 1px solid var(--line);">
                <div style="display: flex; flex-direction: column; align-items: center; gap: 0.35rem;">
                    <span style="font-size: 0.68rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted-soft);">Texture density</span>
                    {texture_svg}
                    <span style="font-size: 0.72rem; font-weight: 700; color: var(--ink);">{_safe_text(texture.get("hand_feel", "N/A"))}</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: center; gap: 0.35rem;">
                    <span style="font-size: 0.68rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted-soft);">Drape flow</span>
                    {drape_svg}
                    <span style="font-size: 0.72rem; font-weight: 700; color: var(--ink);">{_safe_text(texture.get("drape", "N/A"))}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_mini_palette(analysis.get("color_palette", {}).get("colors", []))


def render_key_value_block(title: str, rows: Dict[str, Any]) -> None:
    st.markdown(f"### {title}")
    items = []
    for label, value in rows.items():
        items.append(
            "<div class='kv-row'>"
            f"<span class='kv-label'>{_safe_text(label)}</span>"
            f"<span class='kv-value'>{_safe_text(value)}</span>"
            "</div>"
        )
    st.markdown(
        f"<div class='result-card ivory-card'>{''.join(items)}</div>",
        unsafe_allow_html=True,
    )


def render_list_block(title: str, items: Iterable[str]) -> None:
    st.markdown(f"### {title}")
    values = list(items)
    if not values:
        body = "<p>No data available.</p>"
    else:
        body = "<ul>" + "".join(f"<li>{_safe_text(item)}</li>" for item in values) + "</ul>"
    st.markdown(f"<div class='result-card ivory-card'>{body}</div>", unsafe_allow_html=True)


def render_empty_state(icon: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="empty-state-card ivory-card">
            <div class="empty-state-icon">{icon}</div>
            <h3>{_safe_text(title)}</h3>
            <p>{_safe_text(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_confidence_bar(label: str, confidence: float) -> str:
    pct = round(confidence * 100, 1)
    tier = "high" if confidence >= 0.8 else ("medium" if confidence >= 0.5 else "low")
    return f"""
    <div class="confidence-bar-container">
        <span style="font-size:0.82rem;font-weight:700;color:var(--ink);min-width:8ch;">{_safe_text(label)}</span>
        <div class="confidence-bar">
            <div class="confidence-bar-fill {tier}" style="width:{pct}%;"></div>
        </div>
        <span class="confidence-bar-label">{pct}%</span>
    </div>"""


def render_badge(label: str, variant: str = "accent") -> str:
    return f'<span class="badge badge-{variant}">{_safe_text(label)}</span>'


def render_status_dot(online: bool, pulse: bool = False) -> str:
    cls = "online" if online else "offline"
    pulse_cls = " pulse-dot" if pulse and online else ""
    return f'<span class="status-dot {cls}{pulse_cls}"></span>'


def render_skeleton(lines: int = 3, show_title: bool = True) -> str:
    parts = []
    if show_title:
        parts.append('<div class="skeleton skeleton-title"></div>')
    for i in range(lines):
        parts.append(
            f'<div class="skeleton skeleton-text" style="width:{80 - i * 15}%;"></div>'
        )
    return f'<div style="padding:1rem;">{"".join(parts)}</div>'


def render_skeleton_card() -> str:
    return '<div class="skeleton skeleton-card" style="margin-bottom:0.8rem;"></div>'


def render_swatch_skeleton() -> str:
    return '<div class="skeleton skeleton-swatch" style="margin-bottom:0.8rem;"></div>'


def render_confusion_matrix_heatmap(
    confusion_matrix: list[list[int]],
    labels: list[str],
) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.caption("Install plotly to view the interactive confusion matrix heatmap.")
        return

    colorscale = [
        [0, "#121820"],
        [0.25, "#2A313A"],
        [0.5, "#6B6257"],
        [0.75, "#C9A86B"],
        [1, "#DDBB7E"],
    ]
    text_color = "#FAF7F2"
    title_color = "#FAF7F2"
    tick_color = "#C9A86B"

    fig = go.Figure(
        data=go.Heatmap(
            z=confusion_matrix,
            x=labels,
            y=labels,
            colorscale=colorscale,
            text=[[str(v) for v in row] for row in confusion_matrix],
            texttemplate="%{text}",
            textfont={"size": 11, "color": text_color},
            hoverongaps=False,
            hovertemplate="Predicted: %{x}<br>Actual: %{y}<br>Count: %{z}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text="Confusion Matrix", font=dict(size=16, color=title_color)),
        xaxis_title="Predicted Label",
        yaxis_title="True Label",
        xaxis=dict(tickangle=45, tickfont=dict(size=10, color=tick_color)),
        yaxis=dict(tickfont=dict(size=10, color=tick_color)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=80, r=30, t=60, b=100),
        height=max(420, len(labels) * 45),
        width=None,
    )
    st.plotly_chart(fig, width="stretch")


def render_color_wheel(colors: Iterable[Dict[str, Any]]) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.caption("Install plotly to view the interactive color wheel.")
        return

    color_list = list(colors)
    if not color_list:
        return

    title_color = "#FAF7F2"
    legend_font_color = "#E8E3D8"
    legend_bg = "rgba(18,24,32,0.72)"

    fig = go.Figure()
    for i, color in enumerate(color_list):
        hex_code = _safe_hex(color.get("hex"))
        name = _safe_text(color.get("name", f"Color {i + 1}"))
        pct = color.get("percentage", 0)
        angle = i * (360 / max(len(color_list), 1))
        fig.add_trace(
            go.Barpolar(
                r=[pct],
                theta=[angle],
                width=[360 / max(len(color_list), 1) - 4],
                marker_color=hex_code,
                marker_line_color="rgba(20, 33, 43, 0.08)",
                marker_line_width=1,
                name=name,
                hovertemplate=f"{name}<br>{hex_code}<br>{pct}%<extra></extra>",
                showlegend=True,
            )
        )

    fig.update_layout(
        title=dict(text="Color Distribution", font=dict(size=16, color=title_color)),
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, max(c.get("percentage", 0) for c in color_list) + 10],
            ),
            angularaxis=dict(visible=False),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(
            font=dict(size=11, color=legend_font_color), bgcolor=legend_bg
        ),
        height=380,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    st.plotly_chart(fig, width="stretch")


def render_radar_chart(
    labels: list[str],
    values: list[float],
    title: str = "Quality Profile",
    max_value: float = 10.0,
) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.caption("Install plotly to view the radar chart.")
        return

    if not labels or not values or len(labels) != len(values):
        return

    fill_color = "rgba(201, 168, 107, 0.18)"
    line_color = "#C9A86B"
    marker_color = "#DDBB7E"
    radial_tick_color = "#B8B2A9"
    angular_tick_color = "#E8E3D8"
    title_color = "#FAF7F2"

    clamped = [min(max(v, 0), max_value) for v in values]
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=clamped + [clamped[0]],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor=fill_color,
            line=dict(color=line_color, width=2.5),
            marker=dict(size=6, color=marker_color),
            name=title,
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_value],
                tickfont=dict(size=10, color=radial_tick_color),
            ),
            angularaxis=dict(tickfont=dict(size=11, color=angular_tick_color)),
            bgcolor="rgba(0,0,0,0)",
        ),
        title=dict(
            text=title, font=dict(size=16, color=title_color, family="Fraunces, serif")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=360,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    st.plotly_chart(fig, width="stretch")


def render_gauge_chart(
    value: float,
    title: str = "Score",
    max_value: float = 10.0,
    thresholds: tuple[float, float] | None = None,
) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.caption("Install plotly to view the gauge chart.")
        return

    if thresholds is None:
        thresholds = (max_value * 0.4, max_value * 0.7)

    clamped = min(max(value, 0), max_value)
    pct = clamped / max_value * 100
    color = (
        "#8B5E3C"
        if pct < thresholds[0] / max_value * 100
        else ("#B08968" if pct < thresholds[1] / max_value * 100 else "#C9A86B")
    )
    title_color = "#FAF7F2"
    tick_color = "#B8B2A9"
    threshold_line_color = "#FAF7F2"
    step_colors = [
        "rgba(139, 94, 60, 0.16)",
        "rgba(201, 168, 107, 0.12)",
        "rgba(201, 168, 107, 0.20)",
    ]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=clamped,
            domain=dict(x=[0, 1], y=[0, 1]),
            title=dict(
                text=title,
                font=dict(size=16, color=title_color, family="Fraunces, serif"),
            ),
            number=dict(font=dict(size=36, color=color, family="Fraunces, serif")),
            gauge=dict(
                axis=dict(
                    range=[0, max_value], tickfont=dict(size=10, color=tick_color)
                ),
                bar=dict(color=color, thickness=0.35),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                steps=[
                    dict(range=[0, thresholds[0]], color=step_colors[0]),
                    dict(
                        range=[thresholds[0], thresholds[1]],
                        color=step_colors[1],
                    ),
                    dict(
                        range=[thresholds[1], max_value],
                        color=step_colors[2],
                    ),
                ],
                threshold=dict(
                    line=dict(color=threshold_line_color, width=2),
                    thickness=0.8,
                    value=max_value * 0.8,
                ),
            ),
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=30, r=30, t=80, b=20),
    )
    st.plotly_chart(fig, width="stretch")


def render_confusion_sankey(
    confusion_matrix: list[list[int]],
    labels: list[str],
) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.caption("Install plotly to view the confusion flow diagram.")
        return

    if not confusion_matrix or not labels:
        return

    warm = "rgba(201, 168, 107, 0.25)"
    misclass = "rgba(139, 94, 60, 0.35)"
    actual_node_color = "#C9A86B"
    predicted_node_color = "#DDBB7E"
    title_color = "#FAF7F2"
    font_color = "#E8E3D8"

    n = len(labels)
    source, target, value, link_colors = [], [], [], []

    for i in range(n):
        for j in range(n):
            count = confusion_matrix[i][j]
            if count > 0:
                source.append(i)
                target.append(n + j)
                value.append(count)
                link_colors.append(warm if i == j else misclass)

    node_colors = [actual_node_color] * n + [predicted_node_color] * n
    node_labels = [f"Actual: {l}" for l in labels] + [f"Predicted: {l}" for l in labels]

    fig = go.Figure(
        go.Sankey(
            node=dict(
                pad=12,
                thickness=18,
                line=dict(color="rgba(20,33,43,0.08)", width=0.5),
                label=node_labels,
                color=node_colors,
            ),
            link=dict(source=source, target=target, value=value, color=link_colors),
        )
    )
    fig.update_layout(
        title=dict(
            text="Misclassification Flow",
            font=dict(size=16, color=title_color, family="Fraunces, serif"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color=font_color),
        height=max(400, n * 38),
        margin=dict(l=10, r=10, t=60, b=20),
    )
    st.plotly_chart(fig, width="stretch")


def render_image_comparison(
    image_a: "Image.Image",
    image_b: "Image.Image",
    label_a: str = "Fabric A",
    label_b: str = "Fabric B",
) -> None:
    try:
        from streamlit_image_comparison import image_comparison
        import tempfile, os

        tmp_a = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp_b = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        try:
            image_a.save(tmp_a.name)
            image_b.save(tmp_b.name)
            image_comparison(
                img1=tmp_a.name,
                img2=tmp_b.name,
                label1=label_a,
                label2=label_b,
                starting_position=50,
                show_labels=True,
                make_responsive=True,
            )
        finally:
            tmp_a.close()
            tmp_b.close()
            for tmp_path in (tmp_a.name, tmp_b.name):
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
    except ImportError:
        import streamlit as st_local

        col_a, col_b = st_local.columns(2)
        with col_a:
            st_local.image(image_a, caption=label_a, width="stretch")
        with col_b:
            st_local.image(image_b, caption=label_b, width="stretch")


def render_interactive_table(
    data: list[dict] | "pd.DataFrame",
    height: int = 400,
    selection_mode: str = "single",
) -> Any:
    try:
        import pandas as pd
        from st_aggrid import AgGrid, GridOptionsBuilder
    except ImportError:
        import streamlit as st_local

        st_local.dataframe(data, width="stretch")
        return None

    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode, pre_selected_rows=[])
    gb.configure_side_bar(filters_panel=True, columns_panel=False)
    gb.configure_default_column(
        filterable=True, sortable=True, resizable=True, wrap_text=True
    )
    grid = AgGrid(
        df,
        gridOptions=gb.build(),
        theme="balham",
        height=height,
        allow_unsafe_jscode=False,
    )
    return grid


def render_chat_narrative(analysis: Dict[str, Any]) -> None:
    import streamlit as st_local

    llm = analysis.get("llm_analysis") or {}
    fabric = llm.get("fabric_type") or {}
    pattern = llm.get("pattern") or {}
    texture = llm.get("texture") or {}
    quality = llm.get("quality_assessment") or {}
    palette = analysis.get("color_palette") or {}

    with st_local.chat_message("assistant", avatar="\U0001f9f5"):
        summary = llm.get("overall_summary")
        if summary:
            st_local.markdown(f"**Material Brief**  \n{summary}")

        fabric_primary = fabric.get("primary")
        if fabric_primary:
            st_local.markdown(f"- **Fabric**: {fabric_primary}")
            if fabric.get("sub_type"):
                st_local.markdown(f"  - Subtype: {fabric.get('sub_type')}")
            if fabric.get("blend_composition"):
                st_local.markdown(f"  - Blend: {fabric.get('blend_composition')}")

        pattern_type = pattern.get("type")
        if pattern_type:
            st_local.markdown(
                f"- **Pattern**: {pattern_type} / {pattern.get('sub_type', 'N/A')}"
            )

        texture_primary = texture.get("primary")
        if texture_primary:
            st_local.markdown(
                f"- **Texture**: {texture_primary} | Weight: {texture.get('weight', 'N/A')} | Drape: {texture.get('drape', 'N/A')}"
            )

        quality_score = quality.get("score")
        if quality_score is not None:
            st_local.markdown(
                f"- **Quality**: {quality_score}/10 ({quality.get('grade', 'N/A')})"
            )

        dominant_color = palette.get("dominant_color", {})
        if dominant_color.get("name"):
            st_local.markdown(
                f"- **Dominant Color**: {dominant_color.get('name')} ({dominant_color.get('hex', 'N/A')})"
            )

        fun_fact = llm.get("fun_fact")
        if fun_fact:
            st_local.markdown(f"  \n*{fun_fact}*")


def render_palette_gradient_bar(colors: Iterable[Dict[str, Any]]) -> None:
    color_list = list(colors)
    if not color_list:
        return
    stops = []
    cumulative = 0
    total = sum(c.get("percentage", 0) for c in color_list) or 1
    for color in color_list:
        hex_code = _safe_hex(color.get("hex"))
        pct = color.get("percentage", 0) / total * 100
        stops.append(f"{hex_code} {cumulative:.1f}%")
        cumulative += pct
        stops.append(f"{hex_code} {cumulative:.1f}%")

    gradient = f"linear-gradient(90deg, {', '.join(stops)})"
    tooltip_parts = " | ".join(
        f"{c.get('name', '?')} ({c.get('hex', '?')})" for c in color_list
    )
    st.markdown(
        f"""
        <div class="fs-gradient-bar" title="{_safe_text(tooltip_parts)}" style="background:{gradient}; height:16px; border:1px solid var(--line);">
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_floating_action_bar(label: str, buttons_html: str) -> None:
    st.markdown(
        f"""
        <div class="floating-action-bar">
            <span class="fab-label">{_safe_text(label)}</span>
            {buttons_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
