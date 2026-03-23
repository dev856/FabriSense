import io
import unittest

from PIL import Image

from src.image_preprocessor import ImagePreprocessor


class ImagePreprocessorTests(unittest.TestCase):
    def _make_upload(self, image_format="PNG", size=(40, 20)):
        image = Image.new("RGB", size, (120, 90, 60))
        buffer = io.BytesIO()
        image.save(buffer, format=image_format)
        buffer.name = f"sample.{image_format.lower()}"
        buffer.size = len(buffer.getvalue())
        buffer.seek(0)
        return buffer

    def test_validate_image_accepts_supported_image(self):
        upload = self._make_upload()
        valid, message = ImagePreprocessor.validate_image(upload)
        self.assertTrue(valid)
        self.assertEqual(message, "Image is valid.")

    def test_resize_for_analysis_adds_padding_to_target(self):
        upload = self._make_upload(size=(120, 60))
        image = ImagePreprocessor.load_image(upload)
        resized = ImagePreprocessor.resize_for_analysis(image, target_size=(64, 64))

        self.assertEqual(resized.size, (64, 64))

    def test_image_to_base64_returns_string(self):
        upload = self._make_upload()
        image = ImagePreprocessor.load_image(upload)
        encoded = ImagePreprocessor.image_to_base64(image)

        self.assertIsInstance(encoded, str)
        self.assertGreater(len(encoded), 10)


if __name__ == "__main__":
    unittest.main()
