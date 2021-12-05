import time
from typing import List, Union
from XMAS_inputs import full_input


t = time.time()


def has_sum_to_target(sequence: List[int], target: int) -> bool:
    ordered = sorted(sequence)
    front, back = 0, len(ordered) - 1

    while front < back:
        if (ordered[front] + ordered[back] == target) and (
            ordered[front] != ordered[back]
        ):
            return True
        elif ordered[front] + ordered[back] < target:
            front += 1
        else:
            back -= 1
    return False


# assert has_sum_to_target([35, 20, 15, 25, 47], 40) == True
# assert has_sum_to_target([95, 102, 117, 150, 182], 127) == False


def is_invalid_preamble(sequence: List[int], preamble_length: int) -> int:
    for i, seq in enumerate(sequence):
        if not has_sum_to_target(
            sequence[i : preamble_length + i], sequence[preamble_length + i]
        ):
            return sequence[preamble_length + i], preamble_length + i


# assert is_invalid_preamble(
#         [
#             35,
#             20,
#             15,
#             25,
#             47,
#             40,
#             62,
#             55,
#             65,
#             95,
#             102,
#             117,
#             150,
#             182,
#             127,
#             219,
#             299,
#             277,
#             309,
#             576,
#         ],
#         5,
#     ) == (127, 14)


# with open('../inputs/day09.txt') as f:
#     XMAS = [int(line.strip()) for line in f.readlines()]
XMAS = [int(x) for x in full_input.split("\n")]
part_1 = is_invalid_preamble(XMAS, 25)[0]


# part 2, find two numbers in contiguous set which equal the invalid preamble
# return the sum of the min and max


def sum_max_min(sequence: List[int], target: int) -> int:
    for i in range(len(sequence)):
        for j in range(2, len(sequence) + 1):
            if sum(sequence[i:j]) == target:
                return sum([min(sequence[i:j]), max(sequence[i:j])])


def sum_max_min(data, target):

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


pred = sum_max_min(XMAS, part_1)

print(time.time() - t)
print(part_1)  # 14144619
print(pred)
