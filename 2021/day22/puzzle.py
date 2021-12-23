from pathlib import Path
from typing import Literal
import numpy as np
from dataclasses import dataclass, field



T1_ANS = 590784
T2_ANS = 2758514936282235


@dataclass
class Cube:
    raw: str
    xmin: int = None
    xmax: int = None
    ymin: int = None
    ymax: int = None
    zmin: int = None
    zmax: int = None
    toggle: bool = None
    overlaps_p1: bool = None

    def __post_init__(self):
        row = self.raw
        toggle, other = row.split(" ")
        xs, ys, zs = other.split(",")
        cube = []
        for bounds in [xs, ys, zs]:
            low, hi = bounds.split("..")
            low = int(low[2:])
            hi = int(hi) + 1
            cube += [low, hi]

        toggle = True if (toggle == "on") else False

        self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax = cube
        self.toggle = toggle
        self.set_overlaps_p1()
        return

    def __repr__(self) -> str:
        tgl = "ON, " if self.toggle else "OFF, " 
        xs = f"x=[{self.xmin}: {self.xmax}), "
        ys = f"y=[{self.ymin}: {self.ymax}), "
        zs = f"z=[{self.zmin}: {self.zmax}))"
        return "".join(["Cube(", tgl, xs, ys, zs])
    
    def force_positive(self, global_mins: dict[Literal['x', 'y', 'z']: int], part_1=True):
        if part_1:
            self.xmin += 50
            self.xmax += 50
            self.ymin += 50
            self.ymax += 50
            self.zmin += 50
            self.zmax += 50
        else:
            self.xmin += global_mins['x']
            self.xmax += global_mins['x']
            self.ymin += global_mins['y']
            self.ymax += global_mins['y']
            self.zmin += global_mins['z']
            self.zmax += global_mins['z']
        return self
    
    def set_overlaps_p1(self):
        outside_x = (self.xmin > 50) or (self.xmax < -50)
        outside_y = (self.ymin > 50) or (self.ymax < -50)
        outside_z = (self.zmin > 50) or (self.zmax < -50)
        
        self.overlaps_p1 = not any([outside_x, outside_y, outside_z])
        return
    

@dataclass
class Puzzle:
    fname: str
    galaxy: np.array = field(default=None, repr=False)
    global_mins: dict[Literal['x', 'y', 'z']: int] = field(default_factory=dict, repr=False)
    instructions: list[Cube] = field(default_factory=list, repr=False)
    
    def __post_init__(self):
        raw = Path(self.fname).open().readlines()  # or read() for a big block of text
        self.instructions = [Cube(row) for row in raw]
        
        xmin = min([c.xmin for c in self.instructions if c.overlaps_p1])
        xmax = max([c.xmax for c in self.instructions if c.overlaps_p1])
        ymin = min([c.ymin for c in self.instructions if c.overlaps_p1])
        ymax = max([c.ymax for c in self.instructions if c.overlaps_p1])
        zmin = min([c.zmin for c in self.instructions if c.overlaps_p1])
        zmax = max([c.zmax for c in self.instructions if c.overlaps_p1])
        
        self.global_mins = {'x': xmin, 'y': ymin, 'z': zmin}
        
        for box in self.instructions:
            box.force_positive(self.global_mins)
        
        # self.galaxy = np.zeros((xmax - xmin, ymax - ymin, zmax - zmin), dtype=np.bool_)
        return

    def part_1(self):
        self.galaxy = np.zeros((101, 101, 101), dtype=np.bool_)
        for box in self.instructions:
            if box.overlaps_p1: 
                print(box)
                self.galaxy[
                    box.xmin : box.xmax, box.ymin : box.ymax, box.zmin : box.zmax
                ] = box.toggle

        return self.galaxy.sum()
            

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