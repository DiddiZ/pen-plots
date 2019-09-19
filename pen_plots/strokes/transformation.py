import numpy as np
from pen_plots.strokes import bounding_box


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


def scale_to_fit(strokes, min_width=None, max_width=None, min_height=None, max_height=None):
    """
    Returns the scaling matrix corresponding to the given scale_factor.
    """
    # Compute dimension
    bbox_min, bbox_max = bounding_box(strokes)
    width, height = bbox_max - bbox_min

    # Determine scaling facor
    c = [1, 1]
    if min_width is not None and width < min_width:
        c[0] = min_width / width
    elif max_width is not None and width > max_width:
        c[0] = max_width / width
    if min_height is not None and height < min_height:
        c[1] = min_height / height
    elif max_height is not None and height > max_height:
        c[1] = max_height / height

    return affine_transformation(strokes, rotation=np.diag(c))
