import unittest

from training.models import SUPPORTED_ARCHITECTURES


class TrainingModelTests(unittest.TestCase):
    def test_supported_architectures_include_transfer_learning_options(self):
        self.assertIn("scratch_cnn", SUPPORTED_ARCHITECTURES)
        self.assertIn("resnet18", SUPPORTED_ARCHITECTURES)
        self.assertIn("resnet34", SUPPORTED_ARCHITECTURES)
        self.assertIn("efficientnet_b0", SUPPORTED_ARCHITECTURES)
        self.assertIn("mobilenet_v3_small", SUPPORTED_ARCHITECTURES)
        self.assertIn("vgg16", SUPPORTED_ARCHITECTURES)
        self.assertIn("alexnet", SUPPORTED_ARCHITECTURES)


if __name__ == "__main__":
    unittest.main()
