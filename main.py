#!/usr/bin/env python3
"""One Word From Grandma: pick the single word a grandma would text about AI.

The judge compares two words at a time and picks the funnier, more
grandma-like one, weighing, most important first:

  1. it reads as the single word a grandma would text about AI;
  2. it sounds like a real grandmother's texting voice, warm and a little
     baffled, the way she would type it to a grandchild;
  3. it is funny in one word, with the joke landing without a caption;
  4. it feels tied to AI, robots or machines;
  5. it is a fresh pick rather than the obvious one, and still instantly
     readable.

Each candidate below is scored 0-5 on those four scored criteria (the
first is enforced by the gate: exactly one word, 1-30 characters). The
scores are combined with weights that keep the judge's own order --
voice first, then funny, then AI-tied, then fresh -- so a word can only
win on a later criterion when it is not beaten on an earlier one. The
winner is written, alone and with no trailing newline, to
/output/entry.txt, where the sealed gate scorer reads it.

Standard library only. No network, no randomness: the same run always
writes the same word.
"""

import os
import sys

# word, (grandma voice, funny in one word, tied to AI/robots, fresh pick)
CANDIDATES = [
    # The classic grandma misspelling of "computer": she does not say
    # "artificial intelligence", she calls the whole thing a compooter.
    # Warm, baffled, funny on its own, clearly about the machine, and
    # nobody's obvious first pick.
    ("COMPOOTER", (5, 5, 4, 4)),
    # Her typo for "robot": closer to the machine, but a thinner joke
    # than COMPOOTER and less warmly baffled.
    ("ROBUT", (4, 4, 5, 4)),
    # Peak grandma vocabulary for a thing she cannot name -- but it
    # could be about anything, not about AI.
    ("WHATSIT", (5, 3, 1, 3)),
    ("DOOHICKEY", (5, 3, 1, 3)),
    # A grandma-ish word for a gadget, but flat: no joke lands.
    ("GIZMO", (4, 2, 3, 2)),
    # A robot noise. A grandchild would text this, not a grandma.
    ("BEEPBOOP", (2, 3, 5, 3)),
    # A film reference, not a grandma's voice at all.
    ("SKYNET", (1, 2, 5, 2)),
    # The obvious pick: tied to AI and nothing else. No joke, no voice.
    ("ROBOT", (3, 1, 5, 1)),
    # What she might call it, but it fits any subject, not AI.
    ("MAGIC", (3, 2, 2, 1)),
    ("WOW", (3, 1, 1, 1)),
]

# Weights keep the judge's priority order: voice dominates funny,
# funny dominates AI-tied, AI-tied dominates fresh.
WEIGHTS = (1000, 100, 10, 1)

OUTPUT_PATH = os.environ.get("MAKEFUN_OUTPUT_PATH", "/output/entry.txt")


def score(entry):
    """Weighted score of one candidate, in the judge's criterion order."""
    _word, marks = entry
    return sum(mark * weight for mark, weight in zip(marks, WEIGHTS))


def pick_word():
    """The best candidate; ties go to the earliest listed (stable max)."""
    best = CANDIDATES[0]
    for entry in CANDIDATES[1:]:
        if score(entry) > score(best):
            best = entry
    return best[0]


def check_gate(word):
    """The sealed gate: UTF-8 text of 1 to 30 characters, not only
    whitespace, and exactly one word (no whitespace inside it). On top
    of the gate, letters only: the judge's brief allows no punctuation
    tricks, so a pick carrying punctuation, digits or symbols could
    never be the word a grandma would text."""
    if not 1 <= len(word) <= 30:
        raise ValueError("word must be 1-30 characters, got %d" % len(word))
    if not word.strip():
        raise ValueError("word must not be only whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be exactly one word")
    if not word.isalpha():
        raise ValueError("entry must be letters only, no punctuation")
    word.encode("utf-8")  # raises if not encodable UTF-8 text
    return word


def main():
    word = check_gate(pick_word())
    directory = os.path.dirname(OUTPUT_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(word)
    print("wrote %r (%d bytes) to %s" % (word, len(word.encode("utf-8")), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    sys.exit(main())
