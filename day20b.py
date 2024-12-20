import fileinput
import math
from queue import PriorityQueue

Point = tuple[int, int]
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

bound_i = len(input)
bound_j = len(input[0])


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


def manhattan(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


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
tentative[start[0]][start[1]] = 0
prev: list[list[Point | None]] = [
    [None for _ in range(bound_i)] for _ in range(bound_j)
]

q: PriorityQueue[tuple[float, Point]] = PriorityQueue()
q.put((0, (start[0], start[1])))

shortest_dist = None

while not q.empty():
    dist, pos = q.get()
    if pos == end:
        shortest_dist = dist
        break

    if tentative[pos[0]][pos[1]] < dist:
        continue

    for ni, nj in neighbors_4(pos, bound_i, bound_j):
        if input[ni][nj] == "#":
            continue

        cand = tentative[pos[0]][pos[1]] + 1
        if cand < tentative[ni][nj]:
            prev[ni][nj] = pos
            tentative[ni][nj] = cand
            q.put((cand, (ni, nj)))

trace: Point | None = end
path = []
while True:
    assert trace is not None
    trace = prev[trace[0]][trace[1]]
    if trace is None:
        break
    path.append(trace)

num_cheats = 0
for p in reversed(path):
    for i in range(-20, 21):
        for j in range(-20, 21):
            n = (p[0] + i, p[1] + j)
            if not within_bounds(n, bound_i, bound_j):
                continue
            dist = manhattan(p, n)
            if dist > 20:
                continue
            if input[n[0]][n[1]] == "#":
                continue
            if tentative[n[0]][n[1]] - tentative[p[0]][p[1]] - dist >= 100:
                num_cheats += 1

print(num_cheats)
