import unittest

from PIL import Image

from src.analyzer import FabricAnalyzer


class DummyLLMClient:
    provider = "mock"

    def analyze_image(self, image, prompt):
        return {
            "fabric_type": {
                "primary": "Cotton",
                "sub_type": "Plain Weave",
                "blend_composition": "100% Cotton",
                "confidence": "high",
            },
            "pattern": {
                "type": "Solid",
                "sub_type": "None",
                "pattern_scale": "small",
                "pattern_repeat": "none",
                "description": "Uniform surface with no print",
            },
            "texture": {
                "primary": "Smooth",
                "hand_feel": "Soft",
                "weight": "Medium-weight",
                "drape": "Semi-structured",
                "sheen": "Matte",
            },
            "quality_assessment": {
                "score": 8.0,
                "out_of": 10,
                "grade": "A",
                "factors": ["Even weave", "Clean finish"],
                "durability_estimate": "High",
                "pilling_tendency": "Low",
            },
            "care_instructions": {
                "washing": "Machine wash cold",
                "drying": "Tumble dry low",
                "ironing": "Warm iron",
                "special_care": "Wash dark colors separately",
                "dry_clean_recommended": False,
                "bleach_safe": False,
            },
            "occasion_suitability": [{"occasion": "Casual", "suitability_score": 8, "note": "Easy everyday wear"}],
            "season_recommendation": {
                "best_seasons": ["Spring", "Summer"],
                "avoid_seasons": ["Winter"],
                "climate_suitability": "Warm climates",
                "breathability": "High",
            },
            "price_range": {
                "category": "Mid-range",
                "estimated_per_meter_usd": "$12-18",
                "estimated_per_meter_inr": "1000-1500",
                "value_for_money": "Good",
            },
            "sustainability": {
                "eco_score": 7,
                "out_of": 10,
                "biodegradable": True,
                "recyclable": True,
                "environmental_impact": "Medium",
                "notes": "Natural fiber with moderate processing impact",
            },
            "styling_suggestions": [{"garment": "Shirt", "style": "Relaxed casual", "target_audience": "Unisex"}],
            "interior_use": {
                "suitable": True,
                "suggestions": ["Pillow covers"],
                "notes": "Good for low-friction decor use",
            },
            "fun_fact": "Cotton fibers are naturally breathable.",
            "overall_summary": "A versatile cotton fabric with balanced weight and practical care requirements.",
        }


class FabricAnalyzerTests(unittest.TestCase):
    def test_analyze_combines_llm_and_cv_results(self):
        image = Image.new("RGB", (100, 100), (180, 80, 60))
        analyzer = FabricAnalyzer(llm_client=DummyLLMClient())

        result = analyzer.analyze(image)

        self.assertIn("llm_analysis", result)
        self.assertIn("color_palette", result)
        self.assertEqual(result["analysis_metadata"]["model_used"], "mock")
        self.assertEqual(result["llm_analysis"]["fabric_type"]["primary"], "Cotton")
        self.assertTrue(result["color_palette"]["colors"])

    def test_local_analysis_runs_without_llm_setup(self):
        image = Image.new("RGB", (120, 90), (55, 88, 140))
        analyzer = FabricAnalyzer()

        result = analyzer.analyze(image, mode="local")

        self.assertEqual(result["analysis_metadata"]["analysis_mode"], "local")
        self.assertEqual(result["analysis_metadata"]["model_used"], "local-heuristics")
        self.assertIn("quality_assessment", result["llm_analysis"])
        self.assertIn("overall_summary", result["llm_analysis"])


if __name__ == "__main__":
    unittest.main()
