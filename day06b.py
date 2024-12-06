import fileinput
from enum import Enum, auto


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

    def turn_right(self) -> "Direction":
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


def within_bounds(i: int, j: int, max_i: int, max_j: int) -> bool:
    if i < 0:
        return False
    elif i >= max_i:
        return False
    elif j < 0:
        return False
    elif j >= max_j:
        return False
    else:
        return True


input = list(map(list, map(str.rstrip, fileinput.input())))
max_i = len(input)
max_j = len(input[0])


def peek(p: Point, d: Direction) -> str:
    ahead_i, ahead_j = move(p, d)
    if within_bounds(ahead_i, ahead_j, max_i, max_j):
        return input[ahead_i][ahead_j]
    else:
        return str()


start: Point = (0, 0)
for i in range(max_i):
    for j in range(max_j):
        if input[i][j] == "^":
            start = (i, j)


loops = 0

for i in range(max_i):
    for j in range(max_j):
        if input[i][j] != ".":
            continue

        input[i][j] = "#"
        visited: set[tuple[Point, Direction]] = set()
        p = start
        d = Direction.Up
        while True:
            if (p, d) not in visited:
                visited.add((p, d))
            else:
                loops += 1
                input[i][j] = "."
                break

            whats_ahead = peek(p, d)
            while whats_ahead == "#":
                d = d.turn_right()
                whats_ahead = peek(p, d)

            if not whats_ahead:
                input[i][j] = "."
                break
            p = move(p, d)

print(loops)
