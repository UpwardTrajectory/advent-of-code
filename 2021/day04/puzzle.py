import pandas as pd
import numpy as np
from dataclasses import dataclass


@dataclass
class Board:
    raw: str
    state: np.array = None

    def __post_init__(self):
        if self.state is None:
            self.state = np.zeros((5, 5), dtype=bool)

    def __repr__(self):
        return f"Board({self.orig[0]}...)"

    @property
    def orig(self):
        board = [
            row.strip().replace("  ", " ").split(" ") for row in self.raw.split("\n")
        ]
        return np.array(board).astype(int)

    @property
    def winner(self):
        horiz = self.state.all(axis=1).any()
        vert = self.state.all(axis=0).any()
        return horiz | vert

    def mark_num(self, num: int):
        self.state[np.where(self.orig == num)] = True

    def final_score(self, winning_draw):
        unmarked_sum = (self.orig * (1 - self.state)).sum()
        return winning_draw * unmarked_sum


@dataclass
class Bingo:
    draws: np.array
    boards: list[Board]

    def play(self):
        for draw in self.draws:
            for board in self.boards:
                board.mark_num(draw)
                if board.winner:
                    return board.final_score(draw)

    def last_board(self):
        win_order = []
        for draw in self.draws:
            for board in self.boards:
                board.mark_num(draw)
                if board.winner and board not in win_order:
                    win_order.append(board)
                if len(win_order) == len(self.boards):
                    return board.final_score(draw)


def parse_raw(fname: str) -> tuple[np.array, list[np.array]]:
    with open(fname, "r") as f:
        raw = f.read().strip()

    draws, *boards = raw.split("\n\n")
    draws = np.array(draws.split(",")).astype(int)
    boards = [Board(raw) for raw in boards]
    return draws, boards


def play_game(fname: str) -> int:
    draws, boards = parse_raw(fname)
    game = Bingo(draws, boards)
    return game.play()


def find_last_board_score(fname: str) -> int:
    draws, boards = parse_raw(fname)
    game = Bingo(draws, boards)
    return game.last_board()


draws, boards = parse_raw("test.txt")
game = Bingo(draws, boards)
t1 = game.play()
assert t1 == 4512, f"Test 1 failed. Got {t1} instead of 4512."

t2 = game.last_board()
assert t2 == 1924, f"Test 2 failed. Got {t2} instead of 1924."


print("All tests passed.")


if __name__ == "__main__":
    p1 = play_game("inputs.txt")
    print("Part 1:", p1)

    p2 = find_last_board_score("inputs.txt")
    print("Part 2:", p2)
