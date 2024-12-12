import fileinput
from enum import Enum, auto
from collections import defaultdict

input = list(map(list, map(str.rstrip, fileinput.input())))


Point = tuple[int, int]


def within_bounds(p: Point, max_i: int, max_j: int) -> bool:
    i, j = p
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


class Direction(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()


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


def neighbors_4_naive(p: Point) -> list[Point]:
    i, j = p
    return [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]


def search(input: list[list[str]], start: Point) -> set[Point]:
    visited: set[Point] = set()
    queue: list[Point] = [start]
    bound_i = len(input)
    bound_j = len(input[0])
    region = input[start[0]][start[1]]

    while len(queue) > 0:
        current = queue.pop()
        visited.add(current)
        for n in neighbors_4_naive(current):
            if not within_bounds(n, bound_i, bound_j):
                continue
            if n in visited:
                continue
            if input[n[0]][n[1]] != region:
                continue
            queue.append(n)

    return visited


def components(input: list[list[str]]) -> dict[int, set[Point]]:
    bound_i = len(input)
    bound_j = len(input[0])
    visited: set[Point] = set()
    components: dict[int, set[Point]] = dict()
    free_id = 0

    for i in range(bound_i):
        for j in range(bound_j):
            if (i, j) in visited:
                continue

            search_result = search(input, (i, j))
            visited = visited.union(search_result)
            components[free_id] = search_result
            free_id += 1

    return components


def count_lines(slice: list[int]) -> int:
    result = 0
    i = 0
    while i < len(slice):
        while (i < len(slice) - 1) and (slice[i] + 1 == slice[i + 1]):
            i += 1
        result += 1
        i += 1

    return result


cs = components(input)

total_price = 0
for _, plots in cs.items():
    fence: defaultdict[tuple[int, Direction], list[int]] = defaultdict(list)
    for plot in plots:
        for d in Direction:
            n = move(plot, d)
            if n not in plots:
                if d == Direction.Up or d == Direction.Down:
                    fence[(plot[0], d)].append(plot[1])
                else:
                    fence[(plot[1], d)].append(plot[0])

    sides = 0
    for slice in fence.values():
        slice.sort()
        sides += count_lines(slice)

    total_price += sides * len(plots)


print(total_price)
