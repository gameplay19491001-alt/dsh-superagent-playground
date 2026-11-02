"""Tests for scripts/wordcount.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "wordcount.py"


def run_wordcount(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def parse_output(stdout: str) -> list[tuple[str, int]]:
    return [
        (word, int(count))
        for word, count in (line.split(" ") for line in stdout.splitlines())
    ]


def write_text(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "input.txt"
    path.write_text(content, encoding="utf-8")
    return path


def test_normal_text_ranks_by_frequency(tmp_path: Path) -> None:
    path = write_text(
        tmp_path, "the quick brown fox jumps over the lazy dog the end"
    )

    result = run_wordcount(path)

    assert result.returncode == 0
    assert result.stderr == ""
    counts = parse_output(result.stdout)
    assert counts[0] == ("the", 3)
    # Everything else appears once, so 9 distinct words in total.
    assert len(counts) == 9
    frequencies = [count for _, count in counts]
    assert frequencies == sorted(frequencies, reverse=True)


def test_empty_file_produces_no_output(tmp_path: Path) -> None:
    result = run_wordcount(write_text(tmp_path, ""))

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_only_punctuation_produces_no_output(tmp_path: Path) -> None:
    result = run_wordcount(write_text(tmp_path, "!!! ,,, ... ??? -- *** \t\n"))

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_mixed_case_is_counted_case_insensitively(tmp_path: Path) -> None:
    path = write_text(tmp_path, "Hello hello HELLO world WORLD")

    result = run_wordcount(path)

    assert result.returncode == 0
    assert parse_output(result.stdout) == [("hello", 3), ("world", 2)]


def test_missing_file_exits_with_code_2(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist.txt"

    result = run_wordcount(missing)

    assert result.returncode == 2
    assert result.stdout == ""
    assert missing.name in result.stderr


def test_reports_at_most_ten_words(tmp_path: Path) -> None:
    # w1 appears 12 times, w2 eleven times, ... w12 once.
    content = " ".join(
        f"w{i}" for i in range(1, 13) for _ in range(13 - i)
    )
    result = run_wordcount(write_text(tmp_path, content))

    assert result.returncode == 0
    counts = parse_output(result.stdout)
    assert len(counts) == 10
    assert counts[0] == ("w1", 12)
    assert counts[-1] == ("w10", 3)
    assert {word for word, _ in counts}.isdisjoint({"w11", "w12"})


def test_digits_and_separators_are_handled(tmp_path: Path) -> None:
    path = write_text(tmp_path, "foo-bar baz_qux 42 ab12")

    result = run_wordcount(path)

    assert result.returncode == 0
    assert parse_output(result.stdout) == [
        ("42", 1),
        ("ab12", 1),
        ("bar", 1),
        ("baz", 1),
        ("foo", 1),
        ("qux", 1),
    ]
