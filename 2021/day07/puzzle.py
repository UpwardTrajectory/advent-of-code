from pathlib import Path
from dataclasses import dataclass
import numpy as np
from scipy.optimize import minimize_scalar


@dataclass
class CrabFuelOptimizer:
    fpath: str
    crabs: np.array(int) = None

    def __post_init__(self) -> None:
        crabs = Path(self.fpath).read_text().split(",")
        self.crabs = np.array([int(x) for x in crabs])
        return

    def part_1(self) -> int:
        distances = np.abs(self.crabs - np.median(self.crabs))
        return distances.sum().astype(int)

    def increased_fuel_consumption(self, test_distance: int) -> int:
        test_distance = int(round(test_distance))
        distances = np.abs(self.crabs - test_distance)
        fuel_used = distances * (distances + 1) / 2
        return fuel_used.sum().astype(int)

    def part_2(self) -> int:
        best_pos = (
            minimize_scalar(self.increased_fuel_consumption).x.round().astype(int)
        )
        return self.increased_fuel_consumption(best_pos)


crabs = CrabFuelOptimizer("tests.txt")

t1 = crabs.part_1()
assert t1 == 37, f"Test 1 failed. Got {t1} instead of 37"

t2 = crabs.part_2()
assert t2 == 168, f"Test 2 failed. Got {t2} instead of 168"

print("All tests passed.")


if __name__ == "__main__":
    crabs = CrabFuelOptimizer("inputs.txt")

    p1 = crabs.part_1()
    print("Part 1:", p1)

    p2 = crabs.part_2()
    print("Part 2:", p2)
