import numpy as np


def merge_strokes(strokes):
    from pen_plots.strokes import to_strokes
    from shapely.geometry import MultiLineString
    from shapely.ops import linemerge

    merged = linemerge(MultiLineString(strokes))
    if not hasattr(merged, '__iter__'):  # Result is a single linestring instead of a MultiLineString
        merged = [merged]

    return to_strokes(merged)


def optimize_stroke_order(strokes, start_point=(0, 0)):
    """
    Optimizes stroke order for plotting to reduce travel distance greedily.

    May reverse strokes and start closed loops at arbitrary points.
    """

    # Create list of possible stroke starting points
    points = []
    points_meta = []
    for i, stroke in enumerate(strokes):
        if np.array_equal(stroke[0], stroke[-1]):  # Stroke is closed loop
            # Stroke may start at any point
            points.extend(stroke[0:-1])
            points_meta.extend([(i, j) for j in range(len(stroke) - 1)])
        else:
            # Stroke may start at first point or last point (reversed)
            points.extend([
                stroke[0],
                stroke[-1],
            ])

            points_meta.extend([
                (i, 0),
                (i, -1),
            ])
    points = np.array(points)
    points_meta = np.array(points_meta)

    def closest_stoke(p):
        min_idx = np.argmin(np.sum(np.square(points - p), axis=-1))
        stroke_idx, order = points_meta[min_idx]
        stroke = strokes[stroke_idx]
        if order == -1:
            stroke = stroke[::-1]
        elif order > 0:
            # Shift closed curve accordingly
            stroke = np.roll(stroke[:-1], -order, axis=0)  # Shift points
            stroke = np.concatenate([stroke, stroke[:1]], axis=0)  # Close curve again

        points[points_meta[:, 0] == stroke_idx, :] = np.inf

        return stroke

    pos = start_point
    opt_strokes = []
    for _ in range(len(strokes)):
        stroke = closest_stoke(pos)
        opt_strokes.append(stroke)
        pos = stroke[-1]

    return opt_strokes
