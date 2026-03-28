import unittest

from src.utils import analysis_engine_label, compare_fabric_analyses, summarize_analysis


class UtilsTests(unittest.TestCase):
    def test_compare_fabric_analyses_prefers_higher_quality_score(self):
        analysis_a = {
            "llm_analysis": {
                "fabric_type": {"primary": "Cotton Blend"},
                "pattern": {"type": "Solid"},
                "texture": {"weight": "Medium-weight"},
                "quality_assessment": {"score": 7.2},
                "price_range": {"category": "Mid-range"},
                "season_recommendation": {"best_seasons": ["Spring", "Summer"]},
            },
            "color_palette": {"dominant_color": {"name": "Blue"}},
        }
        analysis_b = {
            "llm_analysis": {
                "fabric_type": {"primary": "Denim"},
                "pattern": {"type": "Solid"},
                "texture": {"weight": "Heavyweight"},
                "quality_assessment": {"score": 8.4},
                "price_range": {"category": "Mid-range"},
                "season_recommendation": {"best_seasons": ["Spring", "Autumn"]},
            },
            "color_palette": {"dominant_color": {"name": "Navy"}},
        }

        result = compare_fabric_analyses(analysis_a, "Fabric A", analysis_b, "Fabric B")

        self.assertEqual(result["winner"], "Fabric B")
        self.assertIn("8.4", result["winner_reason"])
        self.assertTrue(result["similarities"])
        self.assertTrue(result["differences"])

    def test_analysis_engine_label_supports_trained_mode(self):
        self.assertEqual(analysis_engine_label("ai"), "AI-generated")
        self.assertEqual(analysis_engine_label("heuristic"), "Local heuristics")
        self.assertEqual(analysis_engine_label("trained"), "Locally trained model")

    def test_summarize_analysis_uses_engine_label_mapping(self):
        analysis = {
            "llm_analysis": {
                "fabric_type": {"primary": "Cotton"},
                "pattern": {"type": "Solid"},
                "texture": {"primary": "Smooth", "weight": "Lightweight"},
                "quality_assessment": {"score": 7.3},
                "price_range": {"category": "Mid-range"},
                "season_recommendation": {"best_seasons": ["Spring"]},
                "overall_summary": "Test summary",
            },
            "analysis_metadata": {"analysis_mode": "trained"},
            "color_palette": {"dominant_color": {"name": "White"}},
        }

        summary = summarize_analysis(analysis, "sample.jpg")

        self.assertEqual(summary["engine"], "Locally trained model")
        self.assertEqual(summary["fabric"], "Cotton")


if __name__ == "__main__":
    unittest.main()
