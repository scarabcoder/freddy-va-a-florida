# tests/test_extract_chapter.py
import unittest
from tools.extract_chapter import split_chapters

SAMPLE = "\n".join([
    "Title page line",
    "I look about me this evening, said the speaker.",  # NOT a marker (full line)
    "",
    "                                   I",             # centered marker
    "First chapter text.",
    "More chapter one.",
    "                                  II",
    "Second chapter text.",
    "XX",                                                # left-margin marker
    "Twentieth chapter text.",
])

class TestSplitChapters(unittest.TestCase):
    def test_front_matter_separated(self):
        front, chapters = split_chapters(SAMPLE)
        self.assertIn("Title page line", front)
        self.assertIn("I look about me", front)  # prose 'I' line stays in front matter

    def test_chapter_numbers_and_order(self):
        _, chapters = split_chapters(SAMPLE)
        self.assertEqual([c[0] for c in chapters], ["I", "II", "XX"])

    def test_chapter_text_captured(self):
        _, chapters = split_chapters(SAMPLE)
        self.assertIn("First chapter text.", chapters[0][1])
        self.assertNotIn("Second chapter", chapters[0][1])
        self.assertIn("Twentieth chapter text.", chapters[2][1])

if __name__ == "__main__":
    unittest.main()
