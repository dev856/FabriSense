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
            <h3>Material analysis, checkpoint evidence, and review workflows in one place.</h3>
            <p>Move from polished fabric briefs to trained-model benchmarking without leaving the workspace.</p>
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
                    FabriSense puts the locally trained classifier, checkpoint inspection, and benchmark-ready review flows in one cleaner product experience.
                </p>
                <div class="hero-tags">
                    <span>Trained model</span>
                    <span>Local evidence</span>
                    <span>Benchmark lab</span>
                </div>
            </div>
            <div class="hero-stats">
                <div class="stat-card">
                    <div class="stat-icon">&#10022;</div>
                    <h4>Local model briefing</h4>
                    <p>Use the trained classifier output with confidence, alternatives, and checkpoint context.</p>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">&#9646;</div>
                    <h4>Checkpoint evidence</h4>
                    <p>Surface confidence, top alternatives, and saved review notes directly in the result flow.</p>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">&#8644;</div>
                    <h4>Benchmark with clarity</h4>
                    <p>Compare checkpoints on known splits or uploaded labeled ZIPs without leaving the app.</p>
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
    for col, (title, body) in zip(cols, items):
        with col:
            st.markdown(
                f"<div class='info-card'><h3>{title}</h3><p>{body}</p></div>",
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
            <p class="eyebrow">Sample Library</p>
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
            <p class="eyebrow">Image Upload</p>
            <h3>{_safe_text(title)}</h3>
            <p>Drop a flat-lay, close-up, or catalog crop to generate a material read.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
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
    st.image(
        ImagePreprocessor.resize_for_display(image),
        caption=uploaded.name,
        width="stretch",
    )
    return image, uploaded.name


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
                <div class="color-card">
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


def render_compare_card(
    title: str, analysis: Dict[str, Any], image: Image.Image
) -> None:
    llm = analysis.get("llm_analysis", {})
    dominant = analysis.get("color_palette", {}).get("dominant_color", {}) or {}
    quality = llm.get("quality_assessment", {})
    texture = llm.get("texture", {})
    fabric = llm.get("fabric_type", {})
    pattern = llm.get("pattern", {})

    st.image(image, caption=title, width="stretch")
    st.markdown(
        f"""
        <div class="compare-card">
            <h3>{_safe_text(title)}</h3>
            <div class="compare-card-grid">
                <div><span>Fabric</span><strong>{_safe_text(fabric.get("primary", "N/A"))}</strong></div>
                <div><span>Pattern</span><strong>{_safe_text(pattern.get("type", "N/A"))}</strong></div>
                <div><span>Texture</span><strong>{_safe_text(texture.get("primary", "N/A"))}</strong></div>
                <div><span>Weight</span><strong>{_safe_text(texture.get("weight", "N/A"))}</strong></div>
                <div><span>Quality</span><strong>{_safe_text(quality.get("score", "N/A"))} / 10</strong></div>
                <div><span>Color</span><strong>{_safe_text(dominant.get("name", "N/A"))}</strong></div>
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


def render_empty_state(icon: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="empty-state-card">
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

    fig = go.Figure(
        data=go.Heatmap(
            z=confusion_matrix,
            x=labels,
            y=labels,
            colorscale=[
                [0, "#f7f3ec"],
                [0.25, "#e4ddd1"],
                [0.5, "#d4a574"],
                [0.75, "#bb6c3f"],
                [1, "#9d5630"],
            ],
            text=[[str(v) for v in row] for row in confusion_matrix],
            texttemplate="%{text}",
            textfont={"size": 11, "color": "#14212b"},
            hoverongaps=False,
            hovertemplate="Predicted: %{x}<br>Actual: %{y}<br>Count: %{z}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text="Confusion Matrix", font=dict(size=16, color="#14212b")),
        xaxis_title="Predicted Label",
        yaxis_title="True Label",
        xaxis=dict(tickangle=45, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
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
        title=dict(text="Color Distribution", font=dict(size=16, color="#14212b")),
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
            font=dict(size=11, color="#243240"), bgcolor="rgba(255,255,255,0.5)"
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

    clamped = [min(max(v, 0), max_value) for v in values]
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=clamped + [clamped[0]],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor="rgba(187, 108, 63, 0.18)",
            line=dict(color="#bb6c3f", width=2.5),
            marker=dict(size=6, color="#bb6c3f"),
            name=title,
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_value],
                tickfont=dict(size=10, color="#5e6b77"),
            ),
            angularaxis=dict(tickfont=dict(size=11, color="#243240")),
            bgcolor="rgba(0,0,0,0)",
        ),
        title=dict(
            text=title, font=dict(size=16, color="#14212b", family="Fraunces, serif")
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
        "#9a4b49"
        if pct < thresholds[0] / max_value * 100
        else ("#9f6a24" if pct < thresholds[1] / max_value * 100 else "#2f7d63")
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=clamped,
            domain=dict(x=[0, 1], y=[0, 1]),
            title=dict(
                text=title,
                font=dict(size=16, color="#14212b", family="Fraunces, serif"),
            ),
            number=dict(font=dict(size=36, color=color, family="Fraunces, serif")),
            gauge=dict(
                axis=dict(
                    range=[0, max_value], tickfont=dict(size=10, color="#5e6b77")
                ),
                bar=dict(color=color, thickness=0.35),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                steps=[
                    dict(range=[0, thresholds[0]], color="rgba(154, 75, 73, 0.08)"),
                    dict(
                        range=[thresholds[0], thresholds[1]],
                        color="rgba(159, 106, 36, 0.08)",
                    ),
                    dict(
                        range=[thresholds[1], max_value],
                        color="rgba(47, 125, 99, 0.08)",
                    ),
                ],
                threshold=dict(
                    line=dict(color="#14212b", width=2),
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

    n = len(labels)
    source, target, value, link_colors = [], [], [], []
    warm = "rgba(187, 108, 63, 0.25)"
    cool = "rgba(47, 116, 135, 0.25)"
    misclass = "rgba(154, 75, 73, 0.30)"

    for i in range(n):
        for j in range(n):
            count = confusion_matrix[i][j]
            if count > 0:
                source.append(i)
                target.append(n + j)
                value.append(count)
                link_colors.append(warm if i == j else misclass)

    node_colors = ["#bb6c3f"] * n + ["#2f7487"] * n
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
            font=dict(size=16, color="#14212b", family="Fraunces, serif"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color="#243240"),
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
        <div title="{_safe_text(tooltip_parts)}" style="
            height: 36px;
            border-radius: 18px;
            background: {gradient};
            border: 1px solid rgba(20, 33, 43, 0.08);
            box-shadow: 0 6px 20px rgba(18, 28, 36, 0.10);
            cursor: pointer;
            margin-bottom: 0.6rem;
            transition: transform 200ms ease, box-shadow 200ms ease;
        " onmouseover="this.style.transform='scaleY(1.25)';this.style.boxShadow='0 10px 30px rgba(18,28,36,0.16)'"
           onmouseout="this.style.transform='scaleY(1)';this.style.boxShadow='0 6px 20px rgba(18,28,36,0.10)'">
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
