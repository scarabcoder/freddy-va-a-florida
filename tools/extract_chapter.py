# tools/extract_chapter.py
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
