# Spanish/English Diglot-Weave Edition — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a graded-reader edition of *Freddy Goes to Florida* that weaves Mexican Spanish into the English prose, ramping from ~35% Spanish (Ch. 1) to ~80% Spanish (Ch. 21), with first-use glosses and per-chapter vocab lists.

**Architecture:** Two small stdlib-Python tools provide the rails — `extract_chapter.py` splits the source novel into chapters by its Roman-numeral markers, and `check_chapter.py` validates each output Markdown file's structure (footnote integrity, vocab section, first-use-only glossing against a cumulative glossary). The creative weaving is done per chapter following a fixed procedure and ramp schedule, gated by a pilot review of Chapter 1.

**Tech Stack:** Python 3.10 (stdlib only: `re`, `json`, `unittest`), Markdown output, git for versioning. Tests run with `python3 -m unittest`.

**Reference spec:** `docs/superpowers/specs/2026-06-15-spanish-diglot-blend-design.md`

---

## File Structure

- `tools/extract_chapter.py` — split source `.txt` into front matter + numbered chapters.
- `tools/check_chapter.py` — validate one output chapter `.md`; read/update cumulative glossary.
- `tools/glossary.json` — cumulative list of Spanish headwords already glossed (first-use tracking). Shared state across chapters.
- `tools/ramp.md` — the per-chapter density target table (reference for the writer).
- `tests/test_extract_chapter.py` — unit tests for the extractor.
- `tests/test_check_chapter.py` — unit tests for the validator.
- `output/00-portada.md` — front matter / title page (woven lightly or kept English).
- `output/NN-capitulo.md` — one file per chapter, `01`–`21`.
- `output/README.md` — index linking all chapters.
- Source `Freddy Goes to Florida.txt` — **never modified**.

---

## Ramp Schedule (reference for every weaving task)

| Chapters | Target Spanish (by word count) | Character |
|----------|-------------------------------|-----------|
| 1–4 | ~35–42% | English skeleton; Spanish = concrete nouns, colors, simple adjectives, set phrases |
| 5–9 | ~45–55% | Spanish verbs + short clauses enter |
| 10–14 | ~55–65% | Mixed skeleton; full Spanish clauses joined by English connectives |
| 15–18 | ~68–75% | Spanish skeleton; English for hard/abstract words + bridges |
| 19–21 | ~78–80% | True 80% Spanish skeleton; English only for rare hard words |

**Invariants for every chapter:** neutral Mexican Spanish (`ustedes`, never `vosotros`); story/plot/names unchanged; every Spanish word inferable from context or gloss; Spanish clauses fully grammatical; consistent word mappings across chapters (e.g. *barnyard* → `corral` always).

---

## Task 1: Project scaffold

**Files:**
- Create: `tools/ramp.md`
- Create: `tools/glossary.json`
- Create: `output/.gitkeep`
- Create: `tests/.gitkeep`

- [ ] **Step 1: Create directories and the ramp reference**

```bash
mkdir -p tools output tests
touch output/.gitkeep tests/.gitkeep
```

Create `tools/ramp.md` containing the **Ramp Schedule** table and the **Invariants** block from this plan (copy them verbatim so the writer has a single reference).

- [ ] **Step 2: Initialize the cumulative glossary**

Create `tools/glossary.json` with an empty list:

```json
[]
```

- [ ] **Step 3: Commit**

```bash
git add tools/ramp.md tools/glossary.json output/.gitkeep tests/.gitkeep
git commit -m "chore: scaffold tools/output/tests for diglot edition"
```

---

## Task 2: Chapter extractor (TDD)

**Files:**
- Create: `tools/extract_chapter.py`
- Test: `tests/test_extract_chapter.py`

The extractor splits the source on lines that are *exactly* a chapter Roman numeral (after stripping whitespace — handles both centered markers and the left-margin `XX`). Everything before the first marker is "front matter".

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_extract_chapter -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'tools.extract_chapter'` (or ImportError).

- [ ] **Step 3: Write minimal implementation**

```python
# tools/extract_chapter.py
import re
import sys

# Exact Roman numerals for chapters I..XXI (extend if a longer source is used).
CHAPTER_NUMERALS = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI",
]
_NUMERAL_SET = set(CHAPTER_NUMERALS)


def is_chapter_marker(line):
    """A line that, stripped, is exactly one of the chapter numerals."""
    return line.strip() in _NUMERAL_SET


def split_chapters(text):
    """Return (front_matter_str, [(numeral, body_str), ...]) in document order."""
    front = []
    chapters = []
    current_num = None
    current_body = []
    for line in text.splitlines():
        if is_chapter_marker(line):
            if current_num is not None:
                chapters.append((current_num, "\n".join(current_body)))
            else:
                front = current_body  # lines seen before first marker
            current_num = line.strip()
            current_body = []
        else:
            current_body.append(line)
    if current_num is not None:
        chapters.append((current_num, "\n".join(current_body)))
    else:
        front = current_body
    return "\n".join(front), chapters


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        front, chapters = split_chapters(fh.read())
    print(f"front matter: {len(front.split())} words")
    for num, body in chapters:
        print(f"Chapter {num}: {len(body.split())} words")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_extract_chapter -v`
Expected: PASS (3 tests OK).

- [ ] **Step 5: Sanity-run on the real source and confirm 21 chapters**

Run: `python3 tools/extract_chapter.py "Freddy Goes to Florida.txt"`
Expected: a `front matter:` line followed by exactly 21 `Chapter ...` lines, I through XXI, each with a plausible word count (hundreds to ~2000).

- [ ] **Step 6: Commit**

```bash
git add tools/extract_chapter.py tests/test_extract_chapter.py
git commit -m "feat: add chapter extractor with tests"
```

---

## Task 3: Chapter validator (TDD)

**Files:**
- Create: `tools/check_chapter.py`
- Test: `tests/test_check_chapter.py`

Validates one output chapter `.md`: (a) footnote refs and defs match exactly, (b) a `## Vocabulario` table exists with ≥1 row, (c) no headword in this chapter's vocab already exists in the cumulative glossary (first-use rule). Returns structured results; CLI prints them and exits non-zero on failure. An `--add` flag appends this chapter's new headwords to the glossary after a clean check.

Vocab table format (first column = Spanish headword):

```markdown
## Vocabulario

| Español | English |
|---------|---------|
| gallinero | henhouse |
| corral | barnyard |
```

- [ ] **Step 1: Write the failing test**

```python
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

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_check_chapter -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'tools.check_chapter'`.

- [ ] **Step 3: Write minimal implementation**

```python
# tools/check_chapter.py
import json
import re
import sys

_REF_RE = re.compile(r"\[\^([^\]]+)\](?!:)")   # [^id] not followed by ':'
_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:", re.MULTILINE)


def footnote_refs(md):
    return set(_REF_RE.findall(md))


def footnote_defs(md):
    return set(_DEF_RE.findall(md))


def vocab_headwords(md):
    """First column of the table under a '## Vocabulario' heading, in order."""
    lines = md.splitlines()
    out = []
    in_vocab = False
    for line in lines:
        if re.match(r"^##\s+Vocabulario\s*$", line):
            in_vocab = True
            continue
        if in_vocab and re.match(r"^##\s+", line):
            break  # next section ends the vocab block
        if in_vocab and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            head = cells[0]
            if not head or head.lower() in ("español", "espanol") or set(head) <= set("-: "):
                continue  # header row or separator row
            out.append(head)
    return out


def check_chapter(md, glossary):
    """Return (ok, errors, headwords). `glossary` is a set of prior headwords."""
    errors = []
    refs, defs = footnote_refs(md), footnote_defs(md)
    for missing in sorted(refs - defs):
        errors.append(f"footnote ref [^{missing}] has no matching definition")
    for orphan in sorted(defs - refs):
        errors.append(f"footnote def [^{orphan}] is never referenced")

    heads = vocab_headwords(md)
    if not heads:
        errors.append("no '## Vocabulario' table rows found")
    for h in heads:
        if h in glossary:
            errors.append(f"vocab '{h}' already glossed in an earlier chapter (first-use rule)")

    return (len(errors) == 0, errors, heads)


def main():
    md_path = sys.argv[1]
    glossary_path = sys.argv[2] if len(sys.argv) > 2 else "tools/glossary.json"
    do_add = "--add" in sys.argv[3:]

    with open(md_path, encoding="utf-8") as fh:
        md = fh.read()
    with open(glossary_path, encoding="utf-8") as fh:
        glossary = set(json.load(fh))

    ok, errors, heads = check_chapter(md, glossary)
    wc = len(md.split())
    print(f"{md_path}: {wc} words, {len(heads)} new vocab")
    for e in errors:
        print(f"  ERROR: {e}")
    if ok and do_add:
        merged = sorted(glossary | set(heads))
        with open(glossary_path, "w", encoding="utf-8") as fh:
            json.dump(merged, fh, ensure_ascii=False, indent=2)
        print(f"  added {len(heads)} headwords to {glossary_path}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_check_chapter -v`
Expected: PASS (5 tests OK).

- [ ] **Step 5: Commit**

```bash
git add tools/check_chapter.py tests/test_check_chapter.py
git commit -m "feat: add chapter validator with tests"
```

---

## Task 4: Chapter 1 pilot (PILOT GATE)

**Files:**
- Create: `output/01-capitulo.md`

This is the calibration gate. Produce Chapter 1 at the **~35% / English-skeleton** density (Sample A feel), get user sign-off on the feel before batching.

- [ ] **Step 1: Extract the Chapter 1 source text**

Run: `python3 tools/extract_chapter.py "Freddy Goes to Florida.txt"`
Read the Chapter I body (source lines ~90–259). Keep the original sentence order and all story content.

- [ ] **Step 2: Weave Chapter 1 into `output/01-capitulo.md`**

Follow these rules exactly:
- Density target: **~35–42% Spanish** by word count (count Spanish words ÷ total words).
- Keep English as the sentence skeleton; swap concrete nouns, colors, simple adjectives, and set time phrases to Spanish (e.g. `el gallo`, `gallinero`, `corral`, `muy oscuro`, `de la mañana`, `el sol`).
- Mexican Spanish, `ustedes`, names unchanged (Charles, Mr. Bean, Jinx, Freddy).
- The **first time** any Spanish word/phrase appears, add a footnote `[^id]` and a definition `[^id]: word (english)`.
- File layout:

```markdown
# Capítulo I

<woven prose, original paragraphs preserved>

<!-- footnote definitions -->
[^gallo]: gallo (rooster)
[^gallinero]: gallinero (henhouse)

## Vocabulario

| Español | English |
|---------|---------|
| gallo | rooster |
| gallinero | henhouse |
```

Opening paragraph target (reference — match this density):

> Charles, el gallo[^gallo], came out of the front door of the gallinero[^gallinero] and walked slowly across the corral[^corral]. It was still muy oscuro[^oscuro], for it was half past four de la mañana[^manana], and the sol[^sol] was not yet up. He shivered and thought of his nice warm perch in the coop, but había una razón[^razon] why he did not go back to it.

- [ ] **Step 3: Validate structure**

Run: `python3 tools/check_chapter.py output/01-capitulo.md tools/glossary.json`
Expected: `output/01-capitulo.md: <N> words, <M> new vocab` and **no `ERROR:` lines** (exit 0). Fix any footnote/vocab mismatches reported.

- [ ] **Step 4: Spot-check the Spanish ratio**

Manually estimate: pick 3 paragraphs, count Spanish words ÷ total words. Expected: each ≈ 0.35–0.45. If consistently below ~0.30 or above ~0.50, adjust the weave and re-run Step 3.

- [ ] **Step 5: Commit (glossary NOT yet updated — wait for user approval)**

```bash
git add output/01-capitulo.md
git commit -m "feat: Chapter 1 pilot (diglot weave ~35% Spanish)"
```

- [ ] **Step 6: PILOT GATE — get user sign-off**

Present `output/01-capitulo.md` to the user. Ask them to confirm: ratio feel, Mexican word choices, gloss frequency, formatting. **Do not proceed to Task 5 until approved.** Apply any requested calibration changes to this chapter and re-run Steps 3–5 first.

- [ ] **Step 7: Lock Chapter 1 vocab into the glossary**

After approval, append Chapter 1's headwords:

Run: `python3 tools/check_chapter.py output/01-capitulo.md tools/glossary.json --add`
Expected: ends with `added <M> headwords to tools/glossary.json` (exit 0).

```bash
git add tools/glossary.json
git commit -m "chore: lock Chapter 1 vocab into cumulative glossary"
```

---

## Task 5: Batch Chapters 2–21

**Files:**
- Create: `output/02-capitulo.md` … `output/21-capitulo.md`

Repeat the following per chapter **in order** (sequential, because the glossary is shared first-use state). Use the **Ramp Schedule** to pick each chapter's density band.

For chapter `NN` (zero-padded) with numeral `ROMAN`:

- [ ] **Step 1: Extract the chapter's source text** via `python3 tools/extract_chapter.py "Freddy Goes to Florida.txt"` and locate the `ROMAN` body.

- [ ] **Step 2: Weave** into `output/NN-capitulo.md` at the band's target density, following all invariants. Reuse established word mappings (a word glossed earlier is now used **without** a new gloss). Only genuinely new Spanish words get `[^id]` footnotes + vocab rows. Heading: `# Capítulo ROMAN`.

- [ ] **Step 3: Validate** — Run: `python3 tools/check_chapter.py output/NN-capitulo.md tools/glossary.json`. Expected: no `ERROR:` lines (exit 0). In particular, a "already glossed in an earlier chapter" error means you re-glossed a known word — remove that footnote/vocab row. Fix and re-run until clean.

- [ ] **Step 4: Ratio spot-check** — 3 paragraphs, Spanish ÷ total within the band's range (per the Ramp Schedule). Adjust if out of range.

- [ ] **Step 5: Lock vocab + commit** —

```bash
python3 tools/check_chapter.py output/NN-capitulo.md tools/glossary.json --add
git add output/NN-capitulo.md tools/glossary.json
git commit -m "feat: Chapter ROMAN diglot weave (band <range>%)"
```

Repeat Steps 1–5 for each of chapters 2 through 21. Density must be monotonic — no chapter lighter than the previous one.

---

## Task 6: Front matter and index

**Files:**
- Create: `output/00-portada.md`
- Create: `output/README.md`

- [ ] **Step 1: Create the title page** `output/00-portada.md` — the book title, author, a one-line note that this is a Spanish/English graded-reader adaptation for learners, and the public-domain attribution from the source front matter. Keep this page mostly English (it's orientation, not story).

- [ ] **Step 2: Create the index** `output/README.md` — a short intro explaining the diglot method and how to read it (glosses on first use, vocab list per chapter, Spanish density rising across the book), followed by a linked list:

```markdown
# Freddy Goes to Florida — Edición Diglot (ES/EN)

A graded-reader adaptation: Spanish woven into the English, ramping from ~35% to ~80%.
First use of each Spanish word is glossed; each chapter ends with a `Vocabulario` list.

## Capítulos
- [Portada](00-portada.md)
- [Capítulo I](01-capitulo.md)
- [Capítulo II](02-capitulo.md)
- … through Capítulo XXI
```

- [ ] **Step 3: Commit**

```bash
git add output/00-portada.md output/README.md
git commit -m "docs: add portada and chapter index"
```

---

## Task 7: Whole-book audit

**Files:**
- (No new files — verification + possible fixes to existing chapters.)

- [ ] **Step 1: Re-validate every chapter against the final glossary**

Run:

```bash
for f in output/0*-capitulo.md output/1*-capitulo.md output/2*-capitulo.md; do
  python3 tools/check_chapter.py "$f" tools/glossary.json || echo "FAILED: $f"
done
```

Note: this re-check uses the *final* cumulative glossary, so first-use errors will appear for words a chapter legitimately introduced (they're now in the glossary). Treat only **footnote-integrity** and **missing-vocab** errors as real failures here; ignore "already glossed" lines for chapters that were the original introducer. Fix any footnote/vocab structural failures.

- [ ] **Step 2: Ramp monotonicity check**

Skim the per-chapter word counts and your recorded ratios. Confirm density never decreases chapter-to-chapter and lands near ~80% by Ch. 21. Adjust any chapter that breaks the curve, then re-run its Task 5 Step 3 validation.

- [ ] **Step 3: Read-through sanity**

Read the first and last paragraphs of chapters 1, 7, 14, and 21. Confirm: the story is intact and legible, Spanish is correct Mexican Spanish, and the difficulty visibly rises. Fix issues in place and commit.

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "chore: whole-book audit pass for diglot edition"
```

---

## Notes for the implementer

- Run all tests any time you touch the tools: `python3 -m unittest discover -s tests -v`.
- Tools import as `tools.extract_chapter` / `tools.check_chapter`; run unittest from the repo root so the package path resolves (no `__init__.py` needed on Python 3.10 namespace packages, but if imports fail, add empty `tools/__init__.py` and `tests/__init__.py`).
- The source `.txt` is read-only — never edit it.
- Glossary updates happen **only** after a chapter is validated, via the `--add` flag, so first-use tracking stays accurate even if you redo a chapter.
