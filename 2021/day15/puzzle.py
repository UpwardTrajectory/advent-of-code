from pathlib import Path
from dataclasses import dataclass, field
import numpy as np
from skimage.graph import route_through_array


T1_ANS = 40
T2_ANS = 315


@dataclass
class Puzzle:
    fname: str

    def __post_init__(self):
        raw = Path(self.fname).open().readlines()  # or read() for a big block of text
        maze = np.array([list(row.strip()) for row in raw], dtype=int)
        self.maze = maze
        return

    def expand_grid(self) -> np.array:
        """original grid is copied into a 5x5 mega grid.
        Each time copy horizontally or vertically adds one, but 9s wrap back to 1s

        These are the amounts added BEFORE wrapping:

        0 1 2 3 4
        1 2 3 4 5
        2 3 4 5 6
        3 4 5 6 7
        4 5 6 7 8
        """

        def grow(grid: np.array) -> np.array:
            return np.where(grid == 9, 1, grid + 1)

        pos_grids = {0: self.maze}

        for n in range(1, 9):
            pos_grids[n] = grow(pos_grids[n - 1])

        big_grid = []
        # Build horizontal rows of 5, then vstack them at the end
        for start in range(5):
            big_grid.append(np.hstack([pos_grids[i] for i in range(start, start + 5)]))

        return np.vstack(big_grid)

    def get_lowest_risk_route(self, maze: np.array = None) -> int:
        if maze is None:
            maze = self.maze
        end = [dim - 1 for dim in maze.shape]
        route, score = route_through_array(maze, (0, 0), end, fully_connected=False)
        route = np.stack(route, axis=-1)
        return maze[route[0, 1:], route[1, 1:]].sum()

    def part_1(self) -> int:
        return self.get_lowest_risk_route()

    def part_2(self) -> int:
        big_maze = self.expand_grid()
        return self.get_lowest_risk_route(big_maze)


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