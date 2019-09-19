import numpy as np


def concat(strokes):
    """
    Concatenates multiple strokes.

    Raises
    ------
    ValueError
        when strokes aren't overlapping
    """
    partial_strokes = [strokes[0]]
    for i in range(1, len(strokes)):
        # Ensure last point of previous stroke is identical with starting point of next stroke.
        if not np.allclose(partial_strokes[-1][-1], strokes[i][0]):
            raise ValueError("Could not concatenate strokes: %r != %r" % (partial_strokes[-1][-1], strokes[i][0]))
        partial_strokes.append(strokes[i][1:])
    return np.concatenate(partial_strokes, axis=0)


def bounding_box(strokes):
    """
    Computes the bounding box of a stroke or a list of strokes.

    Returns
    -------
    ndarray (2, 2)
        where first dimension is min/max and the second is x/y.
    """
    if isinstance(strokes, list):
        return np.array(
            [
                np.min([np.min(s, axis=0) for s in strokes], axis=0),
                np.max([np.max(s, axis=0) for s in strokes], axis=0),
            ]
        )
    return np.array([
        np.min(strokes, axis=0),
        np.max(strokes, axis=0),
    ])
