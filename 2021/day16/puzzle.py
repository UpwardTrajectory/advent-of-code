from pathlib import Path
from typing import Literal
from dataclasses import dataclass, field
import numpy as np


T1_ANS = [16,12,23,31]
T2_ANS = None


@dataclass
class Puzzle:
    fname: str
    raw : str = field(default=None, repr=False)
    bin_list: list[str] = field(default=None, repr=False)
    version_list: list[int] = field(default_factory=list, repr=False)
    
    def __post_init__(self):
        raw = Path(self.fname).open().readlines()  # or read() for a big block of text
        self.raw = raw
        self.bin_list = self.hex_to_bin()
        return
    
    def hex_to_bin(self, hex_list=None):
        """https://stackoverflow.com/a/4859937/14083170"""
        if hex_list is None:
            hex_list = self.raw
        binaries = [bin(int(n, 16))[2:].rstrip("0") for n in hex_list]
        
        # save leading zeros
        final_binaries = []
        for hx, bn in zip(hex_list, binaries):
            if hx[0] in "0123":
                final_binaries.append("00" + bn)
            elif hx[0] in "4567":
                final_binaries.append("0" + bn)
            else:
                final_binaries.append(bn)
        
        return final_binaries
    
    def decode_packet(self, pkt: str):
        version, type_id, other = pkt[:3], pkt[3:6], pkt[6:]
        version = int(version, 2)
        self.version_list.append(version)
        type_id = int(type_id, 2)
        
        if type_id == 4:
            return self.parse_literal_other(other)
        
        #  first 
        # next 15 bits == length of subpacket 
        if other[0] == "0":
            sub_len = int(other[1:16], 2)
            sub_str = other[16: 16 + sub_len]
            while len(sub_str) < sub_len:
                sub_str = sub_str + "0"
            leftovers = other[17 + sub_len:]
            return sub_str, leftovers
        
        # next 11 bits == total number of subpackets
        return int(other[1:12], 2), other[12:]
        
        
    @staticmethod
    def parse_literal_other(other):
        quick_test = other[::5]
        assert quick_test[-1] == "0", "Final 5 bits should start w/ '0'."
        assert set(quick_test[:-1]) == {"1"}, "Every 5 bits except last should start w/ '1'."
        
        num = "".join([other[i + 1 : i + 5] for i in range(0, len(other), 5)])
        
        return int(num, 2)
    
#     @staticmethod
#     def packet_id_reader(type_id, other):
#         if type_id == 4:
#             return 4, None, parse_literal_other(other)
        
#         if other[0] == "0":
            
#         if other[0] == "1":
            
#         raise SyntaxError("You shouldn't get here.")
    
    
    def part_1(self):
        return sum(self.version_list)

    def part_2(self):
        pass


def run_tests(p1_ans=T1_ANS, p2_ans=T2_ANS, fname="tests.txt"):
    puz = Puzzle(fname)
    t1 = puz.part_1()
    assert t1 == p1_ans, f"Test 1 failed. Got {t1} instead of {p1_ans}"

    if p2_ans is not None:
        t2 = puz.part_2()
        assert t2 == p2_ans, f"Test 2 failed. Got {t2} instead of {p2_ans}"

    print("All tests passed.")
    return


if __name__ == "__main__":
    run_tests()

    puz = Puzzle("inputs.txt")

    p1 = puz.part_1()
    print("Part 1:", p1)

    if T2_ANS is not None:
        p2 = puz.part_2()
        print("Part 2:", p2)