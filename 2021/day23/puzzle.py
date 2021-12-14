from pathlib import Path
from typing import Literal
from dataclasses import dataclass, field
import numpy as np


T1_ANS = 17
T2_ANS = None


@dataclass
class Puzzle:
    fname: str

    def __post_init__(self):
        raw = Path(self.fname).open().readlines()  # or read() for a big block of text
        
        return

    def part_1(self):
        pass

    def part_2(self):
        pass


def run_tests(p1_ans=T1_ANS, p2_ans=T2_ANS, fname="tests.txt"):
    puz = Puzzle(fname)
    t1 = puz.part_1()
    assert t1 == p1_ans, f"Test 1 failed. Got {t1} instead of {p1_ans}"

    if p2_ans is not None:
        t2 = puz.part_2()
        assert t2 == p2_ans, f"Test 2 failed. Got {t2} instead of {p2_ans}"

    print("All tests passed.")
    return


if __name__ == "__main__":
    run_tests()

    puz = Puzzle("inputs.txt")

    p1 = puz.part_1()
    print("Part 1:", p1)

    if T2_ANS is not None:
        p2 = puz.part_2()
        print("Part 2:", p2)