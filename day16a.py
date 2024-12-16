import fileinput
from enum import Enum, auto
from collections import deque
from dataclasses import dataclass


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

    def opposite(self) -> "Direction":
        match self:
            case Direction.Up:
                return Direction.Down
            case Direction.Down:
                return Direction.Up
            case Direction.Right:
                return Direction.Left
            case Direction.Left:
                return Direction.Right

    def turn_ccw(self) -> "Direction":
        match self:
            case Direction.Up:
                return Direction.Left
            case Direction.Down:
                return Direction.Right
            case Direction.Right:
                return Direction.Up
            case Direction.Left:
                return Direction.Down

    def turn_cw(self) -> "Direction":
        match self:
            case Direction.Up:
                return Direction.Right
            case Direction.Down:
                return Direction.Left
            case Direction.Right:
                return Direction.Down
            case Direction.Left:
                return Direction.Up


Point = tuple[int, int]


def move(p: Point, dir: Direction) -> Point:
    match dir:
        case Direction.Up:
            return (p[0] - 1, p[1])
        case Direction.Down:
            return (p[0] + 1, p[1])
        case Direction.Left:
            return (p[0], p[1] - 1)
        case Direction.Right:
            return (p[0], p[1] + 1)


@dataclass
class State:
    pos: Point
    dir: Direction
    score: int


start: Point | None = None
end: Point | None = None
input = list(map(list, map(str.rstrip, fileinput.input())))

for i, row in enumerate(input):
    for j, c in enumerate(row):
        if c == "S":
            start = (i, j)
        elif c == "E":
            end = (i, j)

assert start is not None
assert end is not None

queue: deque[State] = deque()
queue.append(State(start, Direction.Right, 0))

best_score: dict[tuple[Point, Direction], int] = dict()

while len(queue) > 0:
    s = queue.popleft()
    key = (s.pos, s.dir)
    previous_best = best_score.get(key)
    if previous_best is None or s.score < previous_best:
        best_score[key] = s.score
    else:
        continue

    if s.pos == end:
        continue

    pos_ahead = move(s.pos, s.dir)
    if input[pos_ahead[0]][pos_ahead[1]] != "#":
        queue.append(State(pos_ahead, s.dir, s.score + 1))

    queue.append(State(s.pos, s.dir.turn_cw(), s.score + 1000))
    queue.append(State(s.pos, s.dir.turn_ccw(), s.score + 1000))

print([best_score.get((end, d)) for d in Direction])
