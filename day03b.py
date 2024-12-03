import fileinput
from re import finditer, Match

input = map(str.rstrip, fileinput.input())
result = 0


def mul(m: Match) -> int:
    return int(m.group(1)) * int(m.group(2))


active = True
for line in input:
    all_matches: list[Match] = [
        m
        for m in finditer(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)", line)
    ]

    for m in all_matches:
        if m.group(0).startswith("do()"):
            active = True
        elif m.group(0).startswith("don't()"):
            active = False
        elif m.group(0).startswith("mul") and active:
            result += mul(m)

print(result)
