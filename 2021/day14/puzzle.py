from pathlib import Path
from dataclasses import dataclass, field
import numpy as np
import pandas as pd


T1_ANS = 1588
T2_ANS = 2188189693529


@dataclass
class Puzzle:
    fname: str
    bigrams: list[str] = field(default_factory=list, repr=False)
    matrix: pd.DataFrame = None
    initial: pd.DataFrame = None
    initial_str: str = None

    def __post_init__(self):
        raw = Path(self.fname).open().read()
        initial, polyforms = raw.split("\n\n")

        polyforms = {tuple(row.split(" -> ")) for row in polyforms.split("\n")}
        self.bigrams = [row[0] for row in polyforms]
        self.matrix = self.build_matrix(polyforms)
        self.initial_str = initial
        self.initial = self.build_init_vector()
        return

    def build_matrix(self, polyforms: list[tuple[str, str]]) -> pd.DataFrame:
        bigrams = self.bigrams
        mtrx = pd.DataFrame(
            np.zeros((len(bigrams), len(bigrams))),
            index=bigrams,
            columns=bigrams,
            dtype="int64",
        )

        for old, insert in polyforms:
            mtrx.loc[old, insert + old[1]] = 1
            mtrx.loc[old, old[0] + insert] = 1

        return mtrx

    def build_init_vector(self) -> pd.DataFrame:
        init_vec = pd.DataFrame(
            [0] * len(self.bigrams), index=self.bigrams, columns=["cnt"]
        )

        for bigram in zip(self.initial_str[:-1], self.initial_str[1:]):
            poly_name = "".join(bigram)
            init_vec.loc[poly_name, "cnt"] += 1

        return init_vec

    def poly_transform(self, n):
        bigrams = self.bigrams
        new_mtrx = np.linalg.matrix_power(self.matrix, n)
        new_mtrx = self.initial.to_numpy() * new_mtrx
        return pd.DataFrame(new_mtrx, index=bigrams, columns=bigrams, dtype="int64")

    def final_counts(self, n):
        mtrx = self.poly_transform(n)
        mtrx_counts = mtrx.sum(axis=0).to_dict()

        counts = {ltr: 0 for ltr in set("".join(self.bigrams))}

        for bigram, total in mtrx_counts.items():
            counts[bigram[0]] += total
            counts[bigram[1]] += total

        counts[self.initial_str[0]] += 1
        counts[self.initial_str[-1]] += 1

        return {ltr: cnt // 2 for ltr, cnt in counts.items()}

    def part_1(self):
        counts = self.final_counts(10).values()
        return max(counts) - min(counts)

    def part_2(self):
        counts = self.final_counts(40).values()
        return max(counts) - min(counts)


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