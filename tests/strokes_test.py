import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal
from pen_plots.strokes import translate, scale, rotate


class Test_Transformations(unittest.TestCase):
    def test_translate_stroke(self):
        stroke = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

        translated = translate(stroke, 1, 2)
        expected = [[1.0, 2.0], [2.0, 2.0], [2.0, 3.0], [1.0, 3.0], [1.0, 2.0]]

        assert_array_almost_equal(translated, expected)

    def test_translate_strokes(self):
        strokes = [
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
            np.array([[0.0, 1.0], [0.0, 0.0]]),
        ]

        translated = translate(strokes, 1, 2)
        expected = [
            [[1.0, 2.0], [2.0, 2.0], [2.0, 3.0]],
            [[1.0, 3.0], [1.0, 2.0]],
        ]

        self.assertEqual(len(translated), len(expected))
        for i in range(len(expected)):
            assert_array_almost_equal(translated[i], expected[i])

    def test_scale_stroke(self):
        stroke = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

        scaled = scale(stroke, 2)
        expected = [[0.0, 0.0], [2.0, 0.0], [2.0, 2.0], [0.0, 2.0], [0.0, 0.0]]

        assert_array_almost_equal(scaled, expected)

    def test_rotate_stroke(self):
        stroke = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

        rotated = rotate(stroke, np.pi / 2)
        expected = [[0.0, 0.0], [0.0, 1.0], [-1.0, 1.0], [-1.0, 0.0], [0.0, 0.0]]

        assert_array_almost_equal(rotated, expected)
