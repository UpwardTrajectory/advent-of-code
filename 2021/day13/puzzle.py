from pathlib import Path
from dataclasses import dataclass, field


T1_ANS = 10
T2_ANS = None


@dataclass
class Cave:
    name: str
    revisit: bool
    seen: bool = False
    neighbors: set = field(default_factory=set, repr=False)   
    
    def __hash__(self):
        return hash(self.name)
    
    def check_all_visited(self) -> bool:
        all_visited = False
        for c in self.neighbors:
            if not c.seen:
                continue
            if not c.revisit:
                
        if all_seen:
            if self.name == "A":
                print(self.neighbors)
                print("closing A")
            self.revisit = False
#             print("<<closing off", self.name, end=">>")
            return True
        return False
    

@dataclass
class Puzzle:
    fname: str
    caves: dict[str: Cave] = field(default_factory=dict, repr=False)
#     visited: set[Cave] = field(default_factory=set, repr=False)
    paths: int = 0
    all_path_routes: list[str] = field(default_factory=list, repr=False)

    def __post_init__(self):
        raw = Path(self.fname).open().readlines()     
        for conn in raw:
            a, b = conn.strip().split("-")         
            for cave_name in (a, b):
                if cave_name not in self.caves:
                    if cave_name == cave_name.lower():
                        self.caves[cave_name] = Cave(cave_name, False)
                    else:
                        self.caves[cave_name] = Cave(cave_name, True)            
            self.connect(self.caves[a], self.caves[b])
        return
    
    def connect(self, a, b):
        a.neighbors.add(b)
        b.neighbors.add(a)
        return        
        
    def dfs(self, cave=None, cur_path=None):
        if cave is None:
            cave = self.caves['start']
            cur_path = "start"
        
        cave.seen = True
    
        if cave.name == 'end':
            self.paths += 1
            self.all_path_routes.append(cur_path)
            if cave.check_all_visited():
                print("------- All paths explored ------")
            else:
                return self.dfs()
            
        cave.check_all_visited()
        
        for neighbor in cave.neighbors:                
            if neighbor.revisit or not neighbor.seen:
                updated_path = cur_path + "," + neighbor.name
                self.dfs(neighbor, cur_path=updated_path)     
                
        return  
    
    def find_many(self):
        n = 0
        while True:
            if n > 1000:
                break
            self.dfs()
            n += 1
        return self.paths
            

    def part_1(self):
        pass

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
    run_tests(19, None, fname='tests2.txt')
    run_tests(226, None, fname='tests3.txt')


    puz = Puzzle("inputs.txt")

    p1 = puz.part_1()
    print("Part 1:", p1)

    if T2_ANS is not None:
        p2 = puz.part_2()
        print("Part 2:", p2)