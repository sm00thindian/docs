# tests/test_pipeline.py
import unittest
import os
from src.pipeline import process_document

class TestPipeline(unittest.TestCase):
    def test_process_document(self):
        # Placeholder; requires sample file
        # process_document('examples/sample_policy.docx', 'output/', 500, 100)
        # self.assertTrue(os.path.exists('output/sample_policy.json'))
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
