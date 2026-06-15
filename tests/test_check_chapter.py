# tests/test_check_chapter.py
import unittest
from tools.check_chapter import (
    footnote_refs, footnote_defs, vocab_headwords, check_chapter,
)

GOOD = """# Capítulo I

Charles, el gallo[^gallo], salió del gallinero[^gallinero].

[^gallo]: gallo (rooster)
[^gallinero]: gallinero (henhouse)

## Vocabulario

| Español | English |
|---------|---------|
| gallo | rooster |
| gallinero | henhouse |
"""

# A ref with no matching def, and a vocab word already in the glossary.
BAD = """# Capítulo II

El sol[^sol] y la luna[^luna].

[^sol]: sol (sun)

## Vocabulario

| Español | English |
|---------|---------|
| sol | sun |
"""

# An orphan footnote def: [^orphan] is defined but never referenced.
ORPHAN_DEF = """# Capítulo III

El río[^rio] corría.

[^rio]: río (river)
[^orphan]: orphan (huérfano)

## Vocabulario

| Español | English |
|---------|---------|
| río | river |
"""

# The same headword listed twice in this chapter's own Vocabulario table.
DUP_HEADWORD = """# Capítulo IV

La casa[^casa] grande.

[^casa]: casa (house)

## Vocabulario

| Español | English |
|---------|---------|
| casa | house |
| casa | home |
"""

# An indented footnote def (up to 3 leading spaces) with a matching ref.
INDENTED_DEF = """# Capítulo V

La nube[^nube] blanca.

   [^nube]: nube (cloud)

## Vocabulario

| Español | English |
|---------|---------|
| nube | cloud |
"""

class TestCheck(unittest.TestCase):
    def test_footnote_parsing(self):
        self.assertEqual(footnote_refs(GOOD), {"gallo", "gallinero"})
        self.assertEqual(footnote_defs(GOOD), {"gallo", "gallinero"})

    def test_vocab_headwords(self):
        self.assertEqual(vocab_headwords(GOOD), ["gallo", "gallinero"])

    def test_good_chapter_passes(self):
        ok, errors, _ = check_chapter(GOOD, glossary=set())
        self.assertTrue(ok, errors)
        self.assertEqual(errors, [])

    def test_missing_footnote_def_fails(self):
        ok, errors, _ = check_chapter(BAD, glossary=set())
        self.assertFalse(ok)
        self.assertTrue(any("luna" in e for e in errors))

    def test_first_use_violation_fails(self):
        ok, errors, _ = check_chapter(GOOD, glossary={"gallo"})
        self.assertFalse(ok)
        self.assertTrue(any("gallo" in e and "already" in e for e in errors))

    def test_orphan_footnote_def_fails(self):
        ok, errors, _ = check_chapter(ORPHAN_DEF, glossary=set())
        self.assertFalse(ok)
        self.assertTrue(any("orphan" in e for e in errors))

    def test_duplicate_headword_in_chapter_fails(self):
        ok, errors, _ = check_chapter(DUP_HEADWORD, glossary=set())
        self.assertFalse(ok)
        self.assertTrue(any("casa" in e and "more than once" in e for e in errors))

    def test_indented_footnote_def_has_no_missing_def_error(self):
        ok, errors, _ = check_chapter(INDENTED_DEF, glossary=set())
        self.assertFalse(any("no matching definition" in e for e in errors), errors)

if __name__ == "__main__":
    unittest.main()
