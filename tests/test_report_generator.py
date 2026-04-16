"""Tests for PDF report generation."""

from __future__ import annotations

import unittest

from PIL import Image

from src.report_generator import ReportGenerator


class ReportGeneratorTests(unittest.TestCase):
    def test_generate_pdf_with_local_model_evidence_and_long_checkpoint(self):
        analysis = {
            "analysis_metadata": {
                "analysis_mode": "trained",
                "color_clusters": 3,
            },
            "image_info": {
                "width": 640,
                "height": 480,
                "aspect_ratio": "4:3",
                "mode": "RGB",
            },
            "color_palette": {
                "harmony_type": "Analogous",
                "dominant_color": {"name": "Navy", "hex": "#102040"},
                "colors": [
                    {"name": "Navy", "hex": "#102040", "percentage": 70},
                    {"name": "Blue", "hex": "#224488", "percentage": 30},
                ],
            },
            "llm_analysis": {
                "overall_summary": "Locally trained model prediction suggests cotton.",
                "fabric_type": {
                    "primary": "Cotton",
                    "sub_type": "Locally trained model prediction",
                    "blend_composition": "Image-only prediction.",
                    "confidence": "medium (77.0%)",
                },
                "pattern": {
                    "type": "Solid",
                    "sub_type": "Minimal tonal variation",
                    "pattern_scale": "small",
                    "pattern_repeat": "none",
                    "description": "Local surface read.",
                },
                "texture": {
                    "primary": "Smooth",
                    "hand_feel": "Soft and even",
                    "weight": "Lightweight",
                    "drape": "Fluid",
                    "sheen": "Matte",
                },
                "quality_assessment": {
                    "score": 7.2,
                    "out_of": 10,
                    "grade": "B",
                    "durability_estimate": "Medium",
                    "pilling_tendency": "Low",
                    "factors": ["Exposure looks balanced."],
                },
                "care_instructions": {
                    "washing": "Machine wash cold.",
                    "drying": "Line dry.",
                    "ironing": "Low heat.",
                    "special_care": "Test heat first.",
                    "dry_clean_recommended": False,
                    "bleach_safe": False,
                },
                "season_recommendation": {
                    "best_seasons": ["Spring", "Summer"],
                    "avoid_seasons": ["Winter"],
                    "climate_suitability": "Warm weather",
                    "breathability": "High",
                },
                "price_range": {
                    "category": "Mid-range",
                    "estimated_per_meter_usd": "$12-28",
                    "estimated_per_meter_inr": "1000-2300",
                    "value_for_money": "Good",
                },
                "sustainability": {
                    "eco_score": 7,
                    "out_of": 10,
                    "environmental_impact": "Medium",
                    "biodegradable": True,
                    "recyclable": True,
                    "notes": "Likely natural-fiber component.",
                },
                "occasion_suitability": [
                    {
                        "occasion": "Casual",
                        "suitability_score": 8,
                        "note": "Good daily wear.",
                    }
                ],
                "styling_suggestions": [
                    {
                        "garment": "Shirt",
                        "style": "Clean finish",
                        "target_audience": "Everyday wear",
                    }
                ],
                "interior_use": {
                    "suitable": True,
                    "notes": "Works for lightweight accents.",
                    "suggestions": ["Curtain panels"],
                },
                "fun_fact": "Cotton is widely used.",
                "model_prediction": {
                    "label": "Cotton",
                    "confidence": 0.77,
                    "model_name": "model_with_a_very_long_name_for_pdf_layout_testing",
                    "architecture": "resnet18",
                    "checkpoint_path": (
                        "D:/projects/FabriSense/fabrisense/artifacts/models/"
                        "model_b_resnet18_v2/checkpoints/"
                        "best_checkpoint_with_a_very_long_unbroken_filename_for_testing.pth"
                    ),
                    "top_predictions": [
                        {"label": "Cotton", "confidence": 0.77},
                        {"label": "Linen", "confidence": 0.12},
                    ],
                },
            },
        }

        pdf_bytes = ReportGenerator().generate_pdf(
            analysis, Image.new("RGB", (640, 480), "navy")
        )

        self.assertGreater(len(pdf_bytes), 1000)
        self.assertEqual(pdf_bytes[:4], b"%PDF")


if __name__ == "__main__":
    unittest.main()
