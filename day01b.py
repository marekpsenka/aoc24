import fileinput
from collections import Counter


def parse_pairs(line: str) -> tuple[int, int]:
    first_str, second_str = line.split()
    return (int(first_str), int(second_str))


input = map(parse_pairs, map(str.rstrip, fileinput.input()))

left, right = zip(*input)
counts = Counter(right)

scores = map(lambda n: n * counts[n], left)

print(sum(scores))
