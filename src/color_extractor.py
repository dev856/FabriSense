"""Dominant color extraction and harmony classification."""

from __future__ import annotations

import colorsys
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image

try:
    from sklearn.cluster import KMeans
except ImportError:  # pragma: no cover - depends on local environment
    KMeans = None


class ColorExtractor:
    """Extract a dominant palette using k-means clustering."""

    COLOR_NAMES = {
        (255, 0, 0): "Red",
        (0, 255, 0): "Green",
        (0, 0, 255): "Blue",
        (255, 255, 0): "Yellow",
        (255, 165, 0): "Orange",
        (128, 0, 128): "Purple",
        (255, 192, 203): "Pink",
        (165, 42, 42): "Brown",
        (0, 0, 0): "Black",
        (255, 255, 255): "White",
        (128, 128, 128): "Gray",
        (0, 128, 128): "Teal",
        (0, 0, 128): "Navy",
        (245, 245, 220): "Beige",
        (128, 0, 0): "Maroon",
        (0, 128, 0): "Dark Green",
        (75, 0, 130): "Indigo",
        (255, 127, 80): "Coral",
        (64, 224, 208): "Turquoise",
        (218, 165, 32): "Gold",
        (240, 230, 140): "Khaki",
        (230, 230, 250): "Lavender",
        (244, 164, 96): "Sandy Brown",
        (47, 79, 79): "Dark Slate",
        (210, 105, 30): "Chocolate",
        (178, 34, 34): "Firebrick",
    }

    def __init__(self, n_colors: int = 6):
        self.n_colors = n_colors

    def extract_palette(self, image: Image.Image) -> List[Dict]:
        img_small = image.copy()
        img_small.thumbnail((240, 240), Image.Resampling.LANCZOS)
        pixels = np.array(img_small).reshape(-1, 3)

        mask = np.all(pixels > 10, axis=1) & np.all(pixels < 245, axis=1)
        filtered_pixels = pixels[mask]
        if len(filtered_pixels) < 100:
            filtered_pixels = pixels

        unique_pixels = np.unique(filtered_pixels, axis=0)
        if len(unique_pixels) == 0:
            return []

        if KMeans is None:
            return self._extract_palette_without_sklearn(filtered_pixels, unique_pixels)

        n_clusters = min(self.n_colors, len(unique_pixels))
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10,
            max_iter=300,
        )
        kmeans.fit(filtered_pixels)

        colors = np.rint(kmeans.cluster_centers_).astype(int)
        labels = kmeans.labels_
        counts = Counter(labels)
        total_pixels = len(labels)

        palette: List[Dict] = []
        for idx, color in enumerate(colors):
            r, g, b = map(int, color)
            palette.append(
                {
                    "rgb": (r, g, b),
                    "hex": f"#{r:02x}{g:02x}{b:02x}",
                    "percentage": round((counts[idx] / total_pixels) * 100, 1),
                    "name": self._closest_color_name((r, g, b)),
                }
            )

        palette.sort(key=lambda item: item["percentage"], reverse=True)
        return palette

    def _extract_palette_without_sklearn(self, pixels: np.ndarray, unique_pixels: np.ndarray) -> List[Dict]:
        if len(unique_pixels) <= self.n_colors:
            counts = Counter(map(tuple, pixels.tolist()))
        else:
            quantized = (pixels // 16) * 16
            counts = Counter(map(tuple, quantized.tolist()))

        total = sum(counts.values())
        palette: List[Dict] = []
        for color, count in counts.most_common(self.n_colors):
            r, g, b = map(int, color)
            palette.append(
                {
                    "rgb": (r, g, b),
                    "hex": f"#{r:02x}{g:02x}{b:02x}",
                    "percentage": round((count / total) * 100, 1),
                    "name": self._closest_color_name((r, g, b)),
                }
            )
        return palette

    def _closest_color_name(self, rgb: Tuple[int, int, int]) -> str:
        min_distance = float("inf")
        closest_name = "Unknown"
        for reference, name in self.COLOR_NAMES.items():
            distance = sum((a - b) ** 2 for a, b in zip(rgb, reference)) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        return closest_name

    def get_color_harmony(self, palette: List[Dict]) -> str:
        if len(palette) < 2:
            return "Monochromatic"

        hues: List[float] = []
        saturations: List[float] = []
        for color in palette[:4]:
            r, g, b = color["rgb"]
            hue, saturation, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            hues.append(hue * 360)
            saturations.append(saturation * 100)

        if float(np.mean(saturations)) < 12:
            return "Neutral"

        hue_range = max(hues) - min(hues)
        if hue_range < 20:
            return "Monochromatic"
        if hue_range < 60:
            return "Analogous"
        if 90 <= hue_range <= 150:
            return "Triadic"
        if 150 < hue_range < 230:
            return "Complementary"
        return "Mixed"
