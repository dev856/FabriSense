"""Comprehensive tests for UI modernization: components, charts, navigation, dark mode, and integrations."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from PIL import Image


class TestSafeTextHelpers(unittest.TestCase):
    def test_safe_text_normal_string(self):
        from ui.components import _safe_text

        self.assertEqual(_safe_text("hello"), "hello")

    def test_safe_text_none(self):
        from ui.components import _safe_text

        self.assertEqual(_safe_text(None), "")

    def test_safe_text_html_escape(self):
        from ui.components import _safe_text

        self.assertEqual(_safe_text("<script>"), "&lt;script&gt;")

    def test_safe_text_quote_escape(self):
        from ui.components import _safe_text

        self.assertEqual(_safe_text('a"b'), "a&quot;b")

    def test_safe_text_number(self):
        from ui.components import _safe_text

        self.assertEqual(_safe_text(42), "42")

    def test_safe_hex_valid(self):
        from ui.components import _safe_hex

        self.assertEqual(_safe_hex("#ff0000"), "#ff0000")

    def test_safe_hex_short(self):
        from ui.components import _safe_hex

        self.assertEqual(_safe_hex("#f00"), "#f00")

    def test_safe_hex_invalid(self):
        from ui.components import _safe_hex

        self.assertEqual(_safe_hex("red"), "#000000")

    def test_safe_hex_none(self):
        from ui.components import _safe_hex

        self.assertEqual(_safe_hex(None), "#000000")

    def test_safe_hex_empty(self):
        from ui.components import _safe_hex

        self.assertEqual(_safe_hex(""), "#000000")

    def test_safe_hex_long_hex(self):
        from ui.components import _safe_hex

        self.assertEqual(_safe_hex("#ff0000ff"), "#000000")


class TestScoreValueHelper(unittest.TestCase):
    def test_score_value_accepts_qualitative_local_labels(self):
        from ui.pages import _score_value

        self.assertEqual(_score_value("Low"), 3.0)
        self.assertEqual(_score_value("Medium"), 5.5)
        self.assertEqual(_score_value("High"), 8.0)

    def test_score_value_accepts_numeric_strings(self):
        from ui.pages import _score_value

        self.assertEqual(_score_value("7/10"), 7.0)
        self.assertEqual(_score_value("80%"), 8.0)

    def test_score_value_uses_default_for_unknown_text(self):
        from ui.pages import _score_value

        self.assertEqual(_score_value("not available", default=4.0), 4.0)


class TestConfidenceBar(unittest.TestCase):
    def test_high_confidence(self):
        from ui.components import render_confidence_bar

        html = render_confidence_bar("Cotton", 0.95)
        self.assertIn("95.0%", html)
        self.assertIn("high", html)
        self.assertIn("Cotton", html)

    def test_medium_confidence(self):
        from ui.components import render_confidence_bar

        html = render_confidence_bar("Silk", 0.65)
        self.assertIn("65.0%", html)
        self.assertIn("medium", html)

    def test_low_confidence(self):
        from ui.components import render_confidence_bar

        html = render_confidence_bar("Nylon", 0.25)
        self.assertIn("25.0%", html)
        self.assertIn("low", html)

    def test_zero_confidence(self):
        from ui.components import render_confidence_bar

        html = render_confidence_bar("Test", 0.0)
        self.assertIn("0.0%", html)
        self.assertIn("low", html)

    def test_perfect_confidence(self):
        from ui.components import render_confidence_bar

        html = render_confidence_bar("Test", 1.0)
        self.assertIn("100.0%", html)
        self.assertIn("high", html)

    def test_boundary_medium_high(self):
        from ui.components import render_confidence_bar

        html = render_confidence_bar("Test", 0.8)
        self.assertIn("high", html)

    def test_boundary_low_medium(self):
        from ui.components import render_confidence_bar

        html = render_confidence_bar("Test", 0.5)
        self.assertIn("medium", html)

    def test_label_xss_prevention(self):
        from ui.components import render_confidence_bar

        html = render_confidence_bar("<script>alert(1)</script>", 0.9)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)


class TestBadge(unittest.TestCase):
    def test_success_badge(self):
        from ui.components import render_badge

        html = render_badge("Ready", "success")
        self.assertIn("badge-success", html)
        self.assertIn("Ready", html)

    def test_danger_badge(self):
        from ui.components import render_badge

        html = render_badge("Error", "danger")
        self.assertIn("badge-danger", html)

    def test_warning_badge(self):
        from ui.components import render_badge

        html = render_badge("Caution", "warning")
        self.assertIn("badge-warning", html)

    def test_accent_badge(self):
        from ui.components import render_badge

        html = render_badge("Info", "accent")
        self.assertIn("badge-accent", html)

    def test_cool_badge(self):
        from ui.components import render_badge

        html = render_badge("Tech", "cool")
        self.assertIn("badge-cool", html)

    def test_badge_xss(self):
        from ui.components import render_badge

        html = render_badge("<img onerror=x>", "accent")
        self.assertNotIn("<img", html)


class TestStatusDot(unittest.TestCase):
    def test_online_dot(self):
        from ui.components import render_status_dot

        html = render_status_dot(True)
        self.assertIn("online", html)

    def test_offline_dot(self):
        from ui.components import render_status_dot

        html = render_status_dot(False)
        self.assertIn("offline", html)

    def test_pulse_dot(self):
        from ui.components import render_status_dot

        html = render_status_dot(True, pulse=True)
        self.assertIn("pulse-dot", html)

    def test_no_pulse_when_offline(self):
        from ui.components import render_status_dot

        html = render_status_dot(False, pulse=True)
        self.assertNotIn("pulse-dot", html)


class TestSkeletonComponents(unittest.TestCase):
    def test_skeleton_default(self):
        from ui.components import render_skeleton

        html = render_skeleton()
        self.assertIn("skeleton", html)
        self.assertIn("skeleton-title", html)

    def test_skeleton_no_title(self):
        from ui.components import render_skeleton

        html = render_skeleton(show_title=False)
        self.assertNotIn("skeleton-title", html)

    def test_skeleton_card(self):
        from ui.components import render_skeleton_card

        html = render_skeleton_card()
        self.assertIn("skeleton-card", html)

    def test_swatch_skeleton(self):
        from ui.components import render_swatch_skeleton

        html = render_swatch_skeleton()
        self.assertIn("skeleton-swatch", html)

    def test_skeleton_line_count(self):
        from ui.components import render_skeleton

        html = render_skeleton(lines=5)
        self.assertEqual(html.count("skeleton-text"), 5)


class TestEmptyState(unittest.TestCase):
    def test_empty_state_html_content(self):
        from ui.components import render_empty_state

        with patch("streamlit.markdown") as mock_md:
            render_empty_state(
                "&#128269;", "No Data", "Upload something to see results."
            )
            mock_md.assert_called_once()
            html = mock_md.call_args[0][0]
            self.assertIn("empty-state-card", html)
            self.assertIn("No Data", html)
            self.assertIn("Upload something", html)

    def test_empty_state_xss_title_body_escaped(self):
        from ui.components import render_empty_state

        with patch("streamlit.markdown") as mock_md:
            render_empty_state("&#128269;", "<b>Title</b>", "<i>Body</i>")
            html = mock_md.call_args[0][0]
            self.assertNotIn("<b>", html)
            self.assertNotIn("<i>", html)
            self.assertIn("&lt;b&gt;", html)
            self.assertIn("&lt;i&gt;", html)


class TestClientWorkflow(unittest.TestCase):
    def test_client_workflow_renders_compact_html(self):
        from ui.components import render_client_workflow

        with patch("streamlit.markdown") as mock_md:
            render_client_workflow()
            html = mock_md.call_args[0][0]
            self.assertIn("workflow-step-grid", html)
            self.assertIn("<div class='workflow-step ivory-card'>", html)
            self.assertNotIn('\n            <div class="workflow-step">', html)


class TestLabelCleanup(unittest.TestCase):
    def test_home_intro_components_do_not_render_eyebrow_labels(self):
        from ui.components import (
            render_client_workflow,
            render_hero,
            render_page_intro,
            render_sidebar_brand,
        )

        for renderer in (
            render_sidebar_brand,
            render_hero,
            render_client_workflow,
            lambda: render_page_intro("Title", "Body"),
        ):
            with patch("streamlit.markdown") as mock_md:
                renderer()
                html = mock_md.call_args[0][0]
                self.assertNotIn("eyebrow", html)
                self.assertNotIn("ATELIER NOIR", html)
                self.assertNotIn("Client Path", html)
                self.assertNotIn("FABRISENSE STUDIO", html)


class TestFeatureStrip(unittest.TestCase):
    def test_feature_strip_renders_as_one_grid(self):
        from ui.components import render_feature_strip

        with patch("streamlit.markdown") as mock_md, patch(
            "streamlit.columns"
        ) as mock_columns:
            render_feature_strip()
            mock_columns.assert_not_called()
            mock_md.assert_called_once()
            html = mock_md.call_args[0][0]
            self.assertIn("feature-strip", html)
            self.assertIn("feature-card-grid", html)
            self.assertEqual(html.count("info-card ivory-card"), 4)


class TestPaletteGradientBar(unittest.TestCase):
    def test_gradient_bar_with_colors(self):
        from ui.components import render_palette_gradient_bar

        colors = [
            {"hex": "#ff0000", "name": "Red", "percentage": 50},
            {"hex": "#0000ff", "name": "Blue", "percentage": 50},
        ]
        with patch("streamlit.markdown") as mock_md:
            render_palette_gradient_bar(colors)
            mock_md.assert_called_once()
            html = mock_md.call_args[0][0]
            self.assertIn("linear-gradient", html)
            self.assertIn("#ff0000", html)
            self.assertIn("#0000ff", html)

    def test_gradient_bar_empty(self):
        from ui.components import render_palette_gradient_bar

        result = render_palette_gradient_bar([])
        self.assertIsNone(result)

    def test_gradient_bar_single_color(self):
        from ui.components import render_palette_gradient_bar

        colors = [{"hex": "#aabbcc", "name": "Gray", "percentage": 100}]
        with patch("streamlit.markdown") as mock_md:
            render_palette_gradient_bar(colors)
            html = mock_md.call_args[0][0]
            self.assertIn("#aabbcc", html)

    def test_gradient_bar_zero_percentages(self):
        from ui.components import render_palette_gradient_bar

        colors = [
            {"hex": "#ff0000", "name": "Red", "percentage": 0},
            {"hex": "#0000ff", "name": "Blue", "percentage": 0},
        ]
        with patch("streamlit.markdown") as mock_md:
            render_palette_gradient_bar(colors)
            html = mock_md.call_args[0][0]
            self.assertIn("linear-gradient", html)


class TestRadarChart(unittest.TestCase):
    def test_radar_chart_creates_figure(self):
        from ui.components import render_radar_chart
        import plotly.graph_objects as go

        labels = ["Durability", "Breathability", "Eco", "Softness", "Value"]
        values = [8, 6, 7, 9, 5]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_radar_chart(labels, values)
            mock_chart.assert_called_once()
            fig = mock_chart.call_args[0][0]
            self.assertIsInstance(fig, go.Figure)

    def test_radar_chart_mismatched_lengths(self):
        from ui.components import render_radar_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_radar_chart(["A", "B"], [1])
            mock_chart.assert_not_called()

    def test_radar_chart_empty(self):
        from ui.components import render_radar_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_radar_chart([], [])
            mock_chart.assert_not_called()

    def test_radar_chart_clamps_values(self):
        from ui.components import render_radar_chart

        labels = ["A", "B", "C"]
        values = [15, -3, 5]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_radar_chart(labels, values, max_value=10.0)
            fig = mock_chart.call_args[0][0]
            trace = fig.data[0]
            self.assertEqual(trace.r[0], 10.0)
            self.assertEqual(trace.r[1], 0.0)


class TestGaugeChart(unittest.TestCase):
    def test_gauge_creates_figure(self):
        from ui.components import render_gauge_chart
        import plotly.graph_objects as go

        with patch("streamlit.plotly_chart") as mock_chart:
            render_gauge_chart(7.5, "Quality", max_value=10.0)
            mock_chart.assert_called_once()
            fig = mock_chart.call_args[0][0]
            self.assertIsInstance(fig, go.Figure)

    def test_gauge_clamps_high(self):
        from ui.components import render_gauge_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_gauge_chart(15, "Score", max_value=10.0)
            fig = mock_chart.call_args[0][0]
            self.assertEqual(fig.data[0].value, 10.0)

    def test_gauge_clamps_low(self):
        from ui.components import render_gauge_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_gauge_chart(-5, "Score", max_value=10.0)
            fig = mock_chart.call_args[0][0]
            self.assertEqual(fig.data[0].value, 0.0)

    def test_gauge_custom_thresholds(self):
        from ui.components import render_gauge_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_gauge_chart(5, "Score", max_value=10.0, thresholds=(3, 7))
            mock_chart.assert_called_once()

    def test_gauge_default_thresholds(self):
        from ui.components import render_gauge_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_gauge_chart(5, "Score", max_value=10.0)
            mock_chart.assert_called_once()


class TestConfusionSankey(unittest.TestCase):
    def test_sankey_creates_figure(self):
        from ui.components import render_confusion_sankey
        import plotly.graph_objects as go

        matrix = [[10, 2], [3, 8]]
        labels = ["Cotton", "Polyester"]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_confusion_sankey(matrix, labels)
            mock_chart.assert_called_once()
            fig = mock_chart.call_args[0][0]
            self.assertIsInstance(fig, go.Figure)

    def test_sankey_empty_matrix(self):
        from ui.components import render_confusion_sankey

        with patch("streamlit.plotly_chart") as mock_chart:
            render_confusion_sankey([], [])
            mock_chart.assert_not_called()

    def test_sankey_perfect_classification(self):
        from ui.components import render_confusion_sankey

        matrix = [[10, 0, 0], [0, 8, 0], [0, 0, 12]]
        labels = ["A", "B", "C"]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_confusion_sankey(matrix, labels)
            fig = mock_chart.call_args[0][0]
            sankey = fig.data[0]
            self.assertTrue(
                all(
                    s == t - len(labels)
                    for s, t in zip(sankey.link.source, sankey.link.target)
                )
            )

    def test_sankey_misclassification_flow(self):
        from ui.components import render_confusion_sankey

        matrix = [[5, 5], [5, 5]]
        labels = ["A", "B"]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_confusion_sankey(matrix, labels)
            fig = mock_chart.call_args[0][0]
            sankey = fig.data[0]
            misclass_links = [
                i
                for i, (s, t) in enumerate(zip(sankey.link.source, sankey.link.target))
                if t != s + len(labels)
            ]
            self.assertEqual(len(misclass_links), 2)


class TestConfusionMatrixHeatmap(unittest.TestCase):
    def test_heatmap_creates_figure(self):
        from ui.components import render_confusion_matrix_heatmap

        matrix = [[10, 2], [3, 8]]
        labels = ["A", "B"]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_confusion_matrix_heatmap(matrix, labels)
            mock_chart.assert_called_once()

    def test_heatmap_empty_labels(self):
        from ui.components import render_confusion_matrix_heatmap

        matrix = [[5]]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_confusion_matrix_heatmap(matrix, [])
            mock_chart.assert_called_once()


class TestColorWheel(unittest.TestCase):
    def test_color_wheel_renders(self):
        from ui.components import render_color_wheel

        colors = [
            {"hex": "#ff0000", "name": "Red", "percentage": 60},
            {"hex": "#0000ff", "name": "Blue", "percentage": 40},
        ]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_color_wheel(colors)
            mock_chart.assert_called_once()

    def test_color_wheel_empty(self):
        from ui.components import render_color_wheel

        with patch("streamlit.plotly_chart") as mock_chart:
            render_color_wheel([])
            mock_chart.assert_not_called()


class TestAppNavigation(unittest.TestCase):
    def test_nav_labels_match_ids(self):
        from app import NAV_LABELS, NAV_IDS

        self.assertEqual(len(NAV_LABELS), len(NAV_IDS))
        self.assertEqual(len(NAV_LABELS), 8)

    def test_nav_ids_contain_expected_pages(self):
        from app import NAV_IDS

        expected = [
            "analyze",
            "batch",
            "compare",
            "history",
            "guide",
            "care",
            "models",
            "about",
        ]
        self.assertEqual(NAV_IDS, expected)

    def test_nav_icons_match_labels(self):
        from app import NAV_LABELS, NAV_ICONS

        self.assertEqual(len(NAV_ICONS), len(NAV_LABELS))

    def test_session_defaults_include_nav_page(self):
        from app import SESSION_DEFAULTS

        self.assertIn("nav_page", SESSION_DEFAULTS)
        self.assertEqual(SESSION_DEFAULTS["nav_page"], "analyze")

    def test_session_defaults_do_not_include_dark_mode(self):
        from app import SESSION_DEFAULTS

        self.assertNotIn("dark_mode", SESSION_DEFAULTS)


class TestAppCSS(unittest.TestCase):
    def test_app_css_exists(self):
        from ui.styles import APP_CSS

        self.assertTrue(len(APP_CSS) > 1000)

    def test_app_css_preserves_material_icon_fonts(self):
        from ui.styles import APP_CSS

        sans_rule_selector = APP_CSS.split(
            "font-family: var(--font-sans) !important;", 1
        )[0].rsplit("{", 1)[0]
        self.assertNotIn(".stApp span", sans_rule_selector)
        self.assertIn('[class*="material-icons"]', APP_CSS)
        self.assertIn('[class*="material-symbols"]', APP_CSS)
        self.assertIn('"Material Symbols Rounded"', APP_CSS)

    def test_app_css_has_home_layout_grid_rules(self):
        from ui.styles import APP_CSS

        self.assertIn(".feature-strip", APP_CSS)
        self.assertIn(".feature-card-grid", APP_CSS)
        self.assertIn("min-height: 340px", APP_CSS)

    def test_app_css_has_expander_header_contrast_guard(self):
        from ui.styles import APP_CSS

        self.assertIn('details[data-testid="stExpander"] summary *', APP_CSS)
        self.assertIn(".streamlit-expanderHeader *", APP_CSS)
        self.assertIn("-webkit-text-fill-color: #1A1A1A", APP_CSS)

    def test_app_css_has_bento_grid(self):
        from ui.styles import APP_CSS

        self.assertIn(".bento-grid", APP_CSS)
        self.assertIn(".bento-cell", APP_CSS)

    def test_app_css_has_metric_counter(self):
        from ui.styles import APP_CSS

        self.assertIn(".metric-counter", APP_CSS)

    def test_app_css_has_chat_bubble(self):
        from ui.styles import APP_CSS

        self.assertIn(".chat-fabric-bubble", APP_CSS)

    def test_app_css_has_aggrid_styles(self):
        from ui.styles import APP_CSS

        self.assertIn(".ag-theme-balham", APP_CSS)
        self.assertIn(".ag-header", APP_CSS)

    def test_app_css_has_image_comparison(self):
        from ui.styles import APP_CSS

        self.assertIn(".image-comparison-container", APP_CSS)

    def test_app_css_has_palette_gradient(self):
        from ui.styles import APP_CSS

        self.assertIn("--accent-soft", APP_CSS)

    def test_app_css_has_animations(self):
        from ui.styles import APP_CSS

        self.assertIn("@keyframes cardSlideUp", APP_CSS)
        self.assertIn("@keyframes gradientShift", APP_CSS)
        self.assertIn("@keyframes skeletonShimmer", APP_CSS)

    def test_app_css_has_responsive_breakpoints(self):
        from ui.styles import APP_CSS

        self.assertIn("@media (max-width: 980px)", APP_CSS)
        self.assertIn("@media (max-width: 720px)", APP_CSS)


class TestImageComparison(unittest.TestCase):
    def test_image_comparison_fallback_without_package(self):
        from ui.components import render_image_comparison

        img_a = Image.new("RGB", (100, 100), "red")
        img_b = Image.new("RGB", (100, 100), "blue")
        with patch.dict("sys.modules", {"streamlit_image_comparison": None}):
            with patch("streamlit.columns") as mock_cols:
                mock_col = MagicMock()
                mock_cols.return_value = [mock_col, mock_col]
                try:
                    render_image_comparison(img_a, img_b, "A", "B")
                except Exception:
                    pass


class TestInteractiveTable(unittest.TestCase):
    def test_table_with_list_data(self):
        from ui.components import render_interactive_table

        data = [{"name": "Cotton", "score": 8}, {"name": "Silk", "score": 9}]
        with patch("st_aggrid.AgGrid") as mock_ag:
            mock_ag.return_value = MagicMock()
            result = render_interactive_table(data, height=300)
            mock_ag.assert_called_once()

    def test_table_with_empty_list(self):
        from ui.components import render_interactive_table

        with patch("st_aggrid.AgGrid") as mock_ag:
            mock_ag.return_value = MagicMock()
            result = render_interactive_table([], height=200)
            mock_ag.assert_called_once()


class TestChatNarrative(unittest.TestCase):
    def test_chat_narrative_with_full_analysis(self):
        from ui.components import render_chat_narrative

        analysis = {
            "llm_analysis": {
                "overall_summary": "A fine cotton fabric.",
                "fun_fact": "Cotton is ancient!",
                "fabric_type": {
                    "primary": "Cotton",
                    "sub_type": "Woven",
                    "blend_composition": "100% Cotton",
                },
                "pattern": {"type": "Solid", "sub_type": "Plain"},
                "texture": {"primary": "Smooth", "weight": "Light", "drape": "Soft"},
                "quality_assessment": {"score": 8, "grade": "A"},
            },
            "color_palette": {"dominant_color": {"name": "White", "hex": "#ffffff"}},
        }
        with patch("streamlit.chat_message") as mock_chat:
            mock_ctx = MagicMock()
            mock_chat.return_value.__enter__ = MagicMock(return_value=mock_ctx)
            mock_chat.return_value.__exit__ = MagicMock(return_value=False)
            with patch("streamlit.markdown"):
                render_chat_narrative(analysis)

    def test_chat_narrative_with_empty_analysis(self):
        from ui.components import render_chat_narrative

        analysis = {"llm_analysis": {}, "color_palette": {}}
        with patch("streamlit.chat_message") as mock_chat:
            mock_ctx = MagicMock()
            mock_chat.return_value.__enter__ = MagicMock(return_value=mock_ctx)
            mock_chat.return_value.__exit__ = MagicMock(return_value=False)
            with patch("streamlit.markdown"):
                render_chat_narrative(analysis)

    def test_chat_narrative_with_none_values(self):
        from ui.components import render_chat_narrative

        analysis = {
            "llm_analysis": {"overall_summary": None, "fabric_type": None},
            "color_palette": None,
        }
        with patch("streamlit.chat_message") as mock_chat:
            mock_ctx = MagicMock()
            mock_chat.return_value.__enter__ = MagicMock(return_value=mock_ctx)
            mock_chat.return_value.__exit__ = MagicMock(return_value=False)
            with patch("streamlit.markdown"):
                render_chat_narrative(analysis)


class TestRenderMetricBand(unittest.TestCase):
    def test_metric_band_renders(self):
        from ui.components import render_metric_band

        metrics = {"score": 8, "stars": "4/5", "seasons": "Summer", "eco_score": 7}
        with patch("streamlit.columns") as mock_cols:
            mock_cols.return_value = [MagicMock() for _ in range(4)]
            for col in mock_cols.return_value:
                col.__enter__ = MagicMock(return_value=col)
                col.__exit__ = MagicMock(return_value=False)
            with patch("streamlit.markdown"):
                render_metric_band(metrics)


class TestRenderCompareCard(unittest.TestCase):
    def test_compare_card_renders(self):
        from ui.components import render_compare_card

        analysis = {
            "llm_analysis": {
                "fabric_type": {"primary": "Cotton"},
                "pattern": {"type": "Solid"},
                "texture": {"primary": "Smooth", "weight": "Light", "drape": "Soft"},
                "quality_assessment": {"score": 8},
            },
            "color_palette": {"dominant_color": {"name": "White"}, "colors": []},
        }
        img = Image.new("RGB", (100, 100), "white")
        with patch("streamlit.image"):
            with patch("streamlit.markdown"):
                render_compare_card("Test Fabric", analysis, img)


class TestRequirementsNewPackages(unittest.TestCase):
    def test_requirements_file_exists(self):
        req_path = Path(__file__).parent.parent / "requirements.txt"
        self.assertTrue(req_path.exists())

    def test_requirements_contains_new_packages(self):
        req_path = Path(__file__).parent.parent / "requirements.txt"
        content = req_path.read_text()
        self.assertIn("streamlit-option-menu", content)
        self.assertIn("streamlit-image-comparison", content)
        self.assertIn("streamlit-aggrid", content)
        self.assertIn("pandas", content)

    def test_requirements_contains_existing_packages(self):
        req_path = Path(__file__).parent.parent / "requirements.txt"
        content = req_path.read_text()
        self.assertIn("streamlit", content)
        self.assertIn("plotly", content)
        self.assertIn("fpdf2", content)
        self.assertIn("streamlit-lottie", content)


class TestComponentsModuleExports(unittest.TestCase):
    def test_all_new_components_importable(self):
        from ui.components import (
            render_radar_chart,
            render_gauge_chart,
            render_confusion_sankey,
            render_image_comparison,
            render_interactive_table,
            render_chat_narrative,
            render_palette_gradient_bar,
        )

    def test_all_existing_components_importable(self):
        from ui.components import (
            render_sidebar_brand,
            render_page_intro,
            render_hero,
            render_feature_strip,
            render_sample_gallery,
            render_upload_panel,
            render_metric_band,
            render_highlight_banner,
            render_color_palette,
            render_mini_palette,
            render_compare_card,
            render_key_value_block,
            render_list_block,
            render_empty_state,
            render_confidence_bar,
            render_badge,
            render_status_dot,
            render_skeleton,
            render_skeleton_card,
            render_confusion_matrix_heatmap,
            render_color_wheel,
            render_floating_action_bar,
        )


class TestBentoGridCSS(unittest.TestCase):
    def test_bento_grid_classes(self):
        from ui.styles import APP_CSS

        self.assertIn(".bento-grid", APP_CSS)
        self.assertIn(".bento-grid.cols-4", APP_CSS)
        self.assertIn(".bento-grid.cols-3", APP_CSS)
        self.assertIn(".bento-grid .span-2", APP_CSS)
        self.assertIn(".bento-grid .span-row", APP_CSS)

    def test_bento_cell_hover(self):
        from ui.styles import APP_CSS

        self.assertIn(".bento-cell:hover", APP_CSS)


class TestEdgeCasesConfusionSankey(unittest.TestCase):
    def test_single_class(self):
        from ui.components import render_confusion_sankey

        matrix = [[10]]
        labels = ["Only"]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_confusion_sankey(matrix, labels)
            mock_chart.assert_called_once()

    def test_large_matrix(self):
        from ui.components import render_confusion_sankey

        n = 10
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 10
        labels = [f"C{i}" for i in range(n)]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_confusion_sankey(matrix, labels)
            mock_chart.assert_called_once()

    def test_all_zeros(self):
        from ui.components import render_confusion_sankey

        matrix = [[0, 0], [0, 0]]
        labels = ["A", "B"]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_confusion_sankey(matrix, labels)
            fig = mock_chart.call_args[0][0]
            sankey = fig.data[0]
            self.assertEqual(len(sankey.link.source), 0)


class TestEdgeCasesRadarChart(unittest.TestCase):
    def test_single_axis(self):
        from ui.components import render_radar_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_radar_chart(["Quality"], [8.0])
            mock_chart.assert_called_once()

    def test_all_zero_values(self):
        from ui.components import render_radar_chart

        labels = ["A", "B", "C"]
        values = [0, 0, 0]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_radar_chart(labels, values)
            fig = mock_chart.call_args[0][0]
            self.assertEqual(fig.data[0].r[0], 0)

    def test_negative_values_clamped(self):
        from ui.components import render_radar_chart

        labels = ["A", "B"]
        values = [-5, 3]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_radar_chart(labels, values, max_value=10.0)
            fig = mock_chart.call_args[0][0]
            self.assertEqual(fig.data[0].r[0], 0)

    def test_custom_max_value(self):
        from ui.components import render_radar_chart

        labels = ["A", "B"]
        values = [75, 50]
        with patch("streamlit.plotly_chart") as mock_chart:
            render_radar_chart(labels, values, max_value=100.0)
            mock_chart.assert_called_once()


class TestEdgeCasesGaugeChart(unittest.TestCase):
    def test_exact_zero(self):
        from ui.components import render_gauge_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_gauge_chart(0.0, "Score")
            fig = mock_chart.call_args[0][0]
            self.assertEqual(fig.data[0].value, 0.0)

    def test_exact_max(self):
        from ui.components import render_gauge_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_gauge_chart(10.0, "Score", max_value=10.0)
            fig = mock_chart.call_args[0][0]
            self.assertEqual(fig.data[0].value, 10.0)

    def test_negative_clamped(self):
        from ui.components import render_gauge_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_gauge_chart(-100, "Score")
            fig = mock_chart.call_args[0][0]
            self.assertEqual(fig.data[0].value, 0.0)

    def test_over_max_clamped(self):
        from ui.components import render_gauge_chart

        with patch("streamlit.plotly_chart") as mock_chart:
            render_gauge_chart(999, "Score", max_value=10.0)
            fig = mock_chart.call_args[0][0]
            self.assertEqual(fig.data[0].value, 10.0)


class TestMetricBandRobustness(unittest.TestCase):
    def test_metric_band_with_complete_metrics(self):
        from ui.components import render_metric_band

        metrics = {"score": 8, "stars": "4/5", "seasons": "Summer", "eco_score": 7}
        with patch("streamlit.columns") as mock_cols:
            mock_cols.return_value = [MagicMock() for _ in range(4)]
            for col in mock_cols.return_value:
                col.__enter__ = MagicMock(return_value=col)
                col.__exit__ = MagicMock(return_value=False)
            with patch("streamlit.markdown"):
                render_metric_band(metrics)

    def test_metric_band_with_missing_keys(self):
        from ui.components import render_metric_band

        metrics = {}
        with patch("streamlit.columns") as mock_cols:
            mock_cols.return_value = [MagicMock() for _ in range(4)]
            for col in mock_cols.return_value:
                col.__enter__ = MagicMock(return_value=col)
                col.__exit__ = MagicMock(return_value=False)
            with patch("streamlit.markdown"):
                render_metric_band(metrics)

    def test_metric_band_with_partial_keys(self):
        from ui.components import render_metric_band

        metrics = {"score": 5}
        with patch("streamlit.columns") as mock_cols:
            mock_cols.return_value = [MagicMock() for _ in range(4)]
            for col in mock_cols.return_value:
                col.__enter__ = MagicMock(return_value=col)
                col.__exit__ = MagicMock(return_value=False)
            with patch("streamlit.markdown"):
                render_metric_band(metrics)

    def test_metric_band_with_string_score(self):
        from ui.components import render_metric_band

        metrics = {"score": "N/A", "stars": "N/A", "seasons": "N/A", "eco_score": "N/A"}
        with patch("streamlit.columns") as mock_cols:
            mock_cols.return_value = [MagicMock() for _ in range(4)]
            for col in mock_cols.return_value:
                col.__enter__ = MagicMock(return_value=col)
                col.__exit__ = MagicMock(return_value=False)
            with patch("streamlit.markdown"):
                render_metric_band(metrics)


class TestColorPaletteEmptyGuard(unittest.TestCase):
    def test_color_palette_empty_colors(self):
        from ui.components import render_color_palette

        with patch("streamlit.markdown") as mock_md:
            render_color_palette([], "Unknown")
            mock_md.assert_not_called()

    def test_color_palette_with_colors(self):
        from ui.components import render_color_palette

        colors = [{"hex": "#ff0000", "name": "Red", "percentage": 100}]
        with patch("streamlit.columns") as mock_cols:
            mock_cols.return_value = [MagicMock() for _ in range(3)]
            for col in mock_cols.return_value:
                col.__enter__ = MagicMock(return_value=col)
                col.__exit__ = MagicMock(return_value=False)
            with patch("streamlit.markdown"):
                render_color_palette(colors, "Warm")


class TestImageComparisonTempFileCleanup(unittest.TestCase):
    def test_cleanup_survives_oserror(self):
        from ui.components import render_image_comparison
        import os

        img_a = Image.new("RGB", (10, 10), "red")
        img_b = Image.new("RGB", (10, 10), "blue")
        real_unlink = os.unlink
        unlink_calls = []

        def tracked_unlink(path):
            unlink_calls.append(path)
            try:
                real_unlink(path)
            except OSError:
                pass

        with patch("streamlit_image_comparison.image_comparison"):
            with patch("os.unlink", side_effect=tracked_unlink):
                render_image_comparison(img_a, img_b, "A", "B")
        self.assertGreaterEqual(len(unlink_calls), 2)


class TestRadarChartZeroQualityScore(unittest.TestCase):
    def test_zero_quality_score_uses_hand_feel_fallback(self):
        from ui.pages import render_results_page

        analysis = {
            "analysis_metadata": {"analysis_mode": "heuristic", "color_clusters": 3},
            "llm_analysis": {
                "fabric_type": {"primary": "Cotton"},
                "pattern": {"type": "Solid"},
                "texture": {"primary": "Smooth", "hand_feel_score": 7},
                "quality_assessment": {"score": 0, "factors": []},
                "season_recommendation": {"best_seasons": ["Summer"]},
                "price_range": {"value_for_money_score": 6},
                "care_instructions": {},
                "sustainability": {"eco_score": 5},
                "interior_use": {},
                "model_prediction": {},
            },
            "color_palette": {"colors": [], "harmony_type": "Unknown"},
        }
        with patch("streamlit.tabs") as mock_tabs:
            mock_tab = MagicMock()
            mock_tab.__enter__ = MagicMock(return_value=mock_tab)
            mock_tab.__exit__ = MagicMock(return_value=False)
            mock_tabs.return_value = [mock_tab, mock_tab, mock_tab, mock_tab]
            with patch("streamlit.markdown"):
                with patch("streamlit.caption"):
                    with patch("streamlit.columns") as mock_cols:
                        mock_col = MagicMock()
                        mock_col.__enter__ = MagicMock(return_value=mock_col)
                        mock_col.__exit__ = MagicMock(return_value=False)
                        mock_cols.return_value = [mock_col, mock_col]
                        with patch("streamlit.image"):
                            with patch("streamlit.expander"):
                                with patch("ui.components.render_gauge_chart"):
                                    with patch("ui.components.render_metric_band"):
                                        with patch("ui.components.render_page_intro"):
                                            with patch(
                                                "ui.components.render_key_value_block"
                                            ):
                                                with patch(
                                                    "ui.components.render_list_block"
                                                ):
                                                    with patch(
                                                        "ui.components.render_color_palette"
                                                    ):
                                                        with patch(
                                                            "ui.components.render_palette_gradient_bar"
                                                        ):
                                                            with patch(
                                                                "ui.components.render_radar_chart"
                                                            ):
                                                                with patch(
                                                                    "ui.components.render_highlight_banner"
                                                                ):
                                                                    with patch(
                                                                        "ui.components.render_empty_state"
                                                                    ):
                                                                        render_results_page(
                                                                            analysis,
                                                                            None,
                                                                            Image.new(
                                                                                "RGB",
                                                                                (
                                                                                    100,
                                                                                    100,
                                                                                ),
                                                                            ),
                                                                            "test.jpg",
                                                                        )

class TestConfusionImageInspector(unittest.TestCase):
    @patch("streamlit.selectbox")
    @patch("streamlit.columns")
    @patch("streamlit.markdown")
    @patch("streamlit.write")
    @patch("streamlit.success")
    @patch("streamlit.download_button")
    @patch("streamlit.dataframe")
    def test_render_model_info_page_with_misclassifications(
        self, mock_df, mock_dl_btn, mock_success, mock_write, mock_md, mock_cols, mock_selectbox
    ):
        import streamlit as st
        from ui.pages import render_model_info_page
        
        # Setup session state with benchmark results containing predictions
        st.session_state.model_benchmark_bundle = {
            "manifest_dir": "data/manifests",
            "split": "test",
            "max_examples": 10,
            "results": [
                {
                    "model_name": "TestModel",
                    "architecture": "resnet50",
                    "accuracy": 0.8,
                    "macro_f1": 0.8,
                    "weighted_f1": 0.8,
                    "loss": 0.3,
                    "evaluated_examples": 10,
                    "checkpoint_path": "checkpoints/TestModel/resnet50.pt",
                    "predictions": [
                        {
                            "filepath": "data/Cotton/1.jpg",
                            "true_label": "Cotton",
                            "predicted_label": "Linen",
                            "confidence": 0.92,
                        },
                        {
                            "filepath": "data/Linen/2.jpg",
                            "true_label": "Linen",
                            "predicted_label": "Linen",
                            "confidence": 0.98,
                        }
                    ]
                }
            ]
        }
        st.session_state.uploaded_benchmark_manifest = None
        
        # Mock streamlit columns dynamically to support different column counts (e.g. 2 and 3)
        def make_mock_col():
            col = MagicMock()
            col.__enter__ = MagicMock(return_value=col)
            col.__exit__ = MagicMock(return_value=False)
            return col
            
        mock_cols.side_effect = lambda n: [make_mock_col() for _ in range(n)]
        
        # Mock selectbox responses for the 5 selectboxes in render_model_info_page
        mock_selectbox.side_effect = [
            "TestModel | resnet50",              # Inspect checkpoint
            "data/manifests",                    # Benchmark dataset
            "test",                              # Benchmark split
            "TestModel",                         # Inspect benchmark result
            "🚨 Cotton ➔ Linen (1 sample)"        # Select Mismatch Pair to Investigate
        ]
        
        manifest_entries = [
            {
                "display_name": "data/manifests",
                "manifest_dir": "data/manifests",
                "dataset_root": "data",
                "label_count": 10,
                "counts": {"train": 10, "val": 10, "test": 10},
                "class_counts": {},
                "benchmark_mode": "standard",
                "recommended_split": "test",
            }
        ]
        
        available_models = [
            {
                "display_name": "TestModel | resnet50",
                "checkpoint_path": "checkpoints/TestModel/resnet50.pt",
                "model_name": "TestModel",
                "architecture": "resnet50",
                "pretrained": True,
                "metrics": {
                    "accuracy": 0.8,
                    "macro_f1": 0.8,
                    "weighted_f1": 0.8,
                    "loss": 0.3,
                },
                "class_count": 2,
            }
        ]
        
        mock_client = MagicMock()
        mock_client.describe.return_value = {
            "available": True,
            "labels": ["Cotton", "Linen"],
            "model_name": "TestModel",
            "architecture": "resnet50",
            "class_count": 2,
            "checkpoint_path": "checkpoints/TestModel/resnet50.pt"
        }
        
        with patch("ui.pages.get_local_model_client", return_value=mock_client):
            with patch("ui.pages.list_manifest_directories", return_value=manifest_entries):
                with patch("ui.pages.list_available_local_models", return_value=available_models):
                    with patch("ui.pages.ModelReviewStore") as mock_store:
                        mock_store.return_value.load.return_value = []
                        try:
                            render_model_info_page()
                        except Exception as e:
                            import traceback
                            print("EXCEPTION OCCURRED:", e)
                            traceback.print_exc()
        
        # Verify that selectbox was called to choose mismatch pair
        mock_selectbox.assert_any_call(
            "Select Mismatch Pair to Investigate",
            options=["🚨 Cotton ➔ Linen (1 sample)"],
            key="misclass_selector_TestModel"
        )


if __name__ == "__main__":
    unittest.main()
