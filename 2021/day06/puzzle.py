from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal
import numpy as np


def work_backwards(n):
    # {days_till_end: total_fishes_made_by_one_fish}
    FUTURE_FISHES = {
        0: 1,
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 2,
    }
    if n in FUTURE_FISHES:
        return FUTURE_FISHES[n]


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
    school: list[int] = field(default=None, repr=False)
    age: int = 0
    future_fishes: dict[int:int] = field(
        default_factory=lambda: {
            0: 1,
            1: 2,
            2: 2,
            3: 2,
            4: 2,
            5: 2,
            6: 2,
            7: 2,
            8: 3,
            9: 3,
            10: 4,
            11: 4,
            12: 4,
            13: 4,
            14: 4,
            15: 5,
            16: 5,
            17: 7,
            18: 7,
        },
        repr=False,
    )

    def __post_init__(self) -> None:
        if self.fpath is not None:
            raw = Path(self.fpath).open().read()
            self.initial_state = [int(x) for x in raw.split(",")]
        self.school = [LanternFish(x) for x in self.initial_state]
        return

    def exist_one_day(self):
        new_fishes = []
        for fish in self.school:
            if fish.rdy_to_spawn:
                new_fishes.append(fish.spawn())
            fish.exist_one_day()
        self.school.extend(new_fishes)
        self.age += 1
        return

    def naive_exist_n_days(self, n):
        """TO-DO: 
        Find a closed-form solution :)
        -OR- 
        Cache the values for each amount of days left, so we
        don't keep recalculating the same math over & over
        """
        for _ in range(n):
            self.exist_one_day()
        return len(self.school)

    def exist_n_days(self, n):
        self.build_future_fishes(n)
        return sum([self.future_fishes[n - fish] for fish in self.initial_state])

    def build_future_fishes(self, n):
        start = max(self.future_fishes.keys()) + 1
        if start >= n:
            return self.future_fishes
        for day in range(start, n + 1):
            if day % 7 == 0:
                print("\n", "-" * 10, day)
                # extra_fishes = 0
                # other_spawn_days = [7*x for x in range(1, day // 7)]
                # for subsequent_spawn in other_spawn_days:
                #     print(f"{subsequent_spawn} adds: {self.future_fishes[subsequent_spawn]}")
                #     extra_fishes += self.future_fishes[subsequent_spawn]
                self.future_fishes[day] = (
                    self.spawn(day) + self.future_fishes[day - 1] + 1
                )
                print("    Total:", self.future_fishes[day])
            elif day % 7 == 2:
                self.future_fishes[day] = self.future_fishes[day - 1] + 1
            else:
                self.future_fishes[day] = self.future_fishes[day - 1]
        return self.future_fishes

    def spawn(self, day):
        if day < 10:
            return self.future_fishes[day - 9]
        else:
            return self.future_fishes[day - 9] + self.spawn(day - 9)


NUM_DAYS = 18

test_school = School("tests.txt")
t1 = test_school.exist_n_days(NUM_DAYS)
print(t1)

t1b = test_school.exist_n_days(18)
assert t1b == 26, f"Test 1b failed. Got {t1b} instead of 26"

t1 = test_school.exist_n_days(80)
assert t1 == 5934, f"Test 1 failed. Got {t1} instead of 5934"

# t2 = test_school.exist_n_days(256 - 80)
# assert t2 == 26984457539, f"Test 2 failed. Got {t2:,} instead of 26,984,457,539"

print("All tests passed.")


# if __name__ == "__main__":
# school = School('inputs.txt')
# p1 = school.exist_n_days(80)
# print("Part 1:", p1)

#     school = School('inputs.txt')
#     p2 = school.exist_n_days(256-80)
#     print("Part 2:", p2)
