import time

t = time.time()

from itertools import combinations
from numpy import cumsum  # needed for my solution, but not for J.Carson's
from XMAS_inputs import sample, full_input


def parse_raw(blob):
    return [int(x) for x in blob.split("\n")]


def test_one_weakness(i, data, window):
    possible = data[i - window : i]
    for a, b in combinations(possible, 2):
        if a + b == data[i]:
            return True
    return False


def find_weakness(data, window):
    for i in range(window, len(data)):
        if not test_one_weakness(i, data, window):
            return data[i]
    return None


def find_rolling_sum(data, target):
    all_sums = list(cumsum(data))
    poss_sum_pairs = combinations(all_sums, 2)
    for a, b in poss_sum_pairs:
        if b - a == target:
            min_idx = all_sums.index(a) + 1
            max_idx = all_sums.index(b) + 1
            window = data[min_idx:max_idx]
            return min(window) + max(window)
    return None


def find_rolling_sum2(data, target):
    """Not my work. Taken from J.Carson on PuPPy for timing & learning purposes"""
    start = stop = 0
    total = data[0]

    while True:
        while total < target:
            stop += 1
            total += data[stop]

        while total > target:
            # if we've overshot, remove entries from beginning of range
            total -= data[start]
            start += 1

        if total == target:
            if start == stop:
                # length of returned range must be > 1
                # if we've got a range of length 1, start over one entry further down
                start += 1
                stop = start
                total = data[start]
            else:
                break
    window = data[start : stop + 1]

    return min(window) + max(window)


data = parse_raw(sample)
pred = find_weakness(data, 5)
assert pred == 127
assert find_rolling_sum(data, pred) == 62


if __name__ == "__main__":
    t2 = time.time()

    data = parse_raw(full_input)
    pred = find_weakness(data, 25)
    part_2 = find_rolling_sum2(data, pred)

    n = time.time()
    print(f"({n - t}, {n - t2}), ")
    print(pred)
    print(part_2)
