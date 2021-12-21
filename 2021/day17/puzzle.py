from pathlib import Path
from typing import Literal
from dataclasses import dataclass, field
import numpy as np


T1_ANS = 45  # gets to max_height with initial = (6, 9)
T2_ANS = 112


@dataclass
class Projectile:
    v_x: int
    v_y: int
    x: int = 0
    y: int = 0
    n_stops: int = 0
    stops: list[tuple[int, int]] = field(default_factory=list, repr=False)

    def __post_init__(self):
        self.stops.append((self.x, self.y))
        return

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

        if self.v_x < 0:
            self.v_x += 1
        if self.v_x > 0:
            self.v_x -= 1

        self.v_y -= 1

        self.stops.append((self.x, self.y))

        return

    def max_height(self) -> int:
        trajectory = np.array(self.stops)
        return trajectory[:, 1].max()

    def in_the_zone(self, xmin: int, xmax: int, ymin: int, ymax: int) -> bool:
        """CAUTION: this only works after traveling a certain number of stops
        This logic is contained in the "while ..." loop of Puzzle.projectile_in_zone()

        According to that logic, self.stops will always end at the first point OUTSIDE
        the box. So we investigate the 2nd-to-last stop to see if it's still inside the box.
        """
        x, y = self.stops[-2]
        if (xmin <= x <= xmax) and (ymin <= y <= ymax):
            return True
        return False


@dataclass
class Puzzle:
    fname: str
    traveled: dict[tuple[int, int] : Projectile] = field(
        default_factory=dict, repr=False
    )

    def __post_init__(self):
        raw = Path(self.fname).open().read()  # or read() for a big block of text
        xs, ys = [s[2:].split("..") for s in raw[13:].split(", ")]
        self.xmin = int(xs[0])
        self.xmax = int(xs[1])
        self.ymin = int(ys[0])
        self.ymax = int(ys[1])

        return

    def projectile_in_zone(self, v_x: int, v_y: int) -> bool:
        p = Projectile(v_x, v_y)

        while (p.x <= self.xmax) and (p.y >= self.ymin):
            p.move()

        if p.in_the_zone(self.xmin, self.xmax, self.ymin, self.ymax):
            self.traveled[(v_x, v_y)] = p.max_height()

        return

    @property
    def min_vx(self) -> int:
        """From solving summation of decreasing numbers with quadratic formula:
        (v_x * (v_x + 1) / 2) >= xmin
        """
        return int(1 + (-1 + np.sqrt(1 + 8 * self.xmin)) // 2)

    @property
    def max_vx(self) -> int:
        """Can't hit if we overshoot on the very first stop"""
        return self.xmax + 1

    @property
    def min_vy(self) -> int:
        """Lower than this will always undershoot the lower left corner"""
        return self.ymin - self.min_vx

    @property
    def max_vy(self) -> int:
        """Somewhat arbitrary scaling of min_vx, but I'm pretty sure there's
        a closed-form maximum that relies on min_vx, and I'm pretty sure
        this bound > the true mathematical bound.
        """
        return 10 * self.min_vx

    def part_1(self) -> int:
        for x in range(self.min_vx, self.max_vx + 1):
            for y in range(self.min_vy, self.max_vy + 1):
                self.projectile_in_zone(x, y)

        return max(self.traveled.values())

    def part_2(self):
        """This assumes self.part_1() has already been calculated so that
        self.traveled is populated
        """
        return len(self.traveled)


def run_tests(p1_ans=T1_ANS, p2_ans=T2_ANS, fname="tests.txt"):
    puz = Puzzle(fname)
    t1 = puz.part_1()
    assert t1 == p1_ans, f"Test 1 failed. Got {t1} instead of {p1_ans}"
    status_update = "Test #1 passed, did not try Part 2"

    if p2_ans is not None:
        t2 = puz.part_2()
        assert t2 == p2_ans, f"Test 2 failed. Got {t2} instead of {p2_ans}"
        status_update = "Tested both Parts 1 & 2. All tests passed."

    print(status_update)
    return


if __name__ == "__main__":
    run_tests()

    puz = Puzzle("inputs.txt")

    p1 = puz.part_1()
    print("Part 1:", p1)

    if T2_ANS is not None:
        p2 = puz.part_2()
        print("Part 2:", p2)