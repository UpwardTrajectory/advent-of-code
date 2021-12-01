"""Very much NOT optimized, but after chugging along for 20+ mins, it works"""

from typing import NamedTuple
from dataclasses import dataclass
from itertools import product
import numpy as np


SAMPLE = """.#.
..#
###"""

CUBEMAP = """...###.#
#.#.##..
.##.##..
..##...#
.###.##.
.#..##..
.....###
.####..#"""

@dataclass
class Cube(dict):
    x: int
    y: int
    z: int
    w: int
    state: bool
    search_space: tuple 
    
    @staticmethod
    def create(x0: int, y0: int, z0: int, w0: int, start_state: bool):
        search_space = [-1, 0, 1]
        search_space = tuple((x, y, z, w) for x in search_space 
                                          for y in search_space 
                                          for z in search_space 
                                          for w in search_space
                            if (x, y, z, w) != (0, 0, 0, 0)
                            )
        return Cube(x0, y0, z0, w0, start_state, search_space)
    
    def __repr__(self):
        return f"{self.state} Cube({self.x}, {self.y}, {self.z}, {self.w})"
    
    @property
    def show(self):
        if self.state is True:
            return "#"
        else:
            return "."
    
    def true_neighbors(self, fullmap: np.array):
        """Count the number of activated cubes within the neighboring 3D zone"""
        neighbor_states = []
        
        for vec in self.search_space:
            cur = {"x": self.x + vec[0],
                   "y": self.y + vec[1],
                   "z": self.z + vec[2],
                   "w": self.w + vec[3]}
            
            interior_x = (0 <= cur["x"] < fullmap.shape[0])
            interior_y = (0 <= cur["y"] < fullmap.shape[1])
            interior_z = (0 <= cur["z"] < fullmap.shape[2])
            interior_w = (0 <= cur["w"] < fullmap.shape[3])
            
            if all([interior_x, interior_y, interior_z, interior_w]):
                vec_state = fullmap[cur["x"], cur["y"], cur["z"], cur["w"]].state
                neighbor_states.append(vec_state)
        return sum(neighbor_states)
    
    def turn_on(self):
        self.state = True
        return self
    
    
@dataclass
class CubeMap(dict):
    grid: np.array
    full_dim: int 
    
    @staticmethod
    def read_map(raw_data: str, turns=7):
        """Instantiate a map from a string with a 2D layer 
        that sits half-way through the Z-coordinate space
        """
        data = [[True if x == "#" else False for x in row]
                                             for row in raw_data.split("\n")]
        data = [[Cube.create(x + turns, y + turns, turns, turns, val) 
                 for y, val in enumerate(row)] 
                for x, row in enumerate(data)]
        width = len(data[0])
        height = len(data)
        max_size = 2*turns + max(width, height)
        full_grid = product(range(max_size), range(max_size), range(max_size), range(max_size))
        canvas = np.array([Cube.create(x, y, z, w, False) for x, y, z, w in full_grid]
                         ).reshape(max_size, max_size, max_size, max_size)        
        canvas[turns: turns+width, turns: turns+height, turns, turns] = data
        return CubeMap(grid=canvas, full_dim=max_size)
        
    def __repr__(self):
        return f"CubeMap{self.grid.shape}"
    
    @property
    def blank_canvas(self):
        dim = self.full_dim
        full_grid = product(range(dim), range(dim), range(dim), range(dim))
        canvas = np.array([Cube.create(x, y, z, w, False) for x, y, z, w in full_grid]
                         ).reshape(dim, dim, dim, dim)
        return canvas
    
    @property
    def all_states(self):
        return np.vectorize(lambda x: x.state)(self.grid)
    
    @property
    def neighbor_states(self):
        return np.vectorize(lambda x: x.true_neighbors(self.grid))(self.grid)
    
    @property
    def count(self):
        return np.sum(self.all_states)

    def cycle_once(self):
        """Simultaneously follow these 3 rules for every cube in the grid:
        1) if ON & (2 or 3 ON neighbors): stay ON
        2) if OFF & (exactly 3 ON neighbhors): turn ON
        3) otherwise turn/stay OFF
        """
        grid = self.grid
        
        two_or_three = np.logical_or(self.neighbor_states == 2, self.neighbor_states == 3)
        stay_on = np.logical_and(self.all_states == True, two_or_three)
        
        turn_on = np.logical_and(self.all_states == False, self.neighbor_states == 3)
        
        new_grid = self.blank_canvas.copy()
        if stay_on.any():
            new_grid[stay_on] = np.vectorize(lambda x: x.turn_on())(grid[stay_on])
        if turn_on.any():
            new_grid[turn_on] = np.vectorize(lambda x: x.turn_on())(grid[turn_on])
        self.grid = new_grid
        #print(f"Total Activated: {self.count}")
        return self
    
    def cycle_many(self, k):
        for i in range(k):
            self.cycle_once()
            print(f"After {i+1}: {self.count} )
        return self.count
 
    
if __name__ == "__main__":
    galaxy = CubeMap.read_map(CUBEMAP)
    print(galaxy.cycle_many(6))
        