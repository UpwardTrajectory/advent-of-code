from dataclasses import dataclass, field
from collections import Counter
import pandas as pd
import numpy as np


@dataclass
class Line:
    """Lines should always move to the right (or vertical)
    AKA x1 <= x2
    """
    x1: int
    y1: int
    x2: int
    y2: int
    points_touched: set(tuple((int, int))) = field(default_factory=set, repr=False)
            
    def __hash__(self):
        return hash(repr(self))
        
    def fill(self, enable_diag):
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        if x1 == x2:
            y_start = min(y1, y2)
            y_stop = max(y1, y2) + 1
            for y in range(y_start, y_stop):
                self.points_touched.add((x1, y))
        elif y1 == y2:
            for x in range(x1, x2+1):
                self.points_touched.add((x, y1))
        if enable_diag is True:
            if (x1 < x2) and (y1 != y2):
                x_start = x1
                x_stop = x2 + 1
                xs = range(x_start, x_stop)
                if y1 < y2:  # Down-right
                    y_start = y1
                    y_stop = y2 + 1
                    ys = range(y_start, y_stop)

                else:  # up-right
                    y_start = y2
                    y_stop = y1 + 1
                    ys = list(range(y_start, y_stop))[::-1]
                for x, y in zip(xs, ys):
                    self.points_touched.add((x, y))
                
        return
        

@dataclass
class VentFinder:
    fname : str
    lines: set([Line]) = None
    danger_map: 'Counter[(x, y): num_vents]' = field(default=None, repr=False)
    
    def __post_init__(self):
        self.danger_map = Counter()
        
        all_lines = set()

        with open(self.fname, 'r') as f:
            for line in f.readlines():
                p1, p2 = line.strip().split(" -> ")
                x1, y1 = [int(n) for n in p1.split(",")]
                x2, y2 = [int(n) for n in p2.split(",")]


                if x1 <= x2:
                    all_lines.add(Line(x1, y1, x2, y2))           
                else:
                    all_lines.add(Line(x2, y2, x1, y1))
                    
        self.lines = all_lines
        return
    
    def mark(self, line, enable_diag):
        line.fill(enable_diag)
        for pt in line.points_touched:
            self.danger_map[pt] += 1
        return
    
    def map_floor(self, enable_diag):
        for line in self.lines:
            self.mark(line, enable_diag)
        return
    
    def count_dangerous(self, thresh=2, enable_diag=False):
        self.map_floor(enable_diag)
        return len([pt for pt in self.danger_map if self.danger_map[pt] >= thresh])
    
    def show_vents(self):
        xmax = max(l.x2 for l in self.lines)
        ymax = max(max(l.y1, l.y2) for l in self.lines)
        grid = np.zeros((xmax+1, ymax+1))
        
        for pt in self.danger_map:
            grid[pt] = self.danger_map[pt]
        
        grid = grid.astype(int).astype(str)
        grid = np.char.replace(grid, "0", ".").T
        print(grid)
        return 
                
           
vents = VentFinder('tests.txt')
t1 = vents.count_dangerous()
assert t1 == 5, f"Test 1 failed. Got {t1} instead of 5"

vents.danger_map.clear()
t2 = vents.count_dangerous(enable_diag=True)
print(vents.show_vents())
assert t2 == 12, f"Test 2 failed. Got {t2} instead of 12"


if __name__ == "__main__":
    vents = VentFinder('inputs.txt')
    p1 = vents.count_dangerous()
    print("Part 1:", p1)
    
    vents.danger_map.clear()
    p2 = vents.count_dangerous(enable_diag=True)
    print("Part 2:", p2)