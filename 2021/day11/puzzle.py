from pathlib import Path
from dataclasses import dataclass, field
from statistics import median


T1_ANS = 1656
T2_ANS = 195


@dataclass
class Octopus:
    row: int
    col: int
    nrg_level: int
    has_fired: bool = field(default=False, repr=False)
    neighbors: list = field(default_factory=list, repr=False)
    total_flashes: int = 0

    def get_neighbor_coords(self):
        row = self.row
        col = self.col
        neighbor_coords = [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1),                     (row, col + 1),
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
        ]
        neighbor_coords = [
            (r, c) for r, c in neighbor_coords if 0 <= r <= 9 and 0 <= c <= 9
        ]
        return neighbor_coords

    def set_neighbors(self, octopi):
        neighbor_coords = self.get_neighbor_coords()
        self.neighbors = [x for x in octopi if (x.row, x.col) in neighbor_coords]
        return

    def increase_nrg(self):
        self.nrg_level += 1
        return

    def light_up(self):
        if self.nrg_level > 9 and not self.has_fired:
            self.has_fired = True
            self.total_flashes += 1

            for neighbor in self.neighbors:
                self.propogate(neighbor)

        return

    def propogate(self, other):
        other.nrg_level += 1
        if other.nrg_level > 9 and not other.has_fired:
            other.light_up()

    def reset_nrg(self):
        if self.has_fired is True:
            self.nrg_level = 0
            self.has_fired = False
        return


@dataclass
class Puzzle:
    fname: str
    octopi: list[Octopus] = field(default_factory=list, repr=False)
    n: int = 0
    after_100: int = None
    first_sync: int = None

    def __post_init__(self):
        raw = Path(self.fname).open().readlines()
        levels = [[int(x) for x in line.strip()] for line in raw]

        octopi = []
        for row_num, row in enumerate(levels):
            for col_num, lvl in enumerate(row):
                octopi.append(Octopus(row_num, col_num, lvl))

        for octopus in octopi:
            octopus.set_neighbors(octopi)
            
        self.octopi = octopi
        return

    def single_round(self, part_2=False):

        for octps in self.octopi:
            octps.increase_nrg()

        for octps in self.octopi:
            octps.light_up()

        if self.n == 99:
            self.after_100 = sum([octps.total_flashes for octps in self.octopi])

        if part_2:
            total_diff_nrg = len(set(x.nrg_level for x in self.octopi))
            if total_diff_nrg == 1:
                self.first_sync = self.n

        for octps in self.octopi:
            octps.reset_nrg()
        self.n += 1
        return

    def part_1(self):
        """Added part_2=True to make sure we check whether the first_sync
        occurs inside the first 100 iterations (this is unlikely)
        """
        for _ in range(100):
            self.single_round(part_2=True)

        return self.after_100

    def part_2(self):
        while self.first_sync is None:
            self.single_round(part_2=True)
            
            # paranoid safeguard to prevent infinite loop
            if self.n > 1000:
                print("This is going too long.")
                break

        return self.first_sync


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