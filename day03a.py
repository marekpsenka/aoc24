import fileinput
from re import finditer, Match

input = map(str.rstrip, fileinput.input())
result = 0


def mul(m: Match) -> int:
    return int(m.group(1)) * int(m.group(2))


for line in input:
    result += sum(map(mul, finditer(r"mul\((\d{1,3}),(\d{1,3})\)", line)))

print(result)
