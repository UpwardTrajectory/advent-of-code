from typing import List
import re
from bootloader import sample, bootcode


def parse_codes(raw_data: str):
    """Return a dictionary of {mask: [nums, to, which, mask, is, applied]}
    Every thing is a string.
    """
    data = [r.split(" = ") for r in raw_data.split("\n")]
    ops = {}
    cached_label, new_codes = "skip", None

    for label, val in data:
        if label == "mask":
            ops[cached_label] = new_codes
            new_codes = []
            cached_label = val
        elif label[:3] == "mem":
            address = int(label[4:-1])
            long_val = str(bin(int(val))[2:]).rjust(36, "0")
            new_codes.append((address, long_val))
        else:
            raise ValueError("Label must be either 'mask' or 'mem'.")

    ops[cached_label] = new_codes
    ops.pop("skip")
    return ops


def cover_up(num36: str, mask: str):
    ones = [m.start() for m in re.finditer("1", mask)]
    zeros = [m.start() for m in re.finditer("0", mask)]

    fixed = ""
    for i, digit in enumerate(num36):
        if i in ones:
            c = "1"
        elif i in zeros:
            c = "0"
        else:
            c = digit
        fixed += c
    return int(fixed, 2)


def float_through(num36: str, mask: str, mem: dict):
    """Used in part 2"""
    ones = [m.start() for m in re.finditer("1", mask)]
    quantums = [m.start() for m in re.finditer("X", mask)]

    fixed = ""
    for i, digit in enumerate(num36):
        if i in ones:
            c = "1"
        elif i in quantums:
            c = "X"
        else:
            c = digit
        fixed += c

    return mem


def fix_group(mask: str, nums: List, method: str = "mask"):
    result = {}
    if method in ["mask", "v1", 1]:
        for address, val in nums:
            result[address] = cover_up(val, mask)
    if method in ["quantum", "v2", 2]:
        for address, val in nums:
            result = float_through(val, mask, result)
    return result


def hack_the_mainframe(raw_data: str, method: str = "mask"):
    ops = parse_codes(raw_data)

    memory = {}
    for mask, nums in ops.items():
        memory.update(fix_group(mask, nums, method))

    return sum(memory.values())


c = hack_the_mainframe(sample)
assert c == 165
c = hack_the_mainframe(sample, method="quantum")


if __name__ == "__main__":
    print(hack_the_mainframe(bootcode))

    print(hack_the_mainframe(bootcode, method="quantum"))
