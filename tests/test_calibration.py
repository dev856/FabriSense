import unittest

import numpy as np

from training.calibrate import expected_calibration_error, fit_temperature, softmax


class CalibrationTests(unittest.TestCase):
    def test_overconfident_logits_get_temperature_above_one_and_lower_ece(self):
        rng = np.random.default_rng(0)
        labels = rng.integers(0, 4, size=2000)
        # Unit-variance Gaussian logits with a 1.5 shift on the true class: the Bayes-calibrated
        # logits are 1.5 * raw, so scaling raw by 4 needs T = 4 / 1.5 to undo.
        raw_logits = rng.normal(size=(2000, 4))
        raw_logits[np.arange(2000), labels] += 1.5
        overconfident = raw_logits * 4

        temperature = fit_temperature(overconfident, labels)
        self.assertAlmostEqual(temperature, 4 / 1.5, delta=0.4)
        self.assertLess(
            expected_calibration_error(softmax(overconfident, temperature), labels),
            expected_calibration_error(softmax(overconfident), labels),
        )

    def test_perfectly_calibrated_has_zero_ece(self):
        probs = np.array([[1.0, 0.0], [0.0, 1.0]])
        self.assertEqual(expected_calibration_error(probs, np.array([0, 1])), 0.0)


if __name__ == "__main__":
    unittest.main()
