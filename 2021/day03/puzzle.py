import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter


def get_bits(fname: str) -> int:    
    df = pd.read_csv(fname, names=['raw'], dtype=str)
    return np.array([list(b) for b in df['raw']]).astype(int)
    
    
def gamma(bits):
    gamma = stats.mode(bits)[0][0]
    return "".join(gamma.astype(str))


def epsilon(gamma):
    """Silly way of getting the compliment of gamma b/c I couldn't get 
    ~gamma to work after trying a bunch of different datatypes
    
    TODO: make it use binary operations instead of str operations
    """
    return "".join('1' if x == '0' else '0' for x in gamma)


def power_consumption(bits):
#     bits = get_bits(fname)
    gam = gamma(bits)
    eps = epsilon(gam)
    return int(gam, base=2) * int(eps, base=2)


def mode(arr, elem="O"):
    """Custom "mode": if there's a tie, always chose 1 instead of 0"""
    consider = Counter(arr)
    if consider[0] > consider[1]:
        return 0 if elem == "O" else 1
    return 1 if elem == "O" else 0
    
    
def get_elem_rating(bits, elem, level=0):
    """if elem is anything other than "O" (for Oxygen) it will find the least common"""
    if len(bits) == 1:
        return int("".join(str(x) for x in bits[0]), 2)
    col_mask = bits[:, level]
    return get_elem_rating(bits[col_mask == mode(col_mask, elem=elem)], elem, level + 1)
    
def life_support_rating(bits):
    oxygen = get_elem_rating(bits, "O")
    co2 = get_elem_rating(bits, "CO2")
    return oxygen * co2
   
    
test_bits = get_bits('test.txt')
tests = (
    (power_consumption(test_bits), 198),
    (life_support_rating(test_bits), 230)
)

for test_num, test_case in enumerate(tests):
    pred, actual = test_case
    assert pred == actual, f"test #{test_num} failed. got {pred} instead of {actual}"
    
print("All tests passed.")


if __name__ == "__main__":
    bits = get_bits("inputs.txt")
    p1 = power_consumption(bits)
    print("Part 1:", p1)
    p2 = life_support_rating(bits)
    print("Part 2:", p2)