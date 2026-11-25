#!/usr/bin/env python3
"""The Best Advice I Ever Got — make.fun entry.

Writes one sentence about the best advice the writer ever received
to /output/entry.txt (gate: UTF-8, 1-200 characters, single sentence).

One-liner candidate tournament (specificity / surprise / freshness):
  1. Grandfather: fix the fence before the storm, not after - 4/4/4 = 12
  2. Mother: if you cannot say it to their face, do not type it - 5/5/4 = 14
  3. First boss: never trust a deadline with no name attached - 5/4/4 = 13
  4. Father: the cheapest thing you own is your word - 5/5/4 = 14
  5. Grandmother: spare key under the third flowerpot, leave a way back in
     - 5/5/5 = 15 (WINNER)
  6. Teacher: you are not behind, you are on a longer road - 5/4/4 = 13
  7. Uncle: never borrow trouble from tomorrow - 4/4/3 = 11

Winner: the grandmother line. A concrete object (third flowerpot) and a
literal key that turns into a rule for a whole life: specific, earned,
a real voice recalling a real moment, not a slogan. Flooded moves
avoided: "never give up", "be yourself", "follow your dreams".
"""

import argparse
import os
import sys

ENTRY = (
    "My grandmother kept a spare key under the third flowerpot and told me, "
    "'Always leave a way back in,' and I still do, in every part of my life."
)

GATE_MIN = 1
GATE_MAX = 200

TOURNAMENT = [
    ("Grandfather: fix the fence before the storm, not after", 4, 4, 4),
    ("Mother: if you cannot say it to their face, do not type it", 5, 5, 4),
    ("First boss: never trust a deadline with no name attached", 5, 4, 4),
    ("Father: the cheapest thing you own is your word", 5, 5, 4),
    ("Grandmother: spare key under the third flowerpot", 5, 5, 5),
    ("Teacher: you are not behind, you are on a longer road", 5, 4, 4),
    ("Uncle: never borrow trouble from tomorrow", 4, 4, 3),
]


def entry_path() -> str:
    """Absolute output path; falls back to a local output dir for dev runs."""
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "entry.txt")


def check_entry(text: str) -> list:
    """Return a list of gate violations (empty when the entry is valid)."""
    problems = []
    if not (GATE_MIN <= len(text) <= GATE_MAX):
        problems.append(
            "length %d outside gate %d-%d" % (len(text), GATE_MIN, GATE_MAX)
        )
    if not text.strip():
        problems.append("entry is only whitespace")
    if text.count(".") + text.count("!") + text.count("?") < 1:
        problems.append("entry is not a sentence")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:  # pragma: no cover - defensive
        problems.append("not valid UTF-8: %s" % exc)
    return problems


def write_entry(path: str) -> str:
    """Write the entry and return the path written."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="validate the entry against the gate and exit")
    parser.add_argument("--self-test", action="store_true",
                        help="write, read back and compare byte for byte")
    parser.add_argument("--tournament", action="store_true",
                        help="print the candidate tournament scores")
    args = parser.parse_args(argv)

    if args.tournament:
        for name, spec, surp, fresh in TOURNAMENT:
            print("%s - %d/%d/%d = %d" % (name, spec, surp, fresh, spec + surp + fresh))
        print("winner: Grandmother, 15/15")
        return 0

    if args.check:
        problems = check_entry(ENTRY)
        print("entry: %d chars, %d bytes"
              % (len(ENTRY), len(ENTRY.encode("utf-8"))))
        if problems:
            for problem in problems:
                print("FAIL: %s" % problem)
            return 1
        print("check ok: %d chars, within gate %d-%d"
              % (len(ENTRY), GATE_MIN, GATE_MAX))
        return 0

    if args.self_test:
        path = entry_path()
        write_entry(path)
        with open(path, "rb") as handle:
            back = handle.read().decode("utf-8")
        if back != ENTRY:
            print("FAIL: round-trip mismatch")
            return 1
        print("self-test ok: %d bytes round-trip byte-identical" % len(back.encode("utf-8")))
        return 0

    path = write_entry(entry_path())
    print("wrote %s (%d chars)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
