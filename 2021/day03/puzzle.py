import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter
from typing import Literal, Iterable


def get_bits(fname: str) -> np.array:
    df = pd.read_csv(fname, names=["raw"], dtype=str)
    return np.array([list(b) for b in df["raw"]]).astype(int)


def gamma(bits: np.array) -> str:
    gamma = stats.mode(bits)[0][0]
    return "".join(gamma.astype(str))


def epsilon(gamma: str) -> str:
    """Silly way of getting the bit-compliment of gamma b/c I couldn't get 
    ~gamma to work after trying a bunch of different datatypes
    
    NOTE: replace is faster than "".join():  https://stackoverflow.com/a/23303239/14083170
    """
    #     return "".join("1" if b == "0" else "0" for b in gamma)
    return gamma.replace("1", "2").replace("0", "1").replace("2", "0")


def power_consumption(bits: np.array) -> int:
    gam = gamma(bits)
    eps = epsilon(gam)
    return int(gam, base=2) * int(eps, base=2)


def bitmode(arr: Iterable, least_common: bool = False) -> Literal[0, 1]:
    """Custom binary "mode" for individual bits: 
    if there's a tie, always chose 1 instead of 0
    least_common simply gives the opposite
    """
    consider = Counter(arr)
    if consider[0] > consider[1]:
        return int(least_common)
    return int(not least_common)


def get_elem_rating(bits: np.array, least_common: bool, column: int = 0) -> int:
    """least_common gets passed directly into bitmode()
    Oxygen: least_common = False
       CO2: least_common = True
    """
    if len(bits) == 1:
        return int("".join(bits[0].astype(str)), 2)
    col_mask = bits[:, column]
    return get_elem_rating(
        bits[col_mask == bitmode(col_mask, least_common=least_common)],
        least_common,
        column + 1,
    )


def life_support_rating(bits: np.array):
    oxygen = get_elem_rating(bits, least_common=False)
    co2 = get_elem_rating(bits, least_common=True)
    return oxygen * co2


test_bits = get_bits("test.txt")
tests = ((power_consumption(test_bits), 198), (life_support_rating(test_bits), 230))

for test_num, test_case in enumerate(tests):
    pred, actual = test_case
    assert pred == actual, f"test #{test_num+1} failed. got {pred} instead of {actual}"

print("All tests passed.")


if __name__ == "__main__":
    bits = get_bits("inputs.txt")
    p1 = power_consumption(bits)
    print("Part 1:", p1)
    p2 = life_support_rating(bits)
    print("Part 2:", p2)
