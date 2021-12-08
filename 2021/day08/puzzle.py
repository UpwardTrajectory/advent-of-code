from pathlib import Path
from dataclasses import dataclass, field
from collections import Counter


@dataclass
class Observation:
    raw: list[str]
    _in: list[set[str]] = field(default_factory=list, repr=False)
    _out: list[str] = field(default_factory=list, repr=False)
    code: dict[int:str] = field(default_factory=dict, repr=False)
    counts: Counter = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """set codes directly for:
            nums: 1,4,7,8
        
        use self.update_codes() to find:
            nums: 0, 2, 3, 5, 6, 9
            pos: UL, UR   
        
        other positions are decorated w/ @property
        """
        pre, post = self.raw.split("|")
        self.counts = Counter(pre.replace(" ", ""))

        self._in = list(set(x) for x in pre.strip().split(" "))
        self._out = ["".join(sorted(x)) for x in post.strip().split(" ")]

        len_5 = set()
        len_6 = set()

        for code in self._in:
            L = len(code)
            if L == 2:
                self.code[1] = code
            if L == 3:
                self.code[7] = code
            if L == 4:
                self.code[4] = code
            if L == 5:
                if not len_5:
                    len_5 = code
                else:
                    len_5 &= code
            if L == 6:
                if not len_6:
                    len_6 = code
                else:
                    len_6 &= code
            if L == 7:
                self.code[8] = code

        self.len_5 = len_5
        self.len_6 = len_6

        self.update_codes()

        return

    @property
    def top(self):
        return self.code[7] - self.code[1]

    @property
    def mid(self):
        return self.len_5 - self.len_6

    @property
    def LL(self):
        return set([x for x in self.counts if self.counts[x] == 4])

    @property
    def UL(self):
        return set([x for x in self.counts if self.counts[x] == 6])

    @property
    def LR(self):
        return set([x for x in self.counts if self.counts[x] == 9])

    def update_codes(self):
        """self.UL and self.UR cannot be learned until after some extra """
        self.code[0] = self.code[8] - self.mid
        self.code[3] = self.len_5 | self.code[1]

        self.UR = self.code[4] - set.union(self.UL, self.mid, self.LR)
        self.bot = self.code[3] - self.code[4] - self.top

        self.code[6] = self.code[8] - self.UR
        self.code[2] = self.code[8] - self.LR - self.UL
        self.code[5] = self.code[6] - self.LL
        self.code[9] = self.code[8] - self.LL
        return

    def parse_outputs(self):
        code_to_num = {"".join(sorted(list(v))): k for k, v in self.code.items()}
        digits_out = [str(code_to_num[code]) for code in self._out]
        return int("".join(digits_out))


@dataclass
class EasyDigits:
    fpath: str
    # raw_inputs: list[str] = field(default_factory=list, repr=False)
    lines: list[Observation] = None
    # raw_outputs: list[str] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        lines = Path(self.fpath).read_text().split("\n")
        self.lines = [Observation(line) for line in lines]

        return

    def part_1(self) -> int:
        n_segments: "{num_segments: actual_num}" = {2: 1, 4: 4, 3: 7, 7: 8}
        num_easy = 0
        for line in self.lines:
            raw = line.raw.split(" | ")[-1]
            obs = raw.split(" ")
            for num in obs:
                if len(num) in n_segments:
                    num_easy += 1
        return num_easy

    def part_2(self) -> int:
        return sum(line.parse_outputs() for line in self.lines)


def run_tests(p1_ans, p2_ans=None, fname="tests.txt"):
    digits = EasyDigits("tests.txt")
    t1 = digits.part_1()
    assert t1 == p1_ans, f"Test 1 failed. Got {t1} instead of {p1_ans}"

    if p2_ans is not None:
        t2 = digits.part_2()
        assert t2 == p2_ans, f"Test 2 failed. Got {t2} instead of {p2_ans}"

    print("All tests passed.")
    return


if __name__ == "__main__":
    run_tests(26, 61229)

    digits = EasyDigits("inputs.txt")

    p1 = digits.part_1()
    print("Part 1:", p1)

    p2 = digits.part_2()
    print("Part 2:", p2)
