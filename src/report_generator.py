"""PDF report generation for FabriSense analysis results."""

from __future__ import annotations

import os
import tempfile
from datetime import datetime
from typing import Any, Dict, Iterable

try:
    from fpdf import FPDF
except ImportError:  # pragma: no cover - depends on local environment
    FPDF = None
from PIL import Image

from src.utils import analysis_engine_label


class ReportGenerator:
    """Build a richer PDF report for FabriSense analysis results."""

    def generate_pdf(self, analysis: Dict[str, Any], image: Image.Image) -> bytes:
        if FPDF is None:
            raise RuntimeError("fpdf2 is not installed. Install requirements.txt to enable PDF export.")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        llm = analysis.get("llm_analysis", {})
        metadata = analysis.get("analysis_metadata", {})
        image_info = analysis.get("image_info", {})
        palette_block = analysis.get("color_palette", {})
        palette = palette_block.get("colors", [])

        engine = analysis_engine_label(metadata.get("analysis_mode"))
        dominant = palette_block.get("dominant_color", {}) or {}

        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(195, 91, 44)
        pdf.cell(0, 14, "FabriSense Material Report", new_x="LMARGIN", new_y="NEXT", align="C")

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(96, 90, 84)
        pdf.cell(
            0,
            7,
            f"Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )
        pdf.cell(
            0,
            6,
            self._sanitize_text(f"Mode: {metadata.get('analysis_mode', 'unknown')} | Engine: {engine}"),
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )
        pdf.ln(4)

        image_path = self._write_temp_image(image)
        try:
            x_center = (210 - 84) / 2
            pdf.image(image_path, x=x_center, w=84)
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)
        pdf.ln(6)

        self._section(pdf, "Executive Summary")
        self._highlight_box(pdf, llm.get("overall_summary", "No summary available."))

        fabric = llm.get("fabric_type", {})
        pattern = llm.get("pattern", {})
        texture = llm.get("texture", {})
        quality = llm.get("quality_assessment", {})
        care = llm.get("care_instructions", {})
        season = llm.get("season_recommendation", {})
        price = llm.get("price_range", {})
        sustainability = llm.get("sustainability", {})
        interior = llm.get("interior_use", {})
        model_prediction = llm.get("model_prediction", {}) or {}

        self._section(pdf, "Material Snapshot")
        self._key_value_lines(
            pdf,
            [
                ("Primary fabric", fabric.get("primary", "N/A")),
                ("Subtype", fabric.get("sub_type", "N/A")),
                ("Estimated blend", fabric.get("blend_composition", "N/A")),
                ("Confidence", fabric.get("confidence", "N/A")),
                ("Pattern", f"{pattern.get('type', 'N/A')} / {pattern.get('sub_type', 'N/A')}"),
                ("Pattern scale", pattern.get("pattern_scale", "N/A")),
                ("Pattern repeat", pattern.get("pattern_repeat", "N/A")),
                ("Texture", texture.get("primary", "N/A")),
                ("Hand feel", texture.get("hand_feel", "N/A")),
                ("Weight", texture.get("weight", "N/A")),
                ("Drape", texture.get("drape", "N/A")),
                ("Sheen", texture.get("sheen", "N/A")),
            ],
        )
        self._paragraph(pdf, f"Pattern notes: {pattern.get('description', 'N/A')}")

        if model_prediction:
            self._section(pdf, "Local Model Evidence")
            self._key_value_lines(
                pdf,
                [
                    ("Predicted label", model_prediction.get("label", "N/A")),
                    (
                        "Confidence",
                        f"{round(float(model_prediction.get('confidence', 0) or 0) * 100, 1)}%",
                    ),
                    ("Architecture", model_prediction.get("architecture", "N/A")),
                    ("Model name", model_prediction.get("model_name", "N/A")),
                    ("Checkpoint", model_prediction.get("checkpoint_path", "N/A")),
                ],
            )
            top_predictions = model_prediction.get("top_predictions", []) or []
            if top_predictions:
                self._bullet_lines(
                    pdf,
                    [
                        f"{item.get('label', 'N/A')}: {round(float(item.get('confidence', 0) or 0) * 100, 1)}%"
                        for item in top_predictions[:5]
                    ],
                    fallback=None,
                )

        self._section(pdf, "Visual Quality Review")
        self._key_value_lines(
            pdf,
            [
                ("Quality score", f"{quality.get('score', 'N/A')} / {quality.get('out_of', 10)}"),
                ("Grade", quality.get("grade", "N/A")),
                ("Durability", quality.get("durability_estimate", "N/A")),
                ("Pilling tendency", quality.get("pilling_tendency", "N/A")),
            ],
        )
        self._bullet_lines(pdf, quality.get("factors", []), fallback="No specific quality factors supplied.")

        self._section(pdf, "Color Direction")
        self._key_value_lines(
            pdf,
            [
                ("Harmony", palette_block.get("harmony_type", "Unknown")),
                ("Dominant color", f"{dominant.get('name', 'N/A')} {dominant.get('hex', '')}".strip()),
            ],
        )
        self._color_rows(pdf, palette[:6])

        self._section(pdf, "Care and Handling")
        self._key_value_lines(
            pdf,
            [
                ("Washing", care.get("washing", "N/A")),
                ("Drying", care.get("drying", "N/A")),
                ("Ironing", care.get("ironing", "N/A")),
                ("Special care", care.get("special_care", "N/A")),
                ("Dry clean recommended", self._yes_no(care.get("dry_clean_recommended"))),
                ("Bleach safe", self._yes_no(care.get("bleach_safe"))),
            ],
        )

        self._section(pdf, "Commercial Fit")
        self._key_value_lines(
            pdf,
            [
                ("Best seasons", self._list_text(season.get("best_seasons", []))),
                ("Avoid seasons", self._list_text(season.get("avoid_seasons", []))),
                ("Climate suitability", season.get("climate_suitability", "N/A")),
                ("Breathability", season.get("breathability", "N/A")),
                ("Price tier", price.get("category", "N/A")),
                ("Estimated USD per meter", price.get("estimated_per_meter_usd", "N/A")),
                ("Estimated INR per meter", price.get("estimated_per_meter_inr", "N/A")),
                ("Value for money", price.get("value_for_money", "N/A")),
                ("Eco score", f"{sustainability.get('eco_score', 'N/A')} / {sustainability.get('out_of', 10)}"),
                ("Environmental impact", sustainability.get("environmental_impact", "N/A")),
                ("Biodegradable", self._yes_no(sustainability.get("biodegradable"))),
                ("Recyclable", self._yes_no(sustainability.get("recyclable"))),
            ],
        )
        self._paragraph(pdf, f"Sustainability notes: {sustainability.get('notes', 'N/A')}")

        self._section(pdf, "Recommended Uses")
        self._bullet_lines(
            pdf,
            [
                f"{item.get('occasion', 'N/A')} ({item.get('suitability_score', 'N/A')}/10): {item.get('note', 'N/A')}"
                for item in llm.get("occasion_suitability", [])
            ],
            fallback="No occasion recommendations available.",
        )
        self._bullet_lines(
            pdf,
            [
                f"{item.get('garment', 'N/A')}: {item.get('style', 'N/A')} for {item.get('target_audience', 'N/A')}"
                for item in llm.get("styling_suggestions", [])
            ],
            fallback="No styling suggestions available.",
        )
        interior_label = "Suitable" if interior.get("suitable") else "Limited suitability"
        self._paragraph(pdf, f"Interior application: {interior_label}. {interior.get('notes', 'N/A')}")
        self._bullet_lines(pdf, interior.get("suggestions", []), fallback="No interior suggestions available.")

        self._section(pdf, "Reference Metadata")
        self._key_value_lines(
            pdf,
            [
                ("Image size", f"{image_info.get('width', 'N/A')} x {image_info.get('height', 'N/A')}"),
                ("Aspect ratio", image_info.get("aspect_ratio", "N/A")),
                ("Color mode", image_info.get("mode", "N/A")),
                ("Color clusters", metadata.get("color_clusters", "N/A")),
                ("Fun fact", llm.get("fun_fact", "N/A")),
            ],
        )

        pdf.ln(6)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 5, "Generated by FabriSense for reference and review workflows.", align="C")

        output = pdf.output()
        if isinstance(output, bytearray):
            return bytes(output)
        if isinstance(output, bytes):
            return output
        return output.encode("latin-1")

    def _write_temp_image(self, image: Image.Image) -> str:
        copy = image.copy()
        copy.thumbnail((900, 900), Image.Resampling.LANCZOS)
        handle = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        handle.close()
        copy.save(handle.name, format="JPEG", quality=92)
        return handle.name

    def _section(self, pdf: FPDF, title: str) -> None:
        self._reset_x(pdf)
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(195, 91, 44)
        pdf.cell(self._text_width(pdf), 9, self._sanitize_text(title), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(195, 91, 44)
        y = pdf.get_y()
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(2)

    def _highlight_box(self, pdf: FPDF, text: str) -> None:
        self._reset_x(pdf)
        pdf.set_fill_color(250, 238, 225)
        pdf.set_draw_color(227, 196, 167)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(self._text_width(pdf), 7, self._sanitize_text(text), border=1, fill=True)
        pdf.set_xy(x, max(y, pdf.get_y()))

    def _key_value_lines(self, pdf: FPDF, rows: Iterable[tuple[str, Any]]) -> None:
        for label, value in rows:
            self._line(pdf, f"{label}: {value}")

    def _line(self, pdf: FPDF, text: str) -> None:
        self._reset_x(pdf)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(45, 45, 45)
        pdf.multi_cell(self._text_width(pdf), 6, self._sanitize_text(text))

    def _paragraph(self, pdf: FPDF, text: str) -> None:
        self._reset_x(pdf)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(45, 45, 45)
        pdf.multi_cell(self._text_width(pdf), 6, self._sanitize_text(text))

    def _bullet_lines(self, pdf: FPDF, items: Iterable[str], fallback: str | None = None) -> None:
        values = [item for item in items if item]
        if not values and fallback:
            values = [fallback]
        for item in values:
            self._paragraph(pdf, f"- {item}")

    def _color_rows(self, pdf: FPDF, colors: Iterable[Dict[str, Any]]) -> None:
        for color in colors:
            self._reset_x(pdf)
            hex_code = color.get("hex", "#000000")
            red, green, blue = self._hex_to_rgb(hex_code)
            start_x = pdf.get_x()
            start_y = pdf.get_y() + 1
            pdf.set_fill_color(red, green, blue)
            pdf.rect(start_x, start_y, 8, 8, style="F")
            pdf.set_draw_color(215, 205, 193)
            pdf.rect(start_x, start_y, 8, 8)
            pdf.set_xy(start_x + 12, start_y - 1)
            self._line(
                pdf,
                f"{color.get('name', 'Unknown')} {hex_code} ({color.get('percentage', 'N/A')}%)",
            )

    def _reset_x(self, pdf: FPDF) -> None:
        pdf.set_x(pdf.l_margin)

    def _text_width(self, pdf: FPDF) -> float:
        return pdf.w - pdf.l_margin - pdf.r_margin

    def _yes_no(self, value: Any) -> str:
        if value is True:
            return "Yes"
        if value is False:
            return "No"
        return "N/A"

    def _list_text(self, values: Iterable[str]) -> str:
        values_list = [value for value in values if value]
        return ", ".join(values_list) if values_list else "N/A"

    def _hex_to_rgb(self, value: str) -> tuple[int, int, int]:
        cleaned = value.lstrip("#")
        if len(cleaned) != 6:
            return 0, 0, 0
        return int(cleaned[0:2], 16), int(cleaned[2:4], 16), int(cleaned[4:6], 16)

    def _sanitize_text(self, value: Any) -> str:
        text = str(value or "")
        replacements = {
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2013": "-",
            "\u2014": "-",
            "\u2022": "-",
            "\u2026": "...",
            "\xa0": " ",
        }
        for source, target in replacements.items():
            text = text.replace(source, target)
        return text.encode("latin-1", errors="ignore").decode("latin-1")



