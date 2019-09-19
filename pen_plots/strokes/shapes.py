"""
This module contains functions to create strokes for basic shapes.
"""
import numpy as np
from pen_plots.strokes.strokes import concat


def circle(n_segments, start_angle=0, end_angle=2 * np.pi):
    """
    Constructs a stroke describing a circle or arc with radius 1.

    Parameters
    ----------
    n_segments : int
        Number of segments.
    start_angle : radians
        Starting angle in radians. Defaults to 0.
    end_angle : radians
        Ending angle in radians. Defaults to 2*pi in order to describe a full circle.

    Returns
    -------
    stroke
        with `n_segments` + 1 points.
    """
    points = np.empty((n_segments + 1, 2))
    segment_angle = (end_angle - start_angle) / n_segments
    for i in range(n_segments + 1):
        points[i] = [np.cos(start_angle + i * segment_angle), np.sin(start_angle + i * segment_angle)]
    return points


def rectangle(width, height):
    """
    Constructs a stroke describing an axis-aligned rectangle with given `width` and `height`.
    """
    return np.asarray([(0, 0), (width, 0), (width, height), (0, height), (0, 0)])


def rounded_rectangle(width, height, rounding, n_segments):
    """
    Constructs a stroke describing an axis-aligned rectangle with rounded corners.

    Parameters
    ----------
    rounding : float
        Radius of rounding.
    n_segments : int
        Number of segments per rounded corner.

    Returns
    -------
    stroke
        with (`n_segments` + 2) * 4 points.
    """
    return concat(
        [
            circle(n_segments, 0, np.pi / 2) * rounding + [width - rounding, height - rounding],
            [[width - rounding, height], [rounding, height]],
            circle(n_segments, np.pi / 2, np.pi) * rounding + [rounding, height - rounding],
            [[0, height - rounding], [0, rounding]],
            circle(n_segments, np.pi, np.pi / 2 * 3) * rounding + [rounding, rounding],
            [[rounding, 0], [width - rounding, 0]],
            circle(n_segments, np.pi / 2 * 3, 2 * np.pi) * rounding + [width - rounding, rounding],
            [[width, rounding], [width, height - rounding]],
        ]
    )
