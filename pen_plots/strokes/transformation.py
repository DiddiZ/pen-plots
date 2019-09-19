import numpy as np


def affine_transformation(strokes, rotation=np.eye(2), translation=0):
    """
    Scales a single stroke or a list of strokes by a constant factor.

    Parameters
    ----------
    strokes : stroke or list of strokes
        Stroke(s) to be transformed.
    rotation : array_like (2, 2)
        Rotation matrix.
    translation : scalar or array_like (2,)
        Added constant.

    Returns
    -------
    stroke or list of strokes
        Transformed strokes.
    """
    if isinstance(strokes, list):
        return [affine_transformation(s, rotation, translation) for s in strokes]
    return np.einsum('ij,kj->ki', rotation, strokes) + translation


def rotation_matrix(angle):
    """
    Returns the rotation matrix corresponding to the given angle in radians.
    """
    return np.asarray([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)],
    ])


def scaling_matrix(scale_factor):
    """
    Returns the scaling matrix corresponding to the given scale_factor.
    """
    return np.eye(2) * scale_factor


def translate(strokes, x, y):
    """
    Translates a stroke or a list of strokes by `x` and `y`.

    See affine_transformation for details.
    """
    return affine_transformation(strokes, translation=[x, y])


def scale(strokes, scale_factor):
    """
    Scales a stroke or a list of strokes by `scale_factor`.

    See affine_transformation for details.
    """
    return affine_transformation(strokes, rotation=scaling_matrix(scale_factor))


def rotate(strokes, angle):
    """
    Rotates a stroke or a list of strokes by `angle`.

    See affine_transformation for details.
    """
    return affine_transformation(strokes, rotation=rotation_matrix(angle))
