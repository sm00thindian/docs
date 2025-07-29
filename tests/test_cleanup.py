# tests/test_cleaning.py
import unittest
from src.cleaning import TextCleaner

class TestCleaning(unittest.TestCase):
    def test_clean(self):
        cleaner = TextCleaner()
        input_text = "Hello   world!  "
        cleaned = cleaner.clean(input_text)
        self.assertEqual(cleaned, "Hello world!")

if __name__ == '__main__':
    unittest.main()
