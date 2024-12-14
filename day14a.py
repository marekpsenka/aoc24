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


input = map(extract_pos_vel, map(str.rstrip, fileinput.input()))

bound_x = 101
bound_y = 103

robots_pp = 0
robots_pm = 0
robots_mm = 0
robots_mp = 0


for line in input:
    p, v = line
    npx, npy = sum_scaled(p, v, (1, 100))
    npx = npx % bound_x
    npy = npy % bound_y

    if npx < bound_x // 2:
        if npy < bound_y // 2:
            robots_mm += 1
        elif npy > bound_y // 2:
            robots_mp += 1
    elif npx > bound_x // 2:
        if npy < bound_y // 2:
            robots_pm += 1
        elif npy > bound_y // 2:
            robots_pp += 1

print(robots_mp * robots_mm * robots_pm * robots_pp)
