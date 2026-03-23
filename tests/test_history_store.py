import unittest
from pathlib import Path

from src.history_store import HistoryStore
from src.utils import analyses_to_csv, summarize_analysis


class HistoryStoreTests(unittest.TestCase):
    def test_append_and_load_history(self):
        path = Path("data/test_history_store.json")
        if path.exists():
            path.unlink()
        store = HistoryStore(path)
        store.append({"image_name": "one.jpg", "fabric": "Cotton"})
        store.append({"image_name": "two.jpg", "fabric": "Denim"})

        history = store.load()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["image_name"], "two.jpg")
        if path.exists():
            path.unlink()

    def test_analyses_to_csv_outputs_headers(self):
        csv_bytes = analyses_to_csv([
            {"image_name": "one.jpg", "fabric": "Cotton", "quality_score": 7.2},
            {"image_name": "two.jpg", "fabric": "Denim", "quality_score": 8.1},
        ])

        text = csv_bytes.decode("utf-8")
        self.assertIn("image_name", text)
        self.assertIn("Denim", text)

    def test_summarize_analysis_returns_flat_row(self):
        analysis = {
            "analysis_metadata": {"analysis_mode": "local"},
            "llm_analysis": {
                "fabric_type": {"primary": "Cotton Blend"},
                "pattern": {"type": "Solid"},
                "texture": {"primary": "Smooth", "weight": "Lightweight"},
                "quality_assessment": {"score": 7.8},
                "price_range": {"category": "Mid-range"},
                "season_recommendation": {"best_seasons": ["Spring", "Summer"]},
                "overall_summary": "A clean casual fabric.",
            },
            "color_palette": {"dominant_color": {"name": "Blue"}},
        }

        row = summarize_analysis(analysis, "sample.jpg")

        self.assertEqual(row["image_name"], "sample.jpg")
        self.assertEqual(row["fabric"], "Cotton Blend")
        self.assertEqual(row["engine"], "Local heuristics")


if __name__ == "__main__":
    unittest.main()