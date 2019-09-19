import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_raises


class Test_Hershey_Glyphs(unittest.TestCase):
    def test_glyph_loading(self):
        import pen_plots.fonts.hershey as hershey

        glyph = hershey.glyph_by_hershey_code(501)
        expected = [[[0, -12], [-8, 9]], [[0, -12], [8, 9]], [[-5, 2], [5, 2]]]  # A

        assert_array_almost_equal(glyph.lines, expected)

    def test_get_glyph(self):
        import pen_plots.fonts.hershey as hershey

        glyph = hershey.glyph_by_char('A', font='rowmans')
        expected = [[[0, -12], [-8, 9]], [[0, -12], [8, 9]], [[-5, 2], [5, 2]]]  # A

        assert_array_almost_equal(glyph.lines, expected)

    def test_get_glyph_space(self):
        import pen_plots.fonts.hershey as hershey

        glyph = hershey.glyph_by_char(' ', font='rowmand')
        expected = []  # Space

        assert_array_almost_equal(glyph.lines, expected)
