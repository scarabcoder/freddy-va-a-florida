# Ramp Schedule & Invariants

## Measurement note
Percentages below are **true word count** (Spanish word-tokens ÷ total word-tokens),
measured on prose only (excluding footnote definitions and the Vocabulario table).
An English-skeleton weave caps out around ~15-20% because English function words
(the, of, and, to, was…) stay English. To climb higher the **sentence skeleton must
flip to Spanish** — that is the mid-book transition below.

## Ramp schedule (agreed shape: gradual mid-book flip)

| Chapters | Skeleton | Target Spanish (true word count) | Character |
|----------|----------|----------------------------------|-----------|
| 1–4 | English | ~15–22% | English carries structure; Spanish = concrete nouns, colors, simple adjectives, high-frequency verbs (dijo, preguntó), set time phrases. Ch.1 floor ≈ 15%. |
| 5–7 | English, thickening | ~22–32% | More Spanish verbs and short Spanish clauses inside English sentences. |
| 8–11 | Mixing | ~35–50% | Sentences start flipping: many full Spanish clauses joined by English connectives (Sample B feel). |
| 12–14 | Mostly Spanish | ~50–65% | Spanish skeleton dominant; English for hard/abstract words and bridges. |
| 15–18 | Spanish | ~68–75% | Spanish skeleton throughout; English only for hard words. |
| 19–21 | Spanish | ~78–82% | True ~80% Spanish (Sample C feel); English only for rare hard words. |

Density must be **monotonic** — no chapter lighter than the one before it.

## Invariants for every chapter
- Neutral **Mexican** Spanish (`ustedes`, never `vosotros`); Mexican lexicon
  (cobija, parvada, puerco, platicar, carro, etc.) where natural.
- Story / plot / dialogue meaning unchanged; preserve every sentence and paragraph,
  in order. Character names unchanged (Charles, Mr. Bean, Jinx, Freddy, Hank…).
- Every Spanish word inferable from context or covered by a first-use gloss.
- Spanish clauses fully grammatical (agreement, conjugation, gender).
- **Consistent word mappings** across chapters: a word in the cumulative glossary
  (`tools/glossary.json`) is reused with the SAME Spanish choice and is **not**
  re-glossed (e.g. barnyard → corral, said → dijo, henhouse → gallinero, always).
- Only genuinely NEW Spanish words get a `[^id]` footnote + a Vocabulario row.

## Per-chapter file format
`# Capítulo <ROMAN>` heading → woven prose → footnote definitions → `## Vocabulario`
table (Spanish | English). Validate with
`python3 tools/check_chapter.py output/NN-capitulo.md tools/glossary.json` (must be
ERROR-free), then lock vocab with the same command plus `--add`.
