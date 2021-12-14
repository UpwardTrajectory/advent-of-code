"""I ... caved ... and looked at an answer:

final working solution inspired by:
https://github.com/joelgrus/advent2021/blob/master/day12.py
"""

from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field


T1_ANS = 10
T2_ANS = 36


@dataclass
class Puzzle:
    fname: str
    caves: dict[str:list] = field(default_factory=lambda: defaultdict(list), repr=False)
    all_path_routes: set[str] = field(default_factory=set, repr=False)

    def __post_init__(self):
        raw = Path(self.fname).open().readlines()
        for conn in raw:
            a, b = conn.strip().split("-")
            self.caves[a].append(b)
            self.caves[b].append(a)
        return

    @property
    def num_paths(self):
        return len(self.all_path_routes)

    def find_valid_paths(self):

        unexplored = [["start"]]

        while unexplored:
            cur_path = unexplored.pop()
            cave = cur_path[-1]

            if cave == "end":
                self.all_path_routes.add(",".join(cur_path))
            else:
                for next_cave in self.caves[cave]:
                    if next_cave not in cur_path or next_cave.isupper():
                        unexplored.append(cur_path + [next_cave])
        return

    def find_double_small_paths(self):
        small_caves = {
            cave
            for cave in self.caves
            if cave.islower() and cave not in ("start", "end")
        }
        unexplored = [["start"]]

        while unexplored:
            cur_path = unexplored.pop()
            cave = cur_path[-1]

            if cave == "end":
                self.all_path_routes.add(",".join(cur_path))
            else:
                double_smalls = set(
                    cave for cave in small_caves if cur_path.count(cave) > 1
                )
                for next_cave in self.caves[cave]:
                    should_explore = (
                        (next_cave not in cur_path)
                        or next_cave.isupper()
                        or (not double_smalls and next_cave != "start")
                    )
                    if should_explore:
                        unexplored.append(cur_path + [next_cave])
        return

    def part_1(self):
        self.find_valid_paths()
        return self.num_paths

    def part_2(self):
        self.find_double_small_paths()
        return self.num_paths


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
    run_tests(19, 103, fname="tests2.txt")
    run_tests(226, 3509, fname="tests3.txt")

    puz = Puzzle("inputs.txt")

    p1 = puz.part_1()
    print("Part 1:", p1)

    if T2_ANS is not None:
        p2 = puz.part_2()
        print("Part 2:", p2)