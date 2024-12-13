import fileinput
from more_itertools import split_at
from re import search

input = split_at(map(str.rstrip, fileinput.input()), lambda line: not line)

Vec2 = tuple[int, int]


def extract_tuple(s: str) -> Vec2:
    m = search(r"X[\+\=](\d+), Y[\+\=](\d+)", s)
    assert m is not None
    return (int(m.group(1)), int(m.group(2)))


def sum(v: Vec2, w: Vec2) -> Vec2:
    return (v[0] + w[0], v[1] + w[1])


def cost(s: Vec2) -> int:
    return 3 * s[0] + s[1]


def solve(a: Vec2, b: Vec2, p: Vec2) -> Vec2:
    num = p[1] - (p[0] * b[1]) / b[0]
    den = a[1] - (b[1] * a[0]) / b[0]

    x = num / den

    num2 = p[0] - a[0] * x

    return (round(x), round(num2 / b[0]))


total_tokens = 0
for triple in input:
    a, b, prize = map(extract_tuple, triple)
    solution = solve(a, b, prize)
    if (
        a[0] * solution[0] + b[0] * solution[1] == prize[0]
        and a[1] * solution[0] + b[1] * solution[1] == prize[1]
    ):
        total_tokens += cost(solution)

print(total_tokens)
