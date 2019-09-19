"""
This module contains functions to create strokes for basic shapes.
"""
import numpy as np


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
