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


class Test_Reminders(unittest.TestCase):
    def test_frenzied_arynx(self):
        from pen_plots.mtg import strip_reminders, join_keyword_lines

        oracle_text = "Riot (This creature enters the battlefield with your choice of a +1/+1 counter or haste.)\nTrample\n{4}{R}{G}: Frenzied Arynx gets +3/+0 until end of turn."
        expected = "Riot, Trample\n{4}{R}{G}: Frenzied Arynx gets +3/+0 until end of turn."
        self.assertEqual(join_keyword_lines(strip_reminders(oracle_text)), expected)

    def test_rhythm_of_the_wild(self):
        from pen_plots.mtg import strip_reminders, join_keyword_lines

        oracle_text = "Creature spells you control can't be countered.\nNontoken creatures you control have riot. (They enter the battlefield with your choice of a +1/+1 counter or haste.)"
        expected = "Creature spells you control can't be countered.\nNontoken creatures you control have riot."
        self.assertEqual(join_keyword_lines(strip_reminders(oracle_text)), expected)

    def test_ambush_viper(self):
        from pen_plots.mtg import strip_reminders, join_keyword_lines

        oracle_text = "Flash (You may cast this spell any time you could cast an instant.)\nDeathtouch (Any amount of damage this deals to a creature is enough to destroy it.)"
        expected = "Flash, Deathtouch"
        self.assertEqual(join_keyword_lines(strip_reminders(oracle_text)), expected)
