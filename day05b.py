import fileinput
from itertools import takewhile


def parse_pair(s: str) -> tuple[int, int]:
    left_str, right_str = s.split("|")
    return (int(left_str), int(right_str))


input = map(str.rstrip, fileinput.input())

ordering = set(map(parse_pair, takewhile(lambda line: line, input)))


def are_ordered(pages: list[int]) -> bool:
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            if (pages[j], pages[i]) in ordering:
                return False
    return True


def sort(pages: list[int]):
    while True:
        swapped = False
        for i in range(len(pages) - 1):
            if (pages[i + 1], pages[i]) in ordering:
                temp = pages[i]
                pages[i] = pages[i + 1]
                pages[i + 1] = temp
                swapped = True

        if not swapped:
            break


result = 0
for line in input:
    pages = list(map(int, line.split(",")))
    if are_ordered(pages):
        continue
    else:
        sort(pages)
        result += pages[len(pages) // 2]

print(result)
