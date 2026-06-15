# tools/check_chapter.py
import json
import re
import sys

_REF_RE = re.compile(r"\[\^([^\]]+)\](?!:)")   # [^id] not followed by ':'
_DEF_RE = re.compile(r"^[ ]{0,3}\[\^([^\]]+)\]:", re.MULTILINE)


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
    seen = set()
    for h in heads:
        if h in seen:
            errors.append(f"vocab '{h}' listed more than once in this chapter")
        seen.add(h)
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
