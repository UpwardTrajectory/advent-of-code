from typing import Dict, List, NamedTuple
from dataclasses import dataclass
from tickets import sample, notes


@dataclass
class Notes(Dict):
    prelude: Dict
    my_tkt: List
    tkts: List
    fail_tkts: set
    
    @staticmethod    
    def read_notes(data):
        prelude, my_ticket, other_tkts = data.split("\n\n")
        # Prelude
        prelude_parts = {}
        for row in prelude.split("\n"):
            label, vals = row.split(": ")
            first, second = vals.split(" or ")
            nums = (
                tuple(int(x) for x in first.split("-")), 
                tuple(int(x) for x in  second.split("-"))
            )
            prelude_parts[label] = nums

        # My Ticket
        my_ticket = my_ticket.split(":\n")[1]
        my_ticket = [int(x) for x in my_ticket.split(",")]

        # Neighboring Tickets
        other_tkts = other_tkts.split(":\n")[1]
        other_tkts = [[int(x) for x in row.split(",")] for row in other_tkts.split("\n")]
        return Notes(prelude_parts, my_ticket, other_tkts, set())


    def find_failures(self):
        """Locate neighbors with numbers outside of any possible window from the prelude"""
        failed = {}
        for i, neighbor in enumerate(self.tkts):
            failed_this_neighbor = []
            for num in neighbor:
                check_ranges = [
                    [rng[0] <= num <= rng[1] for rng in poss_ranges] 
                    for poss_ranges in self.prelude.values()
                ]
                check_ranges = [True in x for x in check_ranges]
                # num not found in any window
                if sum(check_ranges) == 0:
                    failed_this_neighbor.append(num)
                    self.fail_tkts.add(i)
            failed[i] = sum(failed_this_neighbor)
            
        return sum(failed.values())
    
    @property
    def filter_tkts(self):
        return [x for i, x in enumerate(self.tkts) if i not in self.fail_tkts]

    
n = Notes.read_notes(sample)
pred = n.find_failures()
assert pred == 71


if __name__ == "__main__":
    n = Notes.read_notes(notes)
    print(n.find_failures())
    