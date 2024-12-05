import fileinput
from more_itertools import ilen
from re import finditer

input = list(map(str.rstrip, fileinput.input()))

occurences = 0
for line in input:
    occurences += ilen(finditer("XMAS", line))
    occurences += ilen(finditer("SAMX", line))


chars = [[c for c in string] for string in input]
transposed_chars = list(map(list, zip(*chars)))

for line in transposed_chars:
    occurences += ilen(finditer("XMAS", "".join(line)))
    occurences += ilen(finditer("SAMX", "".join(line)))

dim = len(chars[0])

pp_diagonals = [[chars[i][j - i] for i in range(j + 1)] for j in range(dim)]

for j in range(dim - 1):
    pp_diagonals.append(
        [chars[dim - j + i - 1][dim - i - 1] for i in range(j + 1)]
    )

for diagonal in pp_diagonals:
    occurences += ilen(finditer("XMAS", "".join(diagonal)))
    occurences += ilen(finditer("SAMX", "".join(diagonal)))

mp_diagonals = [
    [chars[i][dim - j + i - 1] for i in range(j + 1)] for j in range(dim)
]

for j in range(dim - 1):
    mp_diagonals.append([chars[dim - j + i - 1][i] for i in range(j + 1)])


for diagonal in mp_diagonals:
    occurences += ilen(finditer("XMAS", "".join(diagonal)))
    occurences += ilen(finditer("SAMX", "".join(diagonal)))

print(occurences)
