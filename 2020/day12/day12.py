import math
from typing import List, Dict, NamedTuple, Literal
from dataclasses import dataclass
from nav_instructions import sample, instructions


class Instruction(NamedTuple):
    cmd: Literal["N", "S", "E", "W", "L", "R", "F"]
    val: int

    @staticmethod
    def read(x: str):
        return Instruction(cmd=x[0], val=int(x[1:]))


@dataclass
class Status(Dict):
    x: int
    y: int
    facing: Literal["N", "S", "E", "W", None]


class Boat(NamedTuple):
    plan: List[Instruction]
    origin: Status = Status(x=0, y=0, facing="E")
    status: Status = Status(x=0, y=0, facing="E")
    waypoint: Status = Status(x=10, y=1, facing="E")

    @staticmethod
    def initialize(data: str):
        parsed_instructions = [Instruction.read(x) for x in data.split("\n")]
        start = Status(x=0, y=0, facing="E")
        current = Status(x=0, y=0, facing="E")
        wp = Status(x=10, y=1, facing=None)
        return Boat(plan=parsed_instructions, origin=start, status=current, waypoint=wp)

    def do_one(self, move: Instruction):
        """Process a single move & update self.status"""
        cmd, val = move
        # Movement
        if cmd == "N":
            self.status.y += val
        elif cmd == "S":
            self.status.y -= val
        elif cmd == "E":
            self.status.x += val
        elif cmd == "W":
            self.status.x -= val
        elif cmd == "F":
            self.do_one(Instruction(cmd=self.status.facing, val=val))

        # Turning
        elif cmd in "LR":
            directions = list("NESWNES")

            if cmd == "L":
                directions = directions[::-1]

            self.status.facing = directions.pop(
                directions.index(self.status.facing) + val // 90
            )
        return

    def waypoint_one(self, move: Instruction):
        cmd, val = move
        # Movement
        if cmd == "N":
            self.waypoint.y += val
        elif cmd == "S":
            self.waypoint.y -= val
        elif cmd == "E":
            self.waypoint.x += val
        elif cmd == "W":
            self.waypoint.x -= val
        elif cmd == "L":
            self.rotate_waypoint(val)
        elif cmd == "R":
            self.rotate_waypoint(-val)
        elif cmd == "F":
            delta_x = self.waypoint.x - self.status.x
            delta_y = self.waypoint.y - self.status.y

            self.status.x += delta_x * val
            self.status.y += delta_y * val
            self.waypoint.x = self.status.x + delta_x
            self.waypoint.y = self.status.y + delta_y
        return

    def rotate_waypoint(self, deg):
        """Adapted from here:
        https://stackoverflow.com/a/34374437
        """
        angle = deg * math.pi / 180
        ox, oy = self.status.x, self.status.y
        px, py = self.waypoint.x, self.waypoint.y

        self.waypoint.x = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        self.waypoint.y = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return

    def navigate(self, method=None):
        if method in ["waypoint", "wp", 2]:
            func = self.waypoint_one
        else:
            func = self.do_one
        for move in self.plan:
            func(move)
        return int(abs(self.status.x) + abs(self.status.y))

    @property
    def dwp(self):
        """Helper function to display offset of the waypoint instead of its exact position"""
        return self.waypoint.x - self.status.x, self.waypoint.y - self.status.y


b = Boat.initialize(sample)
taxi_dist = b.navigate()
assert taxi_dist == 25

w = Boat.initialize(sample)
taxi_dist = w.navigate("waypoint")
assert taxi_dist == 286


if __name__ == "__main__":
    b = Boat.initialize(instructions)
    print(b.navigate())

    w = Boat.initialize(instructions)
    print(w.navigate("wp"))
