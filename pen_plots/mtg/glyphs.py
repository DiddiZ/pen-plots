import numpy as np
import re
from pen_plots.fonts import Glyph, combine_glyphs, transform_glyph
from pen_plots.fonts.hershey import glyph_by_char, glyph_by_hershey_code
from pen_plots.strokes import bounding_box
from pen_plots.strokes.transformation import rotation_matrix, scaling_matrix


def encircled_glyph(glyph, circle_glyph=glyph_by_hershey_code(905)):
    bbox = bounding_box(glyph.lines)
    combined = combine_glyphs(
        transform_glyph(glyph, translation=-(bbox[0] + bbox[1]) / 2),  # Center glyph
        circle_glyph,
    )
    # Increase margins
    return Glyph(combined.lines, combined.left - 2, combined.right + 2)


special_glyphs = {
    # Tap
    '{T}': encircled_glyph(transform_glyph(
        glyph_by_char('T', 'rowmans'),
        rotation=rotation_matrix(np.pi / 4),
    )),
    # Colorless mana
    '{C}': encircled_glyph(transform_glyph(
        glyph_by_hershey_code(735),
        rotation=rotation_matrix(np.pi / 4),
    ))
}

# Single color mana, X and generic mana 0-9
for c in ['B', 'R', 'G', 'U', 'W', 'X'] + ['%d' % i for i in range(10)]:
    special_glyphs['{%s}' % c] = encircled_glyph(
        transform_glyph(
            glyph_by_char(c, 'rowmans'),
            rotation=scaling_matrix(0.95),
        )
    )

# Generic mana 10-16
for c in ['%d' % i for i in range(10, 17)]:
    g1, g2 = glyph_by_char(c[0], 'rowmans'), glyph_by_char(c[1], 'rowmans')
    special_glyphs['{%s}' % c] = encircled_glyph(
        combine_glyphs(
            transform_glyph(g1, rotation=scaling_matrix(0.85), translation=[4 - g1.right, 0]),
            transform_glyph(g2, rotation=scaling_matrix(0.85), translation=[-g1.left - 4, 0]),
        )
    )

# TODO
# {Q}: Untap
# {E}: Energy
# {S}: Snow mana
# {W/U},{W/B},{B/R},{B/G},{U/B},{U/R},{R/G},{R/W},{G/W},{G/U}: hybrid mana
# {2/W},{2/U},{2/B},{2/R},{2/G} Monocolored hybrid mana
# {W/P},{U/P},{B/P},{R/P},{G/P}: Phyrexian mana


def line_to_glyphs(line):
    glyphs = []

    for c in re.findall(r'([^{]|\{[^}]*\})', line):
        if c[0] == '{':
            g = special_glyphs.get(c)
            if g is not None:
                glyphs.append(g)
            else:
                raise ValueError('Unknown special sequence %s' % c)
        else:
            glyphs.append(glyph_by_char(c, 'rowmans'))

    return glyphs
