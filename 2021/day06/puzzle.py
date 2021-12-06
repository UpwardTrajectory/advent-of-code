from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal
import numpy as np


@dataclass
class LanternFish:
    """
    """
    time_left: Literal[range(0, 9)]
    startup_time: int = field(default=2, repr=False)
    cycle_time: int = field(default=6, repr=False)
    n_hatchlings: int = 0

    def exist_one_day(self) -> None:
        self.time_left -= 1
        if self.time_left == -1:
            self.time_left = 6
        return 
    
    @property
    def rdy_to_spawn(self):
        return self.time_left == 0
    
    def spawn(self):
        self.n_hatchlings += 1
        return LanternFish(self.cycle_time + self.startup_time)
    
    
@dataclass
class School:
    fpath: str = None
    initial_state: list[int] = None
    school: list[int] = None
    prev_populations: dict[int: int] = field(default_factory=dict, repr=False)
    age: int = 0
    
    def __post_init__(self) -> None:
        if self.fpath is not None:
            raw = Path(self.fpath).open().read() 
            self.initial_state = [int(x) for x in raw.split(",")]  
        self.school = [LanternFish(x) for x in self.initial_state]
        self.prev_populations[0] = len(self.initial_state)
        return
        
    def exist_one_day(self):
        new_fishes = []
        for fish in self.school:     
            if fish.rdy_to_spawn:
                new_fishes.append(fish.spawn())
            fish.exist_one_day()             
        self.school.extend(new_fishes)
        self.age += 1
        self.prev_populations[self.age] = len(self.school)
        return 
    
    def exist_n_days(self, n):
        """TO-DO: 
        Find a closed-form solution :)
        -OR- 
        Cache the values for each amount of days left, so we
        don't keep recalculating the same math over & over
        """
        todo = Counter(self.initial_state)
        
        for _ in range(n):
            self.exist_one_day()
        return len(self.school)
    
    
test_school = School('tests.txt') 
t1 = test_school.exist_n_days(80)
assert t1 == 5934, f"Test 1 failed. Got {t1} instead of 5934"

# t2 = test_school.exist_n_days(256 - 80)
# assert t2 == 26984457539, f"Test 2 failed. Got {t2:,} instead of 26,984,457,539"

print("All tests passed.")


if __name__ == "__main__":
    school = School('inputs.txt') 
    p1 = school.exist_n_days(80)
    print("Part 1:", p1)

#     school = School('inputs.txt') 
#     p2 = school.exist_n_days(256-80)
#     print("Part 2:", p2)
