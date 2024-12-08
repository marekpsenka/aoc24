import fileinput
from collections import defaultdict
from math import gcd
from itertools import combinations

Point = tuple[int, int]
Vector = tuple[int, int]
input = list(map(list, map(str.rstrip, fileinput.input())))
bound_i = len(input)
bound_j = len(input[0])
antennae: defaultdict[str, list[Point]] = defaultdict(list)


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


def vec_from_to(p1: Point, p2: Point) -> Vector:
    return (p2[0] - p1[0], p2[1] - p1[1])


def quasi_normalize(v: Vector) -> Vector:
    d = gcd(v[0], v[1])
    return (v[0] // d, v[1] // d)


def point_plus_vector(p: Point, v: Vector) -> Point:
    return (p[0] + v[0], p[1] + v[1])


def manhattan(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def flip(v: Vector) -> Vector:
    return (-v[0], -v[1])


def seek(p1: Point, direction: Vector) -> list[Point]:
    result: list[Point] = [p1]
    p = p1
    while True:
        p = point_plus_vector(p, direction)
        if not within_bounds(p[0], p[1], bound_i, bound_j):
            break
        result.append(p)

    return result


for i in range(bound_i):
    for j in range(bound_j):
        if input[i][j] == ".":
            continue
        antennae[input[i][j]].append((i, j))

unique_antinodes: set[Point] = set()

for _, locations in antennae.items():
    for p1, p2 in combinations(locations, 2):
        direction = quasi_normalize(vec_from_to(p1, p2))
        for p in seek(p1, direction):
            unique_antinodes.add(p)
        for p in seek(p1, flip(direction)):
            unique_antinodes.add(p)

print(len(unique_antinodes))
