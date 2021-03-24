import unittest
from mapping import *

class TestCases(unittest.TestCase):

    mapper = {
        "swan ton pacific ranch": "Swanton Pacific Ranch",
        "Swanton Pacific Ranch": "Swanton Pacific Ranch",
        "Swanton Pacifico": "Swanton Pacific Ranch",
        "Swanton": "Swanton Pacific Ranch",
        "Swanton Pacific": "Swanton Pacific Ranch"
    }

    def test_get_match_01(self):
        predicted = get_match("swanto")
        expected = "Swanton Pacific Ranch"
        self.assertEqual(predicted, expected)

    def test_get_match_02(self):
        predicted = get_match("swanton pacifico")
        expected = "Swanton Pacific Ranch"
        self.assertEqual(predicted, expected)

    def test_stt_mapper(self):
        text = "how did cal poly get swanto pacifico rancho"
        predicted = stt_mapper(text)
        expected = "how did cal poly get Swanton Pacific Ranch"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_01(self):
        text = "how big is swanton"
        predicted = stt_mapper(text)
        expected = "how big is Swanton Pacific Ranch"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_02(self):
        """doesn't work for names that are not surrounded by stop words"""
        text = "is Swanton pacific open to the public"
        predicted = stt_mapper(text)
        expected = "is Swanton Pacific Ranch open to the public"
        self.assertEqual(predicted, expected)


if __name__ == '__main__':
   unittest.main()