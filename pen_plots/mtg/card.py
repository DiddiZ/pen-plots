import numpy as np
from pen_plots.strokes import to_strokes, translate, rounded_rectangle, circle, concat, rectangle, bounding_box, scale_to_fit
from pen_plots.fonts import glyphs_to_strokes
from pen_plots.mtg.glyphs import line_to_glyphs
from textwrap import wrap

from pen_plots.mtg import strip_reminders, join_keyword_lines


def _replace_chars(string):
    """
    Replaces some chars with ones which have a hershey code equivalent.
    """
    for replacement in [('\'', '’'), ('—', '-'), ('−', '-'), ('•', '*')]:
        string = string.replace(*replacement)
    return string


def vectorize_card(card_data):
    """
    Converts a MtG card to strokes.
    """
    return create_card(
        card_title=_replace_chars(card_data["name"]),
        card_type=_replace_chars(card_data["type_line"]),
        mana_cost=card_data["mana_cost"],
        oracle_text=join_keyword_lines(strip_reminders(_replace_chars(card_data["oracle_text"]))),
        power=card_data.get("power"),
        toughness=card_data.get("toughness"),
        loyalty=card_data.get("loyalty"),
    )


def difference(strokes, area):
    """
    Computes set difference of a list of strokes and an area specified by a stroke.
    """
    from shapely.geometry import Polygon, MultiLineString

    return to_strokes(MultiLineString(strokes).difference(Polygon(area)))


def create_card(card_title, card_type, mana_cost=None, oracle_text=None, power=None, toughness=None, loyalty=None):
    """
    Creates a MtG card with strokes.

    Parameters
    ----------
    card_title : str
        Name of the card.
    card_type : str
        Type lien of the card.
    mana_cost : str/None
        Mana cost of the card. Uses Scryfall encoding for special symbols, e.g. {R} for pne red mana. May be none to
        indicate no mana costs, e.g. for land.
    oracle_text : str/None
        Oracle text of the card. May be None to indicate no oracle text, i.e. vanilla cards.
    power, toughness : str/None
        Power and toughness of the card. May be None for non-creature cards.
    loyalty : str/None
        Loyality of the card. Mutually exclusive with power/toughness. May be None for non-planeswaker cards.
    Returns
    -------
    list of strokes
        Vectorizes card.
    """
    card_width, card_height = 63, 88
    outer_rounding = 2.5
    bottom_border_extra = 0
    bar_height = 5
    img_height = 39.3

    x_left, x_right = 4.5, card_width - 4.5

    outer_margin, inner_margin = x_left - outer_rounding, 0.5
    y_title_top = card_height - outer_rounding - outer_margin
    y_title_bottom = y_title_top - bar_height
    y_img_top = y_title_bottom - inner_margin
    y_img_bottom = y_img_top - img_height
    y_type_top = y_img_bottom - inner_margin
    y_type_bottom = y_type_top - bar_height

    x_text_left, x_text_right = x_left, x_right
    y_text_top, y_text_bottom = y_type_bottom - inner_margin, outer_rounding + outer_margin + bottom_border_extra

    margin_x_text = 0.5
    oracle_text_line_height = 8 / 3
    oracle_text_par_skip = 2 / 3
    oracle_text_font_size = 5

    strokes = []

    # Outer border
    strokes.append(rounded_rectangle(63, 88, outer_rounding, 8))
    # Outer border inner
    strokes.append(
        translate(
            rounded_rectangle(63 - outer_rounding * 2, 88 - outer_rounding * 2 - bottom_border_extra, 1, 8),
            x=outer_rounding,
            y=outer_rounding + bottom_border_extra,
        )
    )

    # Title bar
    strokes.append(translate(bar_rectangle(x_right - x_left, y_title_top - y_title_bottom, 8), x_left, y_title_bottom))

    # Image Box
    strokes.append(translate(rectangle(x_right - x_left, y_img_top - y_img_bottom), x_left, y_img_bottom))

    # Type bar
    strokes.append(translate(bar_rectangle(x_right - x_left, y_type_top - y_type_bottom, 8), x_left, y_type_bottom))

    # Power/Toughness, loyality
    if power is not None and toughness is not None or loyalty is not None:
        # P/T bar
        pt_bar_width = 8 if loyalty is None else 4
        pt_bar = translate(bar_rectangle(pt_bar_width, 5, 8), x_right - pt_bar_width, y_text_bottom - 1)
        pt_bar_bbox = bounding_box(pt_bar)
        strokes.append(pt_bar)

        # P/T text
        strokes.extend(
            translate(
                scale_to_fit(
                    glyphs_to_strokes(
                        line_to_glyphs(power + '/' + toughness if loyalty is None else loyalty),
                        font_size=7,
                        alignment='center',
                    ),
                    max_width=pt_bar_width,
                ),
                x_right - pt_bar_width / 2,
                y_text_bottom - 1 + 5 / 2,
            )
        )
    else:
        pt_bar_bbox = None

    # Text box
    text_box = translate(rectangle(x_text_right - x_text_left, y_text_top - y_text_bottom), x_text_left, y_text_bottom)
    if pt_bar_bbox is None:
        strokes.append(text_box)
    else:
        # Draw around P/T bar
        strokes.extend(difference([text_box], pt_bar))

    # Mana Cost
    if len(mana_cost) > 0:
        text_mana_cost = glyphs_to_strokes(line_to_glyphs(mana_cost), font_size=6, alignment='right')
        x_mana_cost_left = x_right + bounding_box(text_mana_cost)[0, 0] - margin_x_text
        strokes.extend(
            translate(
                scale_to_fit(
                    text_mana_cost,
                    max_width=x_right - x_left - margin_x_text * 2,
                ),
                x_right - margin_x_text,
                (y_title_bottom + y_title_top) / 2,
            )
        )
    else:
        x_mana_cost_left = x_right

    # Title text
    strokes.extend(
        translate(
            scale_to_fit(
                glyphs_to_strokes(line_to_glyphs(card_title), font_size=6),
                max_width=x_mana_cost_left - x_left - margin_x_text * 2,
            ),
            x_left + margin_x_text,
            (y_title_bottom + y_title_top) / 2,
        )
    )

    # Type Text
    strokes.extend(
        translate(
            scale_to_fit(
                glyphs_to_strokes(line_to_glyphs(card_type), font_size=6),
                max_width=x_right - x_left - margin_x_text * 2,
            ),
            x_left + margin_x_text,
            (y_type_bottom + y_type_top) / 2,
        )
    )

    # Oracle text
    if len(oracle_text) > 0:
        x_line_left = x_text_left + margin_x_text
        oracle_text_scale = 1
        while True:
            oracle_text_strokes = []
            oracle_text_top_offset = (oracle_text_line_height + oracle_text_par_skip) * oracle_text_scale / 2
            for oracle_text_line in oracle_text.split('\n'):
                while len(oracle_text_line) > 0:
                    x_line_right = (
                        x_text_right if pt_bar_bbox is None or pt_bar_bbox[1, 1] < y_text_top - oracle_text_top_offset -
                        oracle_text_par_skip * oracle_text_scale else pt_bar_bbox[0, 0]
                    ) - margin_x_text
                    n_line_chars = 42.5 * (x_line_right - x_line_left - margin_x_text * 2
                                          ) / (x_text_right - x_text_left) / oracle_text_scale

                    line = wrap(oracle_text_line, n_line_chars)[0]  # TODO Calculate wrap based on actual char sizes
                    oracle_text_line = oracle_text_line[len(line) + 1:]

                    oracle_text_strokes.extend(
                        translate(
                            scale_to_fit(
                                glyphs_to_strokes(
                                    line_to_glyphs(line),
                                    font_size=oracle_text_font_size * oracle_text_scale,
                                ),
                                max_width=x_line_right - x_line_left,
                            ),
                            x_line_left,
                            y_text_top - oracle_text_top_offset,
                        )
                    )
                    oracle_text_top_offset += oracle_text_line_height * oracle_text_scale
                oracle_text_top_offset += oracle_text_par_skip * oracle_text_scale

            # Check if text fits
            if bounding_box(oracle_text_strokes)[0][1] > y_text_bottom + oracle_text_par_skip * oracle_text_scale / 2:

                # Check if text doesn't collide with pt bar:
                collision = False
                if pt_bar_bbox is not None:
                    for stroke in oracle_text_strokes:
                        for p in stroke:
                            if p[0] >= pt_bar_bbox[0][0] and p[0] <= pt_bar_bbox[1][0] and p[1] >= pt_bar_bbox[0][
                                1
                            ] and p[1] <= pt_bar_bbox[1][1]:
                                collision = True

                if not collision:
                    strokes.extend(oracle_text_strokes)
                    if oracle_text_scale < 1:
                        print('Scaled oracle text to %f' % oracle_text_scale)
                    break
            oracle_text_scale *= 0.99

    return strokes


def bar_rectangle(w, h, n):
    """
    Bar used for title and type bars
    """
    return concat(
        [
            translate(
                circle(
                    n,
                    -1 / 4 * np.pi,
                    1 / 4 * np.pi,
                ) * h / 2 * np.sqrt(2),
                w - h / 2,
                h / 2,
            ),
            [
                [w, h],
                [0, h],
            ],
            translate(
                circle(
                    8,
                    3 / 4 * np.pi,
                    5 / 4 * np.pi,
                ) * h / 2 * np.sqrt(2),
                h / 2,
                h / 2,
            ),
            [
                [0, 0],
                [w, 0],
            ],
        ]
    )
