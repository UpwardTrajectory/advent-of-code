from pathlib import Path
from typing import Literal
from dataclasses import dataclass, field
from itertools import cycle
import numpy as np


T1_ANS = 739785
T2_ANS = 444356092776315


@dataclass
class Player:
    pos: Literal[range(1, 11)]
    score: int = 0
    total_rolls: int = 0
    winner: bool = False
    dirac_scorer: np.array = field(default=np.identity(10).astype(np.int64) * range(1, 11), repr=False)
    # dirac: list = [
    #     3, 4, 5, 4, 5, 6, 5, 6, 7,  # sum(1, x, y)
    #     4, 5, 6, 5, 6, 7, 6, 7, 8,  # sum(2, x, y)
    #     5, 6, 7, 6, 7, 8, 7, 8, 9   # sum(3, x, y)
    # ]

    def advance(self, rolls: list[int, int, int]):
        self.total_rolls += 3
        self.pos = (self.pos + sum(rolls)) % 10

        if self.pos == 0:
            self.pos = 10
        self.score += self.pos

        if self.score >= 1000:
            self.winner = True
            print("WINNER!:", self)

        return
    
    def advance_dirac(self, start=None, n=3):
        if start is None:
            start = np.zeros(10).astype(np.int64)
            start[self.pos - 1] = 1
         # fmt: off
        changer = np.array([
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        ]).astype(np.int64)
        # fmt: on
        return start @ np.linalg.matrix_power(changer, n)

    def score_dirac(self):
        pass


@dataclass
class Puzzle:
    fname: str

    def __post_init__(self):
        raw = Path(self.fname).open().readlines()  # or read() for a big block of text
        self.p1 = Player(int(raw[0].split(": ")[-1]))
        self.p2 = Player(int(raw[1].split(": ")[-1]))
        return

    def part_1(self):
        p1 = self.p1
        p2 = self.p2

        roll_deterministic = cycle(range(1, 101))
        players = cycle([p1, p2])

        plyr = next(players)

        for _ in range(1111):

            next_3 = [next(roll_deterministic) for _ in range(3)]
            plyr.advance(next_3)
            if plyr.winner:
                return next(players).score * (p1.total_rolls + p2.total_rolls)
                # return f"{(lps := next(players).score)}  * {(tr := p1.total_rolls + p2.total_rolls)} = {lps * tr}"
            plyr = next(players)

    def part_2(self):
        self.__post_init__()
        
        p1 = self.p1
        p2 = self.p2
        

def run_tests(p1_ans=T1_ANS, p2_ans=T2_ANS, fname="tests.txt"):
    puz = Puzzle(fname)
    t1 = puz.part_1()
    assert t1 == p1_ans, f"Test 1 failed. Got {t1} instead of {p1_ans}"

    if p2_ans is not None:
        t2 = puz.part_2()
        assert t2 == p2_ans, f"Test 2 failed. Got {t2} instead of {p2_ans}"

    print("All tests passed.")
    return


# if __name__ == "__main__":
#     run_tests()

#     puz = Puzzle("inputs.txt")

#     p1 = puz.part_1()
#     print("Part 1:", p1)

#     if T2_ANS is not None:
#         p2 = puz.part_2()
#         print("Part 2:", p2)

## After messing w/ a lot of different matrix strategies, I caved & looked up an answer:
## https://www.reddit.com/r/adventofcode/comments/rn2eom/2021_day_21_python_help_with_part2_subtle_error/

from functools import cache
from itertools import product
from typing import NamedTuple


class State(NamedTuple):
    scores: tuple[int, int]
    positions: tuple[int, int]
    turn: int


@cache
def ways_to_reach(state: State, initial_state: State):

    # base cases
    if state == initial_state:
        return 1
    if state.scores < initial_state.scores:
        return 0

    player = prev_turn = 1 - state.turn  # it was the other player's turn
    prev_states = []

    # loop over all possible outcomes of 3 rolls and go back a turn
    for roll_seq in product(range(1, 4), repeat=3):
        roll = sum(roll_seq)
        scores = list(state.scores)
        positions = list(state.positions)

        scores[player] -= positions[player]
        positions[player] -= roll
        positions[player] = (positions[player] - 1) % 10 + 1

        if max(scores) < 21:  # otherwise game already over
            prev_states.append(
                State(scores=tuple(scores), positions=tuple(positions), turn=player)
            )

    return sum(ways_to_reach(prev_state, initial_state) for prev_state in prev_states)


def part2(initial_state: State):
    winning_states_0 = (
        State(scores=(s0, s1), positions=(p0, p1), turn=1)
        for s0 in range(21, 31)
        for s1 in range(1, 21)
        for p0 in range(1, 11)
        for p1 in range(1, 11)
    )
    winning_states_1 = (
        State(scores=(s0, s1), positions=(p0, p1), turn=0)
        for s0 in range(1, 21)
        for s1 in range(21, 31)
        for p0 in range(1, 11)
        for p1 in range(1, 11)
    )
    p0_wins = sum(ways_to_reach(state, initial_state) for state in winning_states_0)
    p1_wins = sum(ways_to_reach(state, initial_state) for state in winning_states_1)
    return max(p0_wins, p1_wins)


def main():
    initial_state = State((0, 0), (6, 4), 0)
    print(part2(initial_state))


if __name__ == "__main__":
    main()