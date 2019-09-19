import numpy as np
import json
import yaml
from pathlib import Path
from pen_plots.fonts import Glyph

# Load glyphs
with open(Path(__file__).parent / "hershey-occidental.json", "r") as read_file:
    glyphs_by_hershey_code = {
        glyph['charcode']: Glyph(
            lines=[np.array(l) * [1, -1] for l in glyph["lines"]],  # Flip y-axis
            left=glyph["left"],
            right=glyph["right"],
        )
        for glyph in json.load(read_file)
    }
    # Add space glyphs.
    for hershey_code in [699, 2199, 2699, 2749, 3199, 3699]:
        glyphs_by_hershey_code[hershey_code] = Glyph(
            lines=[],
            left=-5,
            right=5,
        )

# Load ascii/hershey code mapping
with open(Path(__file__).parent / 'encodings.yml', 'r') as encodings_file:
    hershey_code_by_ascii = yaml.load(encodings_file)


def glyph_by_hershey_code(hershey_code):
    """
    Returns the Hershey glyph corresponding to `hershey_code`.
    """
    glyph = glyphs_by_hershey_code.get(hershey_code)
    if glyph is None:
        raise ValueError("No glyph for hershey code %d" % hershey_code)
    return glyph


def glyph_by_char(c, font):
    """
    Returns the Hershey glyph for char `c` in `font`.
    """
    ascii_code = ord(c)
    hershey_code = hershey_code_by_ascii[font].get(ascii_code)

    if hershey_code is None:
        raise ValueError("No Hershey code for ascii char '%s' (%d)" % (c, ascii_code))

    return glyph_by_hershey_code(hershey_code)
