from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Digit:
    """For ease, can be instantiated w/ a string, but gets turned into a set"""
    signal: set 
    result: int = None
        
    def __post_init__(self):
        self.signal = set(self.signal)
        self.easy_num()
        return
    
    def __len__(self):
        return len(self.signal)
    
    def easy_num(self):
        easy_nums = {2: 1, 4: 4, 3: 7, 7: 8}
        self.result = easy_nums.get(len(self), None)
        return
    
    
    

@dataclass
class EasyDigits:
    fpath: str
    inputs: list[str] = field(default_factory=list, repr=False)
    outputs: list[str] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        lines = Path(self.fpath).read_text().split("\n")
        for line in lines:
            pre, post = line.split("|")
            self.inputs.append(pre.strip().split(" "))
            self.outputs.append(post.strip().split(" "))
        return
    
    def part_1(self) -> int:
        n_segments: '{num_lines: actual_num}' = {2: 1, 4: 4, 3: 7, 7: 8}
        num_easy = 0
        for obs in self.outputs:
            for num in obs:
                if len(num) in n_segments:
                    num_easy += 1
        return num_easy
    
    def part_2(self): -> int:
        return sum(self.decoded_outputs)
    
    
digits = EasyDigits('tests.txt')
t1 = digits.part_1()
assert t1 == 26, f"Test 1 failed. Got {t1} instead of 26"

t2 = digits.part_2()
assert t2 == 61229, f"Test 2 failed. Got {t2} instead of 61229"

print("All tests passed.")


if __name__ == "__main__":
    digits = EasyDigits("inputs.txt")

    p1 = digits.part_1()
    print("Part 1:", p1)

#     p2 = crabs.part_2()
#     print("Part 2:", p2)
