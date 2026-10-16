import unittest

import numpy as np

from training.calibrate import expected_calibration_error, fit_temperature, softmax


class CalibrationTests(unittest.TestCase):
    def test_overconfident_logits_get_temperature_above_one_and_lower_ece(self):
        rng = np.random.default_rng(0)
        labels = rng.integers(0, 4, size=2000)
        # Signal strength 1.0 is the "true" scale; multiplying by 4 makes the model overconfident.
        true_logits = rng.normal(size=(2000, 4))
        true_logits[np.arange(2000), labels] += 1.5
        overconfident = true_logits * 4

        temperature = fit_temperature(overconfident, labels)
        self.assertAlmostEqual(temperature, 4.0, delta=0.6)
        self.assertLess(
            expected_calibration_error(softmax(overconfident, temperature), labels),
            expected_calibration_error(softmax(overconfident), labels),
        )

    def test_perfectly_calibrated_has_zero_ece(self):
        probs = np.array([[1.0, 0.0], [0.0, 1.0]])
        self.assertEqual(expected_calibration_error(probs, np.array([0, 1])), 0.0)


if __name__ == "__main__":
    unittest.main()
