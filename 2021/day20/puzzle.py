from pathlib import Path
from typing import Literal
from itertools import product
from dataclasses import dataclass, field
import numpy as np


T1_ANS = 35
T2_ANS = None


@dataclass
class Puzzle:
    fname: str
    algo: str = field(default=None, repr=False)
    lookup: dict[str:str] = field(default_factory=dict, repr=False)
    img: np.array = None
    minigrid_dirs: list = field(default_factory=list, repr=False)

    def __post_init__(self):
        raw = Path(self.fname).open().readlines()  # or read() for a big block of text
        self.algo = raw[0].replace(".", "0").replace("#", "1").strip()

        possible_binary = list(product([0, 1], repeat=9))
        possible_binary = ["".join(str(x) for x in row) for row in possible_binary]

        self.lookup = {
            minigrid: int(self.algo[int(minigrid, 2)]) for minigrid in possible_binary
        }

        img = np.array(
            [list(row.replace(".", "0").replace("#", "1").strip()) for row in raw[2:]]
        ).astype(int)
        self.img = np.pad(img, 2)
        self.minigrid_dirs = list(product([-1, 0, 1], repeat=2))
        return

    def get_minigrid(self, row: int, col: int) -> str:
        """convert a row num & col num into a single 9-digit string of 0s & 1s
        
        These are conveniently the used like so:
          new_pixel = self.lookup[minigrid]
        """
        img = self.img
        ways = self.minigrid_dirs
        return "".join(str(img[row + way[0], col + way[1]]) for way in ways)

    def enhance(self):
        """Pad the image w/ 2 layers of zeros on each side, then 
        1) Iterate through the inner points NOT on the outermost layer
        2) get their minigrid string
        3) lookup the corresponding value in the algo
        4) save it to a new grid
        """
        nrows, ncols = self.img.shape

        pts = list(product(range(1, nrows-1), range(1, ncols-1)))
        new_img = np.zeros((nrows + 4, ncols + 4), dtype=int)

        for pt in pts:
            minigrid = self.get_minigrid(*pt)
            new_row = pt[0] + 2
            new_col = pt[1] + 2
            new_img[new_row, new_col] = self.lookup[minigrid]

        self.img = new_img
        return self

    def show(self):
        convert = {0: ".", 1: "#"}

        for row in self.img:
            print("".join(convert[x] for x in row))
        return

    def part_1(self):
        self.enhance()
        self.enhance()
        return self.img.sum()

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