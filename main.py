from pen_plots.mtg import vectorize_card, search_card_by_name
from pen_plots.util.matplotlib import show_strokes

card_data = search_card_by_name("Zacama, Primal Calamity")

assert len(card_data) == 1

strokes = vectorize_card(card_data[0])

show_strokes(strokes, 0.32)
