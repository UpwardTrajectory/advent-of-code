from pathlib import Path
from dataclasses import dataclass, field
from statistics import median


T1_ANS = 26397
T2_ANS = 288957


@dataclass
class Navigation:
    raw: str
    incomplete: bool = field(default=None, repr=False)
    invalid: str = field(default=None, repr=False)

    def __post_init__(self):
        self.validate()
        return

    def validate(self):
        """Adapted from approach #3:
        https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-python/
        """
        my_string = self.raw
        brackets = ["()", "{}", "[]", "<>"]
        while any(pair in my_string for pair in brackets):
            for br in brackets:
                my_string = my_string.replace(br, "")
        self.incomplete = set(my_string).issubset(set("({[<"))
        if self.incomplete:
            self.needs_completing = my_string
        invalid_idx = [my_string.find(rt_br) for rt_br in ")}]>"]
        invalid_idx = [x for x in invalid_idx if x != -1]
        if invalid_idx:
            self.invalid = my_string[min(invalid_idx)]
        return self.incomplete, self.invalid

    def complete(self):
        """invalid takes precedence over incomplete, so if it
        is both, this code wil NOT complete an invalid line.
        """
        if not self.incomplete:
            return ""
        closer = {"(": ")", "{": "}", "[": "]", "<": ">"}
        return "".join(closer[b] for b in reversed(self.needs_completing))


@dataclass
class Puzzle:
    fname: str
    lines: list = None

    def __post_init__(self):
        raw = Path(self.fname).open().readlines()
        self.lines = [Navigation(line.strip()) for line in raw]

    def part_1(self):
        todo = [l for l in self.lines if l.invalid and not l.incomplete]
        scoring = {")": 3, "]": 57, "}": 1197, ">": 25137}
        return sum(scoring[line.invalid] for line in todo)

    def part_2(self):
        todo = [l for l in self.lines if l.incomplete and not l.invalid]
        scoring = {")": 1, "]": 2, "}": 3, ">": 4}

        scores = []
        for l in todo:
            r_brackets = l.complete()
            score = 0
            for br in r_brackets:
                score *= 5
                score += scoring[br]
            scores.append(score)

        return median(scores)


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