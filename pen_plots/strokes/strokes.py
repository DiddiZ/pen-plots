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
