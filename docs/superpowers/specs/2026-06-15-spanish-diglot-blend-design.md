# Design: Spanish/English Diglot-Weave Edition of *Freddy Goes to Florida*

**Date:** 2026-06-15
**Source:** `Freddy Goes to Florida.txt` — *To and Again* / *Freddy Goes to Florida* by Walter R. Brooks (1927), Canadian public domain, ~37,493 words, 21 chapters (I–XXI).
**Goal:** Produce a blended-language edition of the novel for a learner of Mexican Spanish, weaving Spanish into the English prose so reading the story doubles as graded Spanish practice.

## Purpose & Audience

The reader is an **A2 (advanced-beginner)** learner of **Mexican Spanish** who wants to acquire vocabulary and reading fluency by reading a story they enjoy, not a textbook. The blended text should be comprehensible at every point through context and glosses, while steadily pulling the reader toward reading real Spanish.

## Method: Word-Level Diglot Weave with a Difficulty Ramp

The core technique is the **diglot weave**: take English sentences and replace content words (nouns, verbs, adjectives, common phrases) with their Spanish equivalents, so meaning stays guessable from the surrounding English. As the book progresses, the weave deepens — more words per sentence become Spanish, and the *sentence frame itself* (word order, function words, verb conjugation) shifts from English to Spanish — until late chapters read as mostly-Spanish prose with occasional English lifelines.

### Density ramp (start ~35% → end ~80% Spanish by word count)

| Chapters | Target Spanish | Character of the weave |
|----------|---------------|------------------------|
| I–IV | ~35–42% | English skeleton; Spanish = concrete nouns, colors, simple adjectives, set phrases. (Sample A feel.) |
| V–IX | ~45–55% | Spanish verbs and short clauses enter; English still carries structure. |
| X–XIV | ~55–65% | Mixed skeleton; many full Spanish clauses joined by English connectives. (Sample B feel.) |
| XV–XVIII | ~68–75% | Spanish skeleton emerges; English reserved for hard/abstract words and bridges. |
| XIX–XXI | ~78–80% | True 80% Spanish skeleton; English only for rare hard words. (Sample C feel.) |

The ramp is gradual and monotonic — no chapter is easier than the one before it. Within a chapter the density is roughly constant; the steps happen between chapters.

### Reference samples (Chapter 1 opening)

**Sample A — ~35%, English skeleton (Ch. 1 target):**
> Charles, **el gallo**, came out of the front door of the **gallinero** and walked slowly across the **corral**. It was still **muy oscuro**, for it was half past four **de la mañana**, and the **sol** was not yet up. He shivered and thought of his nice warm perch in the coop, but **había una razón** why he did not go back to it.

**Sample B — ~60%, mixed skeleton (mid-book):**
> Charles, **el gallo, salió por la puerta del gallinero** and walked slowly across the **corral. Todavía estaba muy oscuro**, for it was half past four **de la mañana, y el sol aún no salía**. He shivered **y pensó en su percha calientita** in the coop, **pero había una razón** why he didn't want to go back.

**Sample C — ~80%, Spanish skeleton (final chapters target):**
> Charles, **el gallo, salió por la puerta del gallinero y caminó despacio por el corral. Todavía estaba muy oscuro, porque eran las cuatro y media de la mañana, y el sol aún no salía. Tembló de frío y pensó en su percha calientita** allá en the coop, but there was a reason **por la que no quería regresar.**

## Spanish Variety & Style Rules

- **Neutral Mexican Spanish.** Use `ustedes` (never `vosotros`). Prefer Mexican lexicon (`carro`, `platicar`, `¿mande?`, `chamba`, diminutives like `calientita`, `poquito`) where natural, but keep register broadly understandable — this is a children's adventure, not slang-heavy.
- **Preserve the story exactly.** No plot, dialogue, or meaning changes. Proper names (Charles, Freddy, Mr. Bean, Jinx) stay as-is. Only the *language of narration and dialogue* is woven.
- **Comprehensibility first.** A swapped word must be inferable from context or covered by a gloss. Never strand the reader.
- **Grammatical correctness.** When a clause is in Spanish, it must be fully correct Spanish (agreement, conjugation, gender) — not English words with Spanish vocabulary.
- **Consistency.** A given English word maps to the same Spanish choice throughout (e.g., *barnyard* → `corral`), so vocabulary compounds across chapters.

## Reading Aids

1. **Gloss on first use.** The first time a Spanish word (or fixed phrase) appears *in the whole book*, attach a footnote-style English gloss, e.g. `gallinero (henhouse)`. Subsequent uses are unglossed. A per-book "already glossed" set prevents re-glossing.
2. **End-of-chapter vocab list.** Each chapter file ends with a `## Vocabulario` table of the Spanish words/phrases *introduced in that chapter*, with English meanings, in order of appearance.

## Output Format

- **Markdown, one file per chapter:** `output/01-capitulo.md` … `output/21-capitulo.md` (plus an `output/00-portada.md` for the title/front matter and an `output/README.md` index).
- Glosses rendered as Markdown footnotes (`[^gallinero]`) collected at the bottom of each chapter, above the vocab list. (Footnotes degrade gracefully to readable text and convert cleanly to EPUB/PDF later.)
- Chapter heading retains the Roman numeral and any chapter title from the source.
- Source `.txt` is left untouched.

## Process

1. **Pilot — Chapter 1 only.** Produce `output/01-capitulo.md` at the Sample-A (~35%) density with glosses and vocab list. User reviews the *feel* (ratio, gloss density, Mexican word choices, formatting).
2. **Calibrate.** Adjust the style rules / ratio based on pilot feedback.
3. **Batch the rest (Ch. II–XXI).** Apply the agreed style and the ramp schedule, maintaining the shared glossed-word set and word-mapping consistency across chapters.
4. **Assemble.** Generate `output/README.md` index and `output/00-portada.md`.

## Non-Goals (YAGNI)

- No visual color-coding of Spanish (rejected in favor of gloss + vocab list).
- No audio, no spaced-repetition export, no app — plain readable files only.
- No EPUB build in this phase (format chosen to make it easy *later*).
- No grammar-explanation sidebars; this is extensive reading, not a textbook.

## Risks & Mitigations

- **Ratio drift across a long book.** Mitigate by spot-checking word-count ratio per chapter against the ramp table.
- **Inconsistent word mappings.** Mitigate with a maintained glossary/mapping carried between chapters.
- **Gloss bloat in early chapters** (many first-uses at once). Acceptable; density of *new* glosses naturally falls as the shared vocabulary grows.
- **A2 comprehension breaks** where a sentence goes fully Spanish too early. Mitigate by keeping the sentence *frame* English until the mid-book bands.
