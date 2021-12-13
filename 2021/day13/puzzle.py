from pathlib import Path
from typing import Literal
from dataclasses import dataclass, field
import numpy as np


T1_ANS = 17
T2_ANS = None


@dataclass
class Puzzle:
    fname: str
    raw_coords: str = None
    grid: np.array = None
    folds: list[tuple[str, int]] = field(default_factory=list, repr=False)

    def __post_init__(self):
        raw = Path(self.fname).open().read()
        coords, folds = raw.split("\n\n")
        self.raw_coords = coords
        self.grid = self.parse_coords(coords)

        folds = [x[11:].split("=") for x in folds.split("\n")]
        self.folds = [(across_dim, int(val)) for across_dim, val in folds]
        return

    @staticmethod
    def parse_coords(coords: str) -> np.array:
        """Turns string of ...x1,y1\nx2,y2\n...
        into row & column locations, which then populates a numpy array
        to mark those positions
        """
        coords = np.array([x.split(",") for x in coords.split("\n")], dtype=int)
        rows = coords[:, 1]
        cols = coords[:, 0]
        grid = np.zeros((rows.max() + 1, cols.max() + 1), dtype=int)
        grid[rows, cols] = 1

        return grid

    def fold_vert(self, val) -> np.array:
        """Offset is needed to deal w/ even vs odd number of rows"""
        offset = int(self.grid.shape[0] % 2)

        top = self.grid[:val, :]
        bot = np.flipud(self.grid[val + offset :, :])
        top[-val - offset :, :] = top[-val - offset :, :] | bot
        return top

    def fold_horiz(self, val) -> np.array:
        """Offset is needed to deal w/ even vs odd number of columns"""
        offset = int(self.grid.shape[1] % 2)

        left = self.grid[:, :val]
        right = self.grid[:, val + offset :]
        right = np.fliplr(right)
        left[:, -val - offset :] = left[:, -val - offset :] | right
        return left

    def fold(self) -> np.array:
        """Read (& dispose of) the first 'fold' instruction and apply it to the grid."""
        across_dim, val = self.folds.pop(0)

        if across_dim == "x":
            new_grid = self.fold_horiz(val)
        if across_dim == "y":
            new_grid = self.fold_vert(val)
        self.grid = new_grid
        return new_grid

    def part_1(self):
        self.fold()
        return self.grid.sum()

    def display(self, matrix=None):
        if matrix is None:
            matrix = self.grid
        grid = np.where(matrix, "#", " ")

        for row in grid:
            print("".join(row))

        return

    def part_2(self):
        while self.folds:
            self.fold()

        self.display()

        return


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