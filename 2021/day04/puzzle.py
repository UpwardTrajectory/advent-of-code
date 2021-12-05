import numpy as np
from dataclasses import dataclass, field


@dataclass
class Board:
    raw: str
    marked_grid: np.array(bool) = None  # default to all False in post_init()
    winning_score: int = None

    def __post_init__(self) -> None:
        if self.marked_grid is None:
            self.marked_grid = np.zeros((5, 5), dtype=bool)

    def __repr__(self) -> str:
        return f"Board({self.number_grid[0]}...)"

    @property
    def number_grid(self) -> np.array:
        board = [
            row.strip().replace("  ", " ").split(" ") for row in self.raw.split("\n")
        ]
        return np.array(board).astype(int)

    @property
    def winner(self) -> bool:
        horiz = self.marked_grid.all(axis=1).any()
        vert = self.marked_grid.all(axis=0).any()
        return horiz | vert

    def mark_num(self, num: int):
        self.marked_grid[np.where(self.number_grid == num)] = True

    def final_score(self, winning_draw: int) -> int:
        if self.winning_score is not None:
            return self.winning_score
        unmarked_sum = (self.number_grid * (1 - self.marked_grid)).sum()
        self.winning_score = winning_draw * unmarked_sum
        return self.winning_score


@dataclass
class Bingo:
    """refactored after knowing part 2 needed all games to eventually win"""

    draws: np.array
    boards: list[Board]
    winning_score: int = None
    last_loser_score: int = None
    win_order: list[Board] = field(default_factory=list)

    def play_all(self) -> None:
        for draw in self.draws:
            for board in self.boards:
                board.mark_num(draw)
                if board.winner:
                    winning_score = board.final_score(draw)
                    if self.winning_score is None:
                        self.winning_score = winning_score
                    if board not in self.win_order:
                        self.win_order.append(board)
                    if len(self.win_order) == len(self.boards):
                        self.last_loser_score = winning_score
                        return


def parse_raw(fname: str) -> tuple[np.array, list[Board]]:
    with open(fname, "r") as f:
        raw = f.read().strip()

    draws, *boards = raw.split("\n\n")
    draws = np.array(draws.split(",")).astype(int)
    boards = [Board(raw) for raw in boards]
    return draws, boards


game = Bingo(*parse_raw("test.txt"))
game.play_all()
t1 = game.winning_score
assert t1 == 4512, f"Test 1 failed. Got {t1} instead of 4512."

t2 = game.last_loser_score
assert t2 == 1924, f"Test 2 failed. Got {t2} instead of 1924."


print("All tests passed.")


if __name__ == "__main__":
    game = Bingo(*parse_raw("inputs.txt"))
    game.play_all()

    p1 = game.winning_score
    print("Part 1:", p1)

    p2 = game.last_loser_score
    print("Part 2:", p2)
