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

    def test_stt_mapper_03(self):
        text = "where is swanton located"
        predicted = stt_mapper(text)
        expected = "where is Swanton Pacific Ranch located"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_04(self):
        text = "can I camp or hike in swanto pacific ranch"
        predicted = stt_mapper(text)
        expected = "can I camp or hike in Swanton Pacific Ranch"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_05(self):
        text = "may i camp or hike in swanto pacific"
        predicted = stt_mapper(text)
        expected = "may i camp or hike in Swanton Pacific Ranch"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_06(self):
        text = "when is swanton pacific ranch open to the public"
        predicted = stt_mapper(text)
        expected = "when is Swanton Pacific Ranch open to the public"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_07(self):
        text = "what was the original name of Swanton Pacific"
        predicted = stt_mapper(text)
        expected = "what was the original name of Swanton Pacific Ranch"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_08(self):
        text = "what is a fun fact about the rancho"
        predicted = stt_mapper(text)
        expected = "what is a fun fact about the rancho"
        self.assertEqual(predicted, expected) #this should stay the same

    def test_stt_mapper_09(self):
        text = "how do i learn more about swanto pacifico rancho"
        predicted = stt_mapper(text)
        expected = "how do i learn more about Swanton Pacific Ranch"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_10(self):
        text = "what is cause uh very day used for"
        predicted = stt_mapper(text)
        expected = "what is Casa Verde used for"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_11(self):
        text = "how old is the cheese house"
        predicted = stt_mapper(text)
        expected = "how old is the Cheese House"
        self.assertEqual(predicted, expected)

    def test_stt_mapper_12(self):
        text = "what does you nah leg ah quadra mean in spanish"
        predicted = stt_mapper(text)
        expected = "what does Una Legua Cuadrada mean in spanish"
        self.assertEqual(predicted, expected)

if __name__ == '__main__':
   unittest.main()