import unittest
from numpy.testing import assert_array_almost_equal


class Test_Cache(unittest.TestCase):
    def test_card_search(self):
        from pen_plots.mtg import search_card_by_name

        cards = search_card_by_name("Zacama, Primal Calamity")

        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["name"], "Zacama, Primal Calamity")
        self.assertEqual(cards[0]["mana_cost"], "{6}{R}{G}{W}")
        self.assertEqual(cards[0]["type_line"], "Legendary Creature — Elder Dinosaur")

    def test_get_image(self):
        import cv2
        from pen_plots.mtg import search_card_by_name, get_image

        cards = search_card_by_name("Zacama, Primal Calamity")
        image_path = get_image(cards[0]["image_uris"]["small"])

        img = cv2.imread(str(image_path))

        self.assertEqual(img.shape, (204, 146, 3))
        assert_array_almost_equal(img[0, 0], [244, 252, 251])
