from pathlib import Path
from dataclasses import dataclass
import numpy as np
from scipy.optimize import minimize_scalar


def get_crabs(fpath: str) -> np.array:
    crabs = Path(fpath).read_text().split(",")
    return np.array([int(x) for x in crabs])


def calc_min_fuel(crabs: np.array) -> int:
    distances = np.abs(crabs - np.median(crabs))
    return distances.sum().astype(int)


def part_1(fpath: str) -> int:
    crabs = get_crabs(fpath)
    return calc_min_fuel(crabs)


@dataclass
class CrabFuelOptimizer:
    fpath: str
    crabs: np.array(int) = None

    def __post_init__(self):
        crabs = Path(self.fpath).read_text().split(",")
        self.crabs = np.array([int(x) for x in crabs])
        return

    def distances_to(self, new_pos: int) -> np.array(int):
        return np.abs(self.crabs - new_pos)

    def increased_fuel_consumption(self, test_distance: int) -> int:
        test_distance = int(round(test_distance))
        distances = self.distances_to(test_distance)
        fuel_used = (distances) * (distances + 1) / 2
        #         print([(k,round(v)) for k,v in zip(distances, fuel_used)])
        return fuel_used.sum().astype(int)

    def part_2(self) -> int:
        best_pos = (
            minimize_scalar(self.increased_fuel_consumption).x.round().astype(int)
        )
        return self.increased_fuel_consumption(best_pos)


t1 = part_1("tests.txt")
assert t1 == 37, f"Test 1 failed. Got {t1} instead of 37"

crabs = CrabFuelOptimizer("tests.txt")
t2 = crabs.part_2()
assert t2 == 168, f"Test 2 failed. Got {t2} instead of 168"

print("All tests passed.")


if __name__ == "__main__":
    p1 = part_1("inputs.txt")
    print("Part 1:", p1)

    crabs = CrabFuelOptimizer("inputs.txt")
    p2 = crabs.part_2()
    print("Part 2:", p2)
