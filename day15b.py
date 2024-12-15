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
        match c:
            case "@":
                position = (i, 2 * j)
            case "#":
                objects[(i, 2 * j)] = "#"
                objects[(i, 2 * j + 1)] = "#"
            case "O":
                objects[(i, 2 * j)] = "["
                objects[(i, 2 * j + 1)] = "]"

assert position is not None


def peek(p: Point, d: Direction) -> str | None:
    ahead = move(p, d)
    return objects.get(ahead)


def gps(p: Point) -> int:
    return 100 * p[0] + p[1]


def push_move_lr(start: Point, d: Direction) -> bool:
    temp = move(start, d)
    temp_obj = objects.get(temp)
    while temp_obj == "[" or temp_obj == "]":
        temp = move(temp, d)
        temp_obj = objects.get(temp)
    if temp_obj is not None:
        assert temp_obj == "#"
        return False

    temp2 = temp
    while temp2 != start:
        temp3 = move(temp2, d.opposite())
        objects[temp2] = objects[temp3]
        temp2 = temp3

    objects.pop(start)
    return True


def push_ud(p: Point, d: Direction) -> set[Point] | None:
    ahead = move(p, d)
    match objects.get(ahead):
        case None:
            return set([p])
        case "#":
            return None
        case "[":
            res1 = push_ud(ahead, d)
            if res1 is None:
                return None
            res2 = push_ud(move(ahead, Direction.Right), d)
            if res2 is None:
                return None

            return res1.union(res2).union([p])
        case "]":
            res1 = push_ud(ahead, d)
            if res1 is None:
                return None
            res2 = push_ud(move(ahead, Direction.Left), d)
            if res2 is None:
                return None

            return res1.union(res2).union([p])
        case _:
            raise RuntimeError


def move_ud(ps: set[Point], d: Direction):
    temp: dict[Point, str] = dict()
    for p in ps:
        temp[p] = objects.pop(p)
    for p in ps:
        objects[move(p, d)] = temp[p]


for d in map(Direction.from_char, chain(*input)):
    ahead = move(position, d)
    obj_ahead = objects.get(ahead)
    if obj_ahead is None:
        position = ahead
    elif obj_ahead == "#":
        continue
    else:
        if d == Direction.Left or d == Direction.Right:
            if push_move_lr(ahead, d):
                position = ahead
        else:
            push_res = push_ud(ahead, d)
            if push_res is None:
                continue
            if obj_ahead == "[":
                push_res2 = push_ud(move(ahead, Direction.Right), d)
            else:
                push_res2 = push_ud(move(ahead, Direction.Left), d)
            if push_res2 is None:
                continue

            move_ud(push_res.union(push_res2), d)
            position = ahead

print(
    sum(
        map(
            lambda pair: gps(pair[0]),
            filter(lambda pair: pair[1] == "[", objects.items()),
        )
    )
)
