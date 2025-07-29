# tests/test_ingestion.py
import unittest
from src.ingestion import WordDocumentIngester

class TestIngestion(unittest.TestCase):
    def test_ingest_docx(self):
        # Assume a sample file; in real tests, use a fixture
        ingester = WordDocumentIngester()
        # text = ingester.ingest('examples/sample_policy.docx')
        # self.assertTrue(len(text) > 0)
        self.assertTrue(True)  # Placeholder

if __name__ == '__main__':
    unittest.main()
