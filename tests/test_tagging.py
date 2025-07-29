# tests/test_tagging.py
import unittest
from src.tagging import TextTagger

class TestTagging(unittest.TestCase):
    def test_tag_chunks(self):
        tagger = TextTagger()
        chunks = ["This is a test chunk about policies."]
        tagged = tagger.tag_chunks(chunks, "test.docx")
        self.assertEqual(len(tagged), 1)
        self.assertIn('keywords', tagged[0])

if __name__ == '__main__':
    unittest.main()
