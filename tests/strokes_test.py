import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_raises


class Test_BoundingBoxes(unittest.TestCase):
    def test_bounding_box_stroke(self):
        from pen_plots.strokes import bounding_box

        stroke = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

        bbox = bounding_box(stroke)
        expected = [[0.0, 0.0], [1.0, 1.0]]

        assert_array_almost_equal(bbox, expected)

    def test_bounding_box_strokes(self):
        from pen_plots.strokes import bounding_box

        strokes = [
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
            np.array([[1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]),
        ]

        bbox = bounding_box(strokes)
        expected = [[0.0, 0.0], [1.0, 1.0]]

        assert_array_almost_equal(bbox, expected)


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

    def test_scale_to_fit(self):
        from pen_plots.strokes import scale_to_fit

        stroke = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

        scaled = scale_to_fit(stroke, min_width=2, max_height=0.5)
        expected = [[0.0, 0.0], [2.0, 0.0], [2.0, 0.5], [0.0, 0.5], [0.0, 0.0]]

        assert_array_almost_equal(scaled, expected)

    def test_scale_to_fit_no_change(self):
        from pen_plots.strokes import scale_to_fit

        stroke = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

        scaled = scale_to_fit(stroke, min_width=0, min_height=0, max_width=2, max_height=2)
        expected = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]

        assert_array_almost_equal(scaled, expected)


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
