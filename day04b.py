import fileinput
from more_itertools import ilen
from re import finditer

input = map(str.rstrip, fileinput.input())

occurences = 0


def has_xmas(i: int, j: int) -> bool:
    mas1 = (chars[i - 1][j - 1] == "M" and chars[i + 1][j + 1] == "S") or (
        chars[i - 1][j - 1] == "S" and chars[i + 1][j + 1] == "M"
    )
    mas2 = (chars[i + 1][j - 1] == "M" and chars[i - 1][j + 1] == "S") or (
        chars[i + 1][j - 1] == "S" and chars[i - 1][j + 1] == "M"
    )
    return chars[i][j] == "A" and mas1 and mas2


chars = [[c for c in string] for string in input]
for i in range(1, len(chars) - 1):
    for j in range(1, len(chars) - 1):
        if has_xmas(i, j):
            occurences += 1

print(occurences)
