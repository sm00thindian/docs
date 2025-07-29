# tests/test_chunking.py
import unittest
from src.chunking import TextChunker

class TestChunking(unittest.TestCase):
    def test_chunk(self):
        chunker = TextChunker(chunk_size=3, overlap=1)
        text = "one two three four five"
        chunks = chunker.chunk(text)
        self.assertEqual(chunks, ["one two three", "three four five"])

if __name__ == '__main__':
    unittest.main()
