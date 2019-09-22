import unittest
from numpy.testing import assert_array_almost_equal


class Test_Hershey_Glyphs(unittest.TestCase):
    def test_glyph_loading(self):
        import pen_plots.fonts.hershey as hershey

        glyph = hershey.glyph_by_hershey_code(501)
        expected = [[[0, 12], [-8, -9]], [[0, 12], [8, -9]], [[-5, -2], [5, -2]]]  # A

        assert_array_almost_equal(glyph.lines, expected)

    def test_get_glyph(self):
        import pen_plots.fonts.hershey as hershey

        glyph = hershey.glyph_by_char('A', font='rowmans')
        expected = [[[0, 12], [-8, -9]], [[0, 12], [8, -9]], [[-5, -2], [5, -2]]]  # A

        assert_array_almost_equal(glyph.lines, expected)

    def test_get_glyph_space(self):
        import pen_plots.fonts.hershey as hershey

        glyph = hershey.glyph_by_char(' ', font='rowmand')
        expected = []  # Space

        assert_array_almost_equal(glyph.lines, expected)


class Test_Glyphs(unittest.TestCase):
    def test_glyphs_to_strokes(self):
        import pen_plots.fonts.hershey as hershey
        from pen_plots.fonts import glyphs_to_strokes

        strokes = glyphs_to_strokes(
            [hershey.glyph_by_char('A', font='rowmans')], font_size=21 * 72 / 25.4, alignment='left'
        )
        expected = [[[9, 12], [1, -9]], [[9, 12], [17, -9]], [[4, -2], [14, -2]]]  # A

        assert_array_almost_equal(strokes, expected)

    def test_glyphs_to_strokes_align_right(self):
        import pen_plots.fonts.hershey as hershey
        from pen_plots.fonts import glyphs_to_strokes

        strokes = glyphs_to_strokes(
            [hershey.glyph_by_char('A', font='rowmans')], font_size=21 * 72 / 25.4, alignment='right'
        )
        expected = [[[-9, 12], [-17, -9]], [[-9, 12], [-1, -9]], [[-14, -2], [-4, -2]]]  # A

        assert_array_almost_equal(strokes, expected)

    def test_glyphs_to_strokes_align_center(self):
        import pen_plots.fonts.hershey as hershey
        from pen_plots.fonts import glyphs_to_strokes

        strokes = glyphs_to_strokes(
            [hershey.glyph_by_char('A', font='rowmans')], font_size=21 * 72 / 25.4, alignment='center'
        )
        expected = [[[0, 12], [-8, -9]], [[0, 12], [8, -9]], [[-5, -2], [5, -2]]]  # A

        assert_array_almost_equal(strokes, expected)

    def test_combine_glyphs(self):
        import pen_plots.fonts.hershey as hershey
        from pen_plots.fonts import combine_glyphs

        glyph = combine_glyphs(
            hershey.glyph_by_char('A', font='rowmans'),
            hershey.glyph_by_char('I', font='rowmans'),
        )
        expected = [[[0, 12], [-8, -9]], [[0, 12], [8, -9]], [[-5, -2], [5, -2]], [[0, 12], [0, -9]]]  # AI

        self.assertEqual(glyph.left, -9)
        self.assertEqual(glyph.right, 9)
        assert_array_almost_equal(glyph.lines, expected)

    def test_transform_glyph_translate(self):
        import pen_plots.fonts.hershey as hershey
        from pen_plots.fonts import transform_glyph

        glyph = transform_glyph(hershey.glyph_by_char('A', font='rowmans'), translation=[8, 9])
        expected = [[[8, 21], [0, 0]], [[8, 21], [16, 0]], [[3, 7], [13, 7]]]  # A

        self.assertEqual(glyph.left, -1)
        self.assertEqual(glyph.right, 17)
        assert_array_almost_equal(glyph.lines, expected)
