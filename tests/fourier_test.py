import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal


def sort_ft(freq, c):
    idx = np.argsort(freq)
    return freq[idx], c[idx]


class Test_Fourier_Approximation(unittest.TestCase):
    def test_fourier_min_error(self):
        from pen_plots.optimization.fourier import fourier_min_error, fourier_fft_min_error

        points = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])

        freq, c = sort_ft(*fourier_min_error(points, 1e-2))
        freq_fft, c_fft = sort_ft(*fourier_fft_min_error(points, 1e-2))

        assert_array_almost_equal(freq, freq_fft)
        assert_array_almost_equal(c, c_fft)

    def test_fourier_min_error_large(self):
        from pen_plots.optimization.fourier import fourier_min_error, fourier_fft_min_error

        points = np.concatenate(
            [
                np.linspace([0.0, 0.0], [1.0, 0.0], endpoint=False),
                np.linspace([1.0, 0.0], [1.0, 1.0], endpoint=False),
                np.linspace([1.0, 1.0], [0.0, 1.0], endpoint=False),
                np.linspace([0.0, 1.0], [0.0, 0.0], endpoint=False),
            ]
        )

        freq, c = sort_ft(*fourier_min_error(points, 1e-2))
        freq_fft, c_fft = sort_ft(*fourier_fft_min_error(points, 1e-2))

        assert_array_almost_equal(freq, freq_fft)
        assert_array_almost_equal(c, c_fft)

    def test_fourier_min_error_approximation(self):
        from pen_plots.optimization.fourier import fourier_min_error, sample_fourier

        points = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])

        freq, c = fourier_min_error(points, 1e-5)
        samples = sample_fourier(freq, c, len(points) + 1)[:-1]

        self.assertGreaterEqual(1e-5, np.mean(np.square(points - samples)))

    def test_fourier_min_error_approximation_large(self):
        from pen_plots.optimization.fourier import fourier_min_error, sample_fourier

        points = np.concatenate(
            [
                np.linspace([0.0, 0.0], [1.0, 0.0], endpoint=False),
                np.linspace([1.0, 0.0], [1.0, 1.0], endpoint=False),
                np.linspace([1.0, 1.0], [0.0, 1.0], endpoint=False),
                np.linspace([0.0, 1.0], [0.0, 0.0], endpoint=False),
            ]
        )

        freq, c = fourier_min_error(points, 1e-5)
        samples = sample_fourier(freq, c, len(points) + 1)[:-1]

        self.assertGreaterEqual(1e-5, np.mean(np.square(points - samples)))
