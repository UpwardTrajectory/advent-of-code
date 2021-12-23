from pathlib import Path
from typing import Literal
from dataclasses import dataclass, field
import numpy as np
import matplotlib.pyplot as plt


T1_ANS = 79
T2_ANS = None

OVERLAP_REQD = 12   # 6 for same_scanner.txt but 12 for normal problem

@dataclass
class Scanner:
    raw: list[str]
    ID: int = None    
    beacons: np.array = None
    coords: np.array = None 
    centroid: np.array = None
    
    def __post_init__(self):
        self.ID = int(self.raw[0].split(" ")[2])
        beacons = [x.split(",") for x in self.raw[1:]]
        self.beacons = np.array(beacons, dtype=int)
        # self.original_state = self.beacons.copy()
        return
        
    def __repr__(self):
        return f"Scanner(ID={self.ID})"
    
    def __eq__(self, other):
        overlap = len(set(self.hashable) & set(other.hashable))
        if overlap > 0:
            print(f"{self.ID} & {other.ID}: {overlap}")
        return overlap >= OVERLAP_REQD
    
    @property
    def hashable(self):
        return tuple(map(tuple, self.beacons))
    
    # def flip(self, dim: str) -> np.array:
    #     dim_to_idx = {"x": 0, "y": 1, "z": 2}
    #     idx = dim_to_idx[dim]
    #     # beacons = self.beacons.copy()
    #     self.beacons[:, idx] = -self.beacons[:, idx]
    #     return self
    
    def rot90(self, dim: str, n=1) -> np.array: 
        # fmt: off
        dim_to_matrix = {
            "x": np.array([[1,  0,  0], 
                           [0,  0, -1],
                           [0,  1,  0]]), 
            
            "y": np.array([[0,  0,  1], 
                           [0,  1,  0],
                           [-1, 0,  0]]), 
            
            "z": np.array([[0, -1,  0], 
                           [1,  0,  0],
                           [0,  0,  1]])
        }
        # fmt: on
        rot_mtrx = np.linalg.matrix_power(dim_to_matrix[dim], n)
        self.beacons = np.matmul(self.beacons, rot_mtrx)
        return self
    
    # def shift(self, dim: str, amt: int):
    #     dim_to_idx = {"x": 0, "y": 1, "z": 2}
    #     idx = dim_to_idx[dim]
    #     self.beacons[:, idx] = self.beacons[:, idx] + amt
    #     return self
    
    def to_origin(self):
        if self.centroid is None:
            self.centroid = np.mean(self.beacons, axis=0).astype(int)
            self.beacons -= self.centroid       
        return self
    
    def orient_to(self, other):
        """"""
        self.to_origin()
        
        if self == other:
            self.coords = other.coords + self.centroid
            return self       
        
        face_up = (
            lambda s: s,
            lambda s: s.rot90("y"),
            lambda s: s.rot90("y"),
            lambda s: s.rot90("y"),
            lambda s: s.rot90("y").rot90("x"),
            lambda s: s.rot90("x").rot90("x")
        )

        for orient in face_up:
            orient(self)
            for spin in [1, 2, 3, 4]:
                self.rot90("z")
                if self == other:
                    self.coords = other.coords + self.centroid
                    return self
        
        self.rot90("x")
        return False


@dataclass
class Puzzle:
    fname: str
    scanners: dict[int: Scanner] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        raw = Path(self.fname).open().read()  # or read() for a big block of text
        scanners = [r.strip().split("\n") for r in raw.split("\n\n")]
        
        for raw_scnr in scanners:
            scnr = Scanner(raw_scnr)
            self.scanners[scnr.ID] = scnr
            
        self.scanners[0].to_origin()
        self.scanners[0].coords = np.array([0, 0, 0])
        
        return

    def part_1(self):
        pass

    def part_2(self):
        pass
    
    
def plot(arr):
    """Primarily built to validate the flip() & rot90() functions using the
    single_box.txt file
    """
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    colors = ("gkbycyrmc" * (len(arr) // 9 + 1))[: len(arr)]

    ax.scatter3D(arr[:, 0], arr[:, 1], arr[:, 2], c=list(colors))

    ax.axes.set_xlim3d(left=-8, right=8)
    ax.axes.set_ylim3d(bottom=-8, top=8)
    ax.axes.set_zlim3d(bottom=-8, top=8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ticks = range(-8, 12, 8)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_zticks(ticks)
    plt.tight_layout()
    return plt


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