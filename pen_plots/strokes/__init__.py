"""
This module contains basic methods for stroke manipulation.

stroke:  ndarray of points with shape (N, 2) which is intended to be plotted with a continous stroke.
strokes: List of strokes.
"""

from pen_plots.strokes.strokes import concat
from pen_plots.strokes.transformation import affine_transformation, translate, scale, rotate
from pen_plots.strokes.shapes import circle
