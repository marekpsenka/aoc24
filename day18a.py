import fileinput
import math
from queue import PriorityQueue

Point = tuple[int, int]


def parse_point(s: str) -> Point:
    x_str, y_str = s.split(",")
    return (int(x_str), int(y_str))


input = map(str.rstrip, fileinput.input())
bytes: set[Point] = set(parse_point(next(input)) for _ in range(1024))

bound_i = 71
bound_j = 71


def neighbors_4(p: Point, bound_i: int, bound_j: int) -> list[Point]:
    i, j = p
    if i == 0:
        if j == 0:
            return [(1, 0), (0, 1)]

        if j == bound_j - 1:
            return [(1, bound_j - 1), (0, bound_j - 2)]

        return [(0, j - 1), (1, j), (0, j + 1)]

    if i == bound_i - 1:
        if j == bound_j - 1:
            return [(bound_i - 2, bound_j - 1), (bound_i - 1, bound_j - 2)]

        if j == 0:
            return [(bound_i - 1, 1), (bound_i - 2, 0)]

        return [(bound_i - 1, j - 1), (bound_i - 2, j), (bound_i - 1, j + 1)]

    if j == 0:
        return [(i - 1, 0), (i, 1), (i + 1, 0)]

    if j == bound_j - 1:
        return [(i - 1, bound_j - 1), (i, bound_j - 2), (i + 1, bound_j - 1)]

    return [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]


tentative = [[math.inf for _ in range(bound_i)] for _ in range(bound_j)]
tentative[0][0] = 0

q: PriorityQueue[tuple[float, Point]] = PriorityQueue()
q.put((0, (0, 0)))

shortest_dist = None

while not q.empty():
    dist, pos = q.get()
    if pos == (bound_i - 1, bound_j - 1):
        shortest_dist = dist
        break

    if tentative[pos[0]][pos[1]] < dist:
        continue

    for ni, nj in neighbors_4(pos, bound_i, bound_j):
        if (ni, nj) in bytes:
            continue

        cand = tentative[pos[0]][pos[1]] + 1
        if cand < tentative[ni][nj]:
            tentative[ni][nj] = cand
            q.put((cand, (ni, nj)))

print(shortest_dist)
