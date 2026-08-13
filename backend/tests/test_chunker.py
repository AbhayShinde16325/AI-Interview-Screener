import unittest

from app.ai.retrieval.chunker import DocumentChunker


class TestDocumentChunker(unittest.TestCase):

    def setUp(self):
        self.chunker = DocumentChunker(chunk_size=200, overlap=40)

    def test_empty_text_returns_no_chunks(self):
        self.assertEqual(self.chunker.chunk(""), [])

    def test_short_text_stays_single_chunk(self):
        chunks = self.chunker.chunk("Short document with a few words.")
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], "Short document with a few words.")

    def test_chunks_never_exceed_limit_much(self):
        text = "Paragraph one with a bit of content.\n\n" * 50
        chunks = self.chunker.chunk(text)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            # chunk_size + sentence spill is allowed, but not wildly larger
            self.assertLessEqual(len(chunk), 400)

    def test_headings_create_sections(self):
        text = "# Section One\n\nSome body text for section one.\n\n" \
               "# Section Two\n\nSome body text for section two."
        chunks = self.chunker.chunk(text)
        joined = "\n".join(chunks)
        self.assertIn("# Section One", joined)
        self.assertIn("# Section Two", joined)

    def test_no_empty_chunks(self):
        text = "a " * 500
        chunks = self.chunker.chunk(text)
        for chunk in chunks:
            self.assertTrue(chunk.strip())


if __name__ == "__main__":
    unittest.main()
