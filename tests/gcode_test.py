import unittest
import io
import numpy as np


class Test_GCode_Export(unittest.TestCase):
    def test_write_gcode_simple(self):
        from pen_plots import write_gcode

        strokes = [
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]),
        ]
        gcode = io.StringIO()
        write_gcode(gcode, strokes, offset=[0, 0])
        expected = """G28
G21
G0 F3600 X0.000 Y0.000 Z2.000
G0 F300 Z0.000
G0 F1800 X1.000 Y0.000
G0 F1800 X1.000 Y1.000
G0 F1800 X0.000 Y1.000
G0 F1800 X0.000 Y0.000
G0 F300 Z2.000
G28 X0 Y0
"""

        self.assertEqual(gcode.getvalue(), expected)
