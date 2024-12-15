import fileinput
from itertools import takewhile, chain
from enum import Enum, auto


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

    @classmethod
    def from_char(cls, c: str) -> "Direction":
        match c:
            case "^":
                return Direction.Up
            case "v":
                return Direction.Down
            case "<":
                return Direction.Left
            case ">":
                return Direction.Right
            case _:
                raise RuntimeError


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


input = map(str.rstrip, fileinput.input())
position: Point | None = None
objects: dict[Point, str] = dict()

for i, line in enumerate(takewhile(lambda line: line, input)):
    for j, c in enumerate(line):
        if c == "@":
            position = (i, j)
        if c == "#" or c == "O":
            objects[(i, j)] = c

assert position is not None


def gps(p: Point) -> int:
    return 100 * p[0] + p[1]


for d in map(Direction.from_char, chain(*input)):
    ahead = move(position, d)
    match objects.get(ahead):
        case None:
            position = ahead
        case "O":
            temp = move(ahead, d)
            temp_obj = objects.get(temp)
            while temp_obj == "O":
                temp = move(temp, d)
                temp_obj = objects.get(temp)

            if temp_obj is None:
                objects.pop(ahead)
                objects[temp] = "O"
                position = ahead

print(
    sum(
        map(
            lambda pair: gps(pair[0]),
            filter(lambda pair: pair[1] == "O", objects.items()),
        )
    )
)
