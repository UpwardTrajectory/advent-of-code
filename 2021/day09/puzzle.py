from pathlib import Path
from dataclasses import dataclass, field
import numpy as np
from scipy.ndimage import measurements


T1_ANS = 15
T2_ANS = 1134


@dataclass
class Point:
    row: int
    col: int
    grid: np.array = field(repr=False)

    @property
    def value(self):
        return self.grid[self.row, self.col]

    @property
    def lt_up(self):
        if self.row != 0:
            return self.value < self.grid[self.row - 1, self.col]
        return True

    @property
    def lt_down(self):
        if self.row != (len(self.grid) - 1):
            return self.value < self.grid[self.row + 1, self.col]
        return True

    @property
    def lt_left(self):
        if self.col != 0:
            return self.value < self.grid[self.row, self.col - 1]
        return True

    @property
    def lt_right(self):
        if self.col != (len(self.grid[0]) - 1):
            return self.value < self.grid[self.row, self.col + 1]
        return True

    def is_lowest(self):
        return all([self.lt_up, self.lt_down, self.lt_left, self.lt_right])


@dataclass
class Puzzle:
    fname: str
    grid: np.array = None

    def __post_init__(self):
        raw = Path(self.fname).open().readlines()
        self.grid = np.array([list(row.strip()) for row in raw]).astype(int)

    def find_low_pts(self):
        low_pts = []

        for rownum, row in enumerate(self.grid):
            for colnum, val in enumerate(row):
                pt = Point(rownum, colnum, self.grid)
                if pt.is_lowest():
                    low_pts.append(pt)

        return low_pts

    def part_1(self):
        low_pts = self.find_low_pts()
        return sum([pt.value + 1 for pt in low_pts])

    @property
    def basins(self):
        return np.where(self.grid == 9, 0, 1)

    def basin_areas(self):
        """Credit where credit is due:
        https://stackoverflow.com/a/25666134/14083170
        """
        lw, num = measurements.label(self.basins)
        areas = measurements.sum(self.basins, lw, index=np.arange(lw.max() + 1))
        return areas.astype(int)

    def part_2(self):
        areas = self.basin_areas()
        top_3 = sorted(areas)[-3:]
        return np.product(top_3)


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