import numpy as np
from collections import namedtuple
from pen_plots.strokes import affine_transformation, bounding_box, translate

# A glyph consists of a list of lines as well as horizontal margins.
Glyph = namedtuple("Glyph", ["lines", "left", "right"])


def glyphs_to_strokes(glyphs):
    """
    Converts a list of glyphs to strokes. Glyphs are placed from left to right, spaced according to their margins.

    This can be considered as rendering a single line of text without line breaks.
    """
    offset = 0
    strokes = []
    for glyph in glyphs:
        strokes.extend(translate(glyph.lines, offset - glyph.left, 0))
        offset += glyph.right - glyph.left

    return strokes


def combine_glyphs(*glyphs):
    """
    Combines multiple glyphs into a single one. Keeps margins of the largest glyphs.
    """
    return Glyph(
        lines=sum([g.lines for g in glyphs], []),
        left=np.min([g.left for g in glyphs]),
        right=np.max([g.right for g in glyphs]),
    )


def transform_glyph(glyph, rotation=np.eye(2), translation=0):
    """
    Applies an affine transformation to the strokes of a glyph. Updates margins accordingly.
    """
    lines = affine_transformation(glyph.lines, rotation, translation)
    bbox, bbox_transformed = bounding_box(glyph.lines)[:, 0], bounding_box(lines)[:, 0]

    # Scale marging according to change in width
    scale_factor = (bbox_transformed[1] - bbox_transformed[0]) / (bbox_transformed[1] - bbox_transformed[0])
    return Glyph(
        lines=lines,
        left=bbox_transformed[0] - bbox[0] + glyph.left * scale_factor,
        right=bbox_transformed[1] - bbox[1] + glyph.right * scale_factor,
    )
