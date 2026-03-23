import unittest

from PIL import Image

from src.color_extractor import ColorExtractor


class ColorExtractorTests(unittest.TestCase):
    def test_extract_palette_returns_sorted_colors(self):
        image = Image.new("RGB", (60, 30))
        for x in range(60):
            for y in range(30):
                if x < 40:
                    image.putpixel((x, y), (200, 40, 40))
                else:
                    image.putpixel((x, y), (40, 40, 180))

        extractor = ColorExtractor(n_colors=2)
        palette = extractor.extract_palette(image)

        self.assertEqual(len(palette), 2)
        self.assertGreaterEqual(palette[0]["percentage"], palette[1]["percentage"])
        self.assertEqual(palette[0]["hex"], "#c82828")

    def test_get_color_harmony_detects_neutral_palette(self):
        extractor = ColorExtractor(n_colors=3)
        palette = [
            {"rgb": (120, 120, 120), "hex": "#787878", "percentage": 50, "name": "Gray"},
            {"rgb": (180, 180, 180), "hex": "#b4b4b4", "percentage": 30, "name": "Gray"},
            {"rgb": (80, 80, 80), "hex": "#505050", "percentage": 20, "name": "Gray"},
        ]

        harmony = extractor.get_color_harmony(palette)
        self.assertEqual(harmony, "Neutral")


if __name__ == "__main__":
    unittest.main()
