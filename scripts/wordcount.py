"""Print the most frequent words in a text file.

Usage:
    python scripts/wordcount.py <file path>

Words are runs of letters and digits; every other character separates words.
Matching is case-insensitive, so "The" and "the" are counted together.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

TOP_N = 10

WORD_RE = re.compile(r"[A-Za-z0-9]+")


def count_words(text: str) -> Counter[str]:
    """Return case-insensitive word counts for ``text``."""
    return Counter(word.lower() for word in WORD_RE.findall(text))


def top_words(counts: Counter[str], n: int = TOP_N) -> list[tuple[str, int]]:
    """Return the ``n`` most common words, most frequent first.

    Ties are broken alphabetically so the output is deterministic.
    """
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]


def render(results: list[tuple[str, int]]) -> str:
    """Render results as one ``word count`` line per word."""
    return "".join(f"{word} {count}\n" for word, count in results)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: python scripts/wordcount.py <file path>", file=sys.stderr)
        return 2

    path = Path(args[0])
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2
    except UnicodeDecodeError:
        print(f"error: {path} is not valid UTF-8 text", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    sys.stdout.write(render(top_words(count_words(text))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
