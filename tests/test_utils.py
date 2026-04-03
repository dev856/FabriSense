import unittest

from src.utils import (
    analysis_engine_label,
    classification_report_rows,
    compare_fabric_analyses,
    model_prediction_margin,
    model_prediction_warnings,
    summarize_analysis,
)


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
                "model_prediction": {
                    "label": "Cotton",
                    "confidence": 0.82,
                    "top_predictions": [
                        {"label": "Cotton", "confidence": 0.82},
                        {"label": "Linen", "confidence": 0.12},
                    ],
                    "model_name": "model_b_resnet18",
                    "architecture": "resnet18",
                },
                "overall_summary": "Test summary",
            },
            "analysis_metadata": {"analysis_mode": "trained"},
            "color_palette": {"dominant_color": {"name": "White"}},
        }

        summary = summarize_analysis(analysis, "sample.jpg")

        self.assertEqual(summary["engine"], "Locally trained model")
        self.assertEqual(summary["fabric"], "Cotton")
        self.assertEqual(summary["predicted_label"], "Cotton")
        self.assertEqual(summary["prediction_margin"], 0.7)
        self.assertEqual(summary["review_flag"], "")

    def test_model_prediction_warnings_flags_low_confidence_and_ambiguity(self):
        prediction = {
            "confidence": 0.41,
            "top_predictions": [
                {"label": "Cotton", "confidence": 0.41},
                {"label": "Linen", "confidence": 0.35},
            ],
        }

        warnings = model_prediction_warnings(prediction)

        self.assertEqual(model_prediction_margin(prediction), 0.06)
        self.assertEqual(len(warnings), 2)
        self.assertTrue(any("Low confidence" in item for item in warnings))
        self.assertTrue(any("close together" in item for item in warnings))

    def test_classification_report_rows_flattens_metrics(self):
        metrics = {
            "classification_report": {
                "Cotton": {"precision": 0.7, "recall": 0.8, "f1-score": 0.75, "support": 10},
                "macro avg": {"precision": 0.7, "recall": 0.8, "f1-score": 0.75, "support": 10},
                "accuracy": 0.75,
            }
        }

        rows = classification_report_rows(metrics)

        self.assertEqual(rows, [{"label": "Cotton", "precision": 0.7, "recall": 0.8, "f1_score": 0.75, "support": 10}])


if __name__ == "__main__":
    unittest.main()
