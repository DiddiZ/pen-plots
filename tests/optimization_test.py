import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal


class Test_Shapely_Conversion(unittest.TestCase):
    def test_conversion(self):
        from pen_plots.strokes import to_strokes
        from shapely.geometry import MultiLineString

        strokes = [
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
            np.array([[1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]),
        ]

        assert_array_almost_equal(to_strokes(MultiLineString(strokes)), strokes)

    def test_conversion_single_stroke(self):
        from pen_plots.strokes import to_strokes
        from shapely.geometry import MultiLineString

        strokes = [
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
        ]
        assert_array_almost_equal(to_strokes(MultiLineString(strokes)), strokes)

    def test_conversion_rings(self):
        from pen_plots.strokes import to_strokes
        from shapely.geometry import MultiLineString
        from pen_plots.strokes import rectangle

        strokes = [
            rectangle(1, 1),
            rectangle(1, 1) + [1, 1],
        ]
        assert_array_almost_equal(to_strokes(MultiLineString(strokes)), strokes)


class Test_Optimization(unittest.TestCase):
    def test_merge_simple(self):
        from pen_plots.strokes import merge_strokes

        strokes = [  # Two strokes which can be joined
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
            np.array([[1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]),
        ]
        expected = [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]

        assert_array_almost_equal(merge_strokes(strokes), expected)

    def test_merge_reverse(self):
        from pen_plots.strokes import merge_strokes

        strokes = [  # Two strokes which can be joined, but one must be reversed
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
            np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0]]),
        ]
        expected = [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]

        assert_array_almost_equal(merge_strokes(strokes), expected)

    def test_optimize_order(self):
        from pen_plots import optimize_stroke_order

        strokes = [
            np.array([[1.0, 0.0], [2.0, 0.0]]),
            np.array([[1.0, 0.0], [0.0, 0.0]]),  # Reversed
        ]
        expected = [
            [[0.0, 0.0], [1.0, 0.0]],
            [[1.0, 0.0], [2.0, 0.0]],
        ]

        optimized = optimize_stroke_order(strokes)
        self.assertEqual(len(optimized), len(expected))
        for i in range(len(expected)):
            assert_array_almost_equal(optimized[i], expected[i])

    def test_optimize_order_loop(self):
        from pen_plots import optimize_stroke_order

        strokes = [
            np.array([[0.0, 0.0], [1.0, 0.0]]),
            np.array([[1.0, 1.0], [1.0, 0.0], [2.0, 0.0], [2.0, 1.0], [1.0, 1.0]]),  # Closed loop
        ]
        expected = [
            np.array([[0.0, 0.0], [1.0, 0.0]]),
            np.array([[1.0, 0.0], [2.0, 0.0], [2.0, 1.0], [1.0, 1.0], [1.0, 0.0]]),
        ]

        optimized = optimize_stroke_order(strokes)
        self.assertEqual(len(optimized), len(expected))
        for i in range(len(expected)):
            assert_array_almost_equal(optimized[i], expected[i])
