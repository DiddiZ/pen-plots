# This module provides algorithms for approximating the Asymmetric Generalized Traveling Salesman Problem.
# The assumed data structure of the problem is a list of states.
# Each state consists of a list of cities.
# Each city is a tuple of a start and an end point.
# The edge weights are endcoded as the eucledian distance between end and start points.
# E.g. tsp[state_idx][city_idx][0] is the start point of city_idx in state_idx.
# Returned solutions are index lists, consistign of state_idx and city_idx of visited cities in order.

import numpy as np


def cost(tsp, sol):
    """
    Computes the cost, i.e. total length of a solution `sol` to a Asymmetric Generalized Traveling Salesman Problem `tsp`.
    """
    cost = 0
    for i in range(1, len(tsp)):
        cost += np.linalg.norm(tsp[sol[i, 0]][sol[i, 1]][0] - tsp[sol[i - 1, 0]][sol[i - 1, 1]][1])
    return cost


def random(tsp):
    """
    Computes a random solution to the Asymmetric Generalized Traveling Salesman Problem.

    This solution is hardly optimal.
    """
    sol = np.empty((len(tsp), 2), dtype=int)
    for i, state in enumerate(np.random.permutation(len(tsp))):
        sol[i, 0] = state
        sol[i, 1] = np.random.randint(len(tsp[state]))
    return sol


def greedy(tsp, start_point=(0, 0)):
    """
    Computes a greedy solution to the Asymmetric Generalized Traveling Salesman Problem.

    Starts with the city closest to `start_point`.
    """
    # Create list of all starting points
    N_cities = np.sum([len(state) for state in tsp])
    points = np.empty((N_cities, len(start_point)), dtype=float)
    points_meta = np.empty((N_cities, len(start_point)), dtype=int)
    i = 0
    for state_idx, state in enumerate(tsp):
        for city_idx, city in enumerate(state):
            points[i] = city[0]
            points_meta[i] = (state_idx, city_idx)
            i += 1

    pos = start_point
    sol = np.empty((len(tsp), 2), dtype=int)
    for i in range(len(tsp)):
        # Find clostest starting point
        state_idx, city_idx = points_meta[np.argmin(np.sum(np.square(points - pos), axis=-1))]
        sol[i] = state_idx, city_idx
        pos = tsp[state_idx][city_idx][1]

        # Set all points of covered state to inf to prevent visiting again
        points[points_meta[:, 0] == state_idx, :] = np.inf

    return sol
