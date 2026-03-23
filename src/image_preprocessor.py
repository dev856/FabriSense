"""Image validation, preparation, and conversion helpers."""

from __future__ import annotations

import base64
import io
from typing import BinaryIO, Optional, Tuple

import numpy as np
from PIL import Image, ImageEnhance


class ImagePreprocessor:
    """Handle image validation and transformations before analysis."""

    SUPPORTED_FORMATS = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}
    MAX_FILE_SIZE_MB = 10
    TARGET_SIZE = (512, 512)
    DISPLAY_MAX_SIZE = (900, 900)

    @staticmethod
    def validate_image(uploaded_file: Optional[BinaryIO]) -> Tuple[bool, str]:
        if uploaded_file is None:
            return False, "No file uploaded."

        name = getattr(uploaded_file, "name", "")
        size = getattr(uploaded_file, "size", None)

        if size is not None:
            file_size_mb = size / (1024 * 1024)
            if file_size_mb > ImagePreprocessor.MAX_FILE_SIZE_MB:
                return (
                    False,
                    f"File too large ({file_size_mb:.1f} MB). Max allowed is {ImagePreprocessor.MAX_FILE_SIZE_MB} MB.",
                )

        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        if ext not in ImagePreprocessor.SUPPORTED_FORMATS:
            supported = ", ".join(sorted(ImagePreprocessor.SUPPORTED_FORMATS))
            return False, f"Unsupported format '.{ext}'. Supported formats: {supported}."

        try:
            image = Image.open(uploaded_file)
            image.verify()
            if hasattr(uploaded_file, "seek"):
                uploaded_file.seek(0)
            return True, "Image is valid."
        except Exception as exc:
            return False, f"Corrupted or invalid image file: {exc}"

    @staticmethod
    def load_image(uploaded_file: BinaryIO) -> Image.Image:
        image = Image.open(uploaded_file)
        if image.mode != "RGB":
            image = image.convert("RGB")
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        return image

    @staticmethod
    def resize_for_analysis(
        image: Image.Image,
        target_size: Tuple[int, int] | None = None,
        background_color: Tuple[int, int, int] = (247, 241, 231),
    ) -> Image.Image:
        target = target_size or ImagePreprocessor.TARGET_SIZE
        frame = image.copy()
        frame.thumbnail(target, Image.Resampling.LANCZOS)

        canvas = Image.new("RGB", target, background_color)
        x_offset = (target[0] - frame.width) // 2
        y_offset = (target[1] - frame.height) // 2
        canvas.paste(frame, (x_offset, y_offset))
        return canvas

    @staticmethod
    def resize_for_display(image: Image.Image) -> Image.Image:
        display = image.copy()
        display.thumbnail(ImagePreprocessor.DISPLAY_MAX_SIZE, Image.Resampling.LANCZOS)
        return display

    @staticmethod
    def enhance_image(image: Image.Image) -> Image.Image:
        sharpened = ImageEnhance.Sharpness(image).enhance(1.25)
        contrasted = ImageEnhance.Contrast(sharpened).enhance(1.08)
        saturated = ImageEnhance.Color(contrasted).enhance(1.05)
        return saturated

    @staticmethod
    def image_to_base64(image: Image.Image) -> str:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=92)
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")

    @staticmethod
    def image_to_bytes(image: Image.Image) -> bytes:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=92)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def get_image_cv2(image: Image.Image) -> np.ndarray:
        rgb = np.array(image)
        return rgb[:, :, ::-1].copy()

    @staticmethod
    def get_image_info(image: Image.Image) -> dict:
        return {
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "aspect_ratio": round(image.width / image.height, 2) if image.height else None,
        }
