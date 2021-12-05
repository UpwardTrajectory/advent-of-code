from itertools import cycle
from dataclasses import dataclass


SAMPLE = "389125467"
STARTING_LINEUP = "562893147"


@dataclass
class CupGame(dict):
    pointer: int
    cups: list
    step_down: cycle
    taken: dict
    cached_pointer: int

    @staticmethod
    def build(data):
        pointer_out = int(data[0])
        cups_out = {int(x): int(y) for x, y in zip(data, data[1:] + data[0])}
        step_down_out = cycle(sorted(cups_out)[::-1])
        taken_out = dict()
        return CupGame(pointer_out, cups_out, step_down_out, taken_out, pointer_out)

    def mega_upgrade(self, total=1000000):
        next_num = max(self.cups) + 1
        new_nums = list(range(next_num, total + 1))
        upgrade = {x: y for x, y in zip(new_nums, new_nums[1:] + [self.pointer])}
        last_orig = list(self.cups)[-1]
        upgrade[last_orig] = new_nums[0]
        self.cups.update(upgrade)
        self.step_down = cycle(sorted(self.cups)[::-1])
        return

    def take_cups(self):
        """Based on current pointer, set aside the next 3 cups, and bridge 
        the gap between where they were removed. (Pointer doesn't move)
        """
        cups = self.cups
        p = self.pointer

        next_3 = [cups[p], cups[cups[p]], cups[cups[cups[p]]]]
        new_p = cups[cups[cups[cups[p]]]]
        taken = []
        for mini_pointer in next_3:
            taken.append([mini_pointer, cups[mini_pointer]])

        self.taken = taken
        self.cups[p] = new_p
        #         print(f"Updating connection @ {p} from {next_3[0]} -> {new_p}.")
        return taken

    def move_pointer(self):
        """Sync pointer w/ descending options, then find next value not inside taken cups"""
        p = self.pointer
        self.cached_pointer = p
        nxt = next(self.step_down)
        while p != nxt:
            nxt = next(self.step_down)
        p = next(self.step_down)

        taken = [x[0] for x in self.taken]

        while p in taken:
            #             print("avoiding taken cups", p)
            p = next(self.step_down)

        self.pointer = p
        #         print(f"           New Pointer: {p}\n")
        return self.pointer

    def insert_cups(self):
        self.taken[2][1] = self.cups[self.pointer]
        self.cups[self.pointer] = self.taken[0][0]

        incoming = {x[0]: x[1] for x in self.taken}
        self.cups.update(incoming)
        self.pointer = self.cups[self.cached_pointer]
        return self.cups

    def play_rounds(self, n, version=1):
        for i in range(n):
            #             print(f"------   Round {i+1}   ------")
            self.take_cups()
            self.move_pointer()
            self.insert_cups()
            if (n > 1000) and (i % 1000):
                print(round(i / n, 5))

        if version == 1:
            return self.final_order
        return self.star_cups_product

    @property
    def final_order(self):
        cursor = self.cups[1]
        order = str(cursor)

        while cursor != 1:
            cursor = self.cups[cursor]
            order += str(cursor)

        return order[:-1]

    @property
    def star_cups_product(self):
        first = self.cups[1]
        second = self.cups[first]
        return first * second


game = CupGame.build(SAMPLE)

pred_10 = game.play_rounds(10)
assert pred_10 == "92658374"

pred_100 = game.play_rounds(90)
assert pred_100 == "67384529"

###  WARNING:  not optimized, takes ~24 days to run
# big_sample_game = CupGame.build(SAMPLE)
# big_sample_game.mega_upgrade()
# big_sample_game.play_rounds(int(1e7), version=2)
# pred_1M = big_sample_game.star_cups_product
# assert pred_1M == 149245887792


if __name__ == "__main__":
    real_game = CupGame.build(STARTING_LINEUP)
    print(real_game.play_rounds(100))
