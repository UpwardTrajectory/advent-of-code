from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import numpy as np


T1_ANS = 5934
T2_ANS = 26984457539


@dataclass
class Puzzle:
    fname: str
    
    def __post_init__(self):
        raw = Path(self.fname).open().read()
        self.initial = self.build_init_vector(raw)

    @staticmethod        
    def build_matrix():
        mtrx = np.zeros((9, 9), 'int64')
        mtrx[1:, :-1] = np.diag(np.ones(8, 'int64'))
        mtrx[0, [6,8]] = 1
        return mtrx

    @staticmethod
    def build_init_vector(incoming_str):
        vec = np.zeros((9, 1), 'int64')
        initial_fishes = Counter(map(int, incoming_str.split(",")))
        
        for num, cnt in initial_fishes.items():
            vec[num, 0] = cnt
            
        return vec

    def get_population(self, n):
        mtrx = self.build_matrix()       
        total = np.linalg.matrix_power(mtrx, n)
        return (self.initial * total).sum()
    
    def part_1(self):
        return self.get_population(80)
    
    def part_2(self):
        return self.get_population(256)

    
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