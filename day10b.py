import fileinput
from collections import deque

Point = tuple[int, int]


def neighbors_4(i: int, j: int, bound_i: int, bound_j: int):
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


input = list(map(list, map(str.rstrip, fileinput.input())))
bound_i = len(input)
bound_j = len(input[0])


def score(start: Point) -> int:
    result = 0
    to_visit: deque[Point] = deque([start])
    while len(to_visit) > 0:
        current = to_visit.popleft()
        height = int(input[current[0]][current[1]])
        if height == 9:
            result += 1
            continue

        for n in neighbors_4(current[0], current[1], bound_i, bound_j):
            if int(input[n[0]][n[1]]) == height + 1:
                to_visit.append(n)

    return result


total_score = 0

for i in range(bound_i):
    for j in range(bound_j):
        if input[i][j] == "0":
            total_score += score((i, j))

print(total_score)
