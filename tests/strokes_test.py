import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_raises


class Test_Concatenation(unittest.TestCase):
    def test_concat(self):
        from pen_plots.strokes import concat

        strokes = [
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
            np.array([[1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]),
        ]

        concatenated = concat(strokes)
        expected = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]

        assert_array_almost_equal(concatenated, expected)

    def test_concat_error(self):
        from pen_plots.strokes import concat

        strokes = [
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
            np.array([[0.0, 1.0], [0.0, 0.0]]),  # Does not start with last end point
        ]
        with assert_raises(ValueError):
            concat(strokes)


class Test_Transformations(unittest.TestCase):
    def test_translate_stroke(self):
        from pen_plots.strokes import translate

        stroke = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

        translated = translate(stroke, 1, 2)
        expected = [[1.0, 2.0], [2.0, 2.0], [2.0, 3.0], [1.0, 3.0], [1.0, 2.0]]

        assert_array_almost_equal(translated, expected)

    def test_translate_strokes(self):
        from pen_plots.strokes import translate

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
        from pen_plots.strokes import scale

        stroke = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

        scaled = scale(stroke, 2)
        expected = [[0.0, 0.0], [2.0, 0.0], [2.0, 2.0], [0.0, 2.0], [0.0, 0.0]]

        assert_array_almost_equal(scaled, expected)

    def test_rotate_stroke(self):
        from pen_plots.strokes import rotate

        stroke = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

        rotated = rotate(stroke, np.pi / 2)
        expected = [[0.0, 0.0], [0.0, 1.0], [-1.0, 1.0], [-1.0, 0.0], [0.0, 0.0]]

        assert_array_almost_equal(rotated, expected)


class Test_Shapes(unittest.TestCase):
    def test_circle(self):
        from pen_plots.strokes import circle

        stroke = circle(8)
        expected = [  # Basic octagon
            [1.0, 0.0], [np.sqrt(2) / 2, np.sqrt(2) / 2], [0.0, 1.0], [-np.sqrt(2) / 2, np.sqrt(2) / 2], [-1.0, 0.0],
            [-np.sqrt(2) / 2, -np.sqrt(2) / 2], [0.0, -1.0], [np.sqrt(2) / 2, -np.sqrt(2) / 2], [1.0, 0.0]
        ]

        assert_array_almost_equal(stroke, expected)

    def test_circle_arc(self):
        from pen_plots.strokes import circle

        stroke = circle(2, 0, np.pi / 2)

        expected = [[1.0, 0.0], [np.sqrt(2) / 2, np.sqrt(2) / 2], [0.0, 1.0]]

        assert_array_almost_equal(stroke, expected)

    def test_rectangle(self):
        from pen_plots.strokes import rectangle

        stroke = rectangle(3, 2)

        expected = [[0.0, 0.0], [3.0, 0.0], [3.0, 2.0], [0.0, 2.0], [0.0, 0.0]]

        assert_array_almost_equal(stroke, expected)
