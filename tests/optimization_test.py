import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal


class Test_Optimization(unittest.TestCase):
    def test_optimize_simple(self):
        from pen_plots.optimization import optimize_stroke_order

        strokes = [  # Two strokes which can be joined
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
            np.array([[1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]),
        ]
        expected = [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]

        assert_array_almost_equal(optimize_stroke_order(strokes), expected)

    def test_optimize_reverse(self):
        from pen_plots.optimization import optimize_stroke_order

        strokes = [  # Two strokes which can be joined, but one must be reversed
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]),
            np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0]]),
        ]
        expected = [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]

        assert_array_almost_equal(optimize_stroke_order(strokes), expected)

    def test_optimize_closed_loop(self):
        from pen_plots.optimization import optimize_stroke_order

        strokes = [  # Two strokes which can be joined, but one is a closed loop
            np.array([[0.0, 0.0], [1.0, 0.0]]),
            np.array([[1.0, 1.0], [1.0, 0.0], [2.0, 0.0], [2.0, 1.0], [1.0, 1.0]]),
        ]
        expected = [[[0.0, 0.0], [1.0, 0.0], [2.0, 0.0], [2.0, 1.0], [1.0, 1.0], [1.0, 0.0]]]

        assert_array_almost_equal(optimize_stroke_order(strokes), expected)
