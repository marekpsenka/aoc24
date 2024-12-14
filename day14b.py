import fileinput
from re import search

Vec2 = tuple[int, int]


def extract_pos_vel(s: str) -> tuple[Vec2, Vec2]:
    m = search(r"p\=(\d+),(\d+) v\=(-?\d+),(-?\d+)", s)
    assert m is not None
    return (
        (int(m.group(1)), int(m.group(2))),
        (int(m.group(3)), int(m.group(4))),
    )


def sum_scaled(v: Vec2, w: Vec2, s: Vec2) -> Vec2:
    return (s[0] * v[0] + s[1] * w[0], s[0] * v[1] + s[1] * w[1])


def neighbors_4_naive(p: Vec2) -> list[Vec2]:
    i, j = p
    return [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]


def num_connected(ps: set[Vec2]) -> int:
    result = 0
    for p in ps:
        if any(map(lambda n: n in ps, neighbors_4_naive(p))):
            result += 1

    return result


input = list(map(extract_pos_vel, map(str.rstrip, fileinput.input())))

bound_x = 101
bound_y = 103

i = 0
while True:
    points: set[Vec2] = set()
    for line in input:
        p, v = line
        npx, npy = sum_scaled(p, v, (1, i))
        npx = npx % bound_x
        npy = npy % bound_y
        points.add((npx, npy))

    nc = num_connected(points)
    if nc > len(input) // 2:
        print(i)
        break

    i += 1
