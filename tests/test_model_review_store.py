import unittest
from pathlib import Path

from src.model_review_store import ModelReviewStore


class ModelReviewStoreTests(unittest.TestCase):
    def test_append_and_load_reviews(self):
        path = Path("data/test_model_review_store.json")
        if path.exists():
            path.unlink()

        store = ModelReviewStore(path)
        store.append({"image_name": "one.jpg", "predicted_label": "Cotton", "corrected_label": "Cotton"})
        store.append({"image_name": "two.jpg", "predicted_label": "Denim", "corrected_label": "Denim"})

        reviews = store.load()

        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews[0]["image_name"], "two.jpg")

        if path.exists():
            path.unlink()


if __name__ == "__main__":
    unittest.main()
