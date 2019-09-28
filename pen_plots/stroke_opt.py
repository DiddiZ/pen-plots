import numpy as np


def optimize_stroke_order(strokes, start_point=(0, 0)):
    """
    Optimizes stroke order for plotting to reduce travel distance greedily.

    May reverse strokes and start closed loops at arbitrary points.
    """
    from pen_plots.optimization.agtsp import greedy

    # Transform strokes to a Asymmetric Generalized Traveling Salesman Problem
    tsp = []
    for stroke in strokes:
        if np.allclose(stroke[0], stroke[-1]):  # Stroke is closed loop
            # Stroke may start at any point
            cities = [(p, p) for p in stroke[:-1]]
            tsp.append(cities)
        else:

            cityA = (stroke[0], stroke[-1])
            cityB = (stroke[-1], stroke[0])
            tsp.append([cityA, cityB])

    opt_strokes = []
    for state_idx, city_idx in greedy(tsp):
        stroke = strokes[state_idx]
        if np.allclose(stroke[0], stroke[-1]):  # Closed loop
            if city_idx > 0:  # Shift closed curve accordingly
                stroke = np.roll(stroke[:-1], -city_idx, axis=0)  # Shift points
                stroke = np.concatenate([stroke, stroke[:1]], axis=0)  # Close curve again
        else:
            if city_idx > 0:
                stroke = stroke[::-1]

        opt_strokes.append(stroke)

    return opt_strokes
