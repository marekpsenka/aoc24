import fileinput


def parse_pairs(line: str) -> tuple[int, int]:
    first_str, second_str = line.split()
    return (int(first_str), int(second_str))


input = map(parse_pairs, map(str.rstrip, fileinput.input()))

left, right = zip(*input)

matched = zip(sorted(left), sorted(right))
diffs = map(lambda p: abs(p[0] - p[1]), matched)

print(sum(diffs))
