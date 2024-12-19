import fileinput

input = map(str.rstrip, fileinput.input())
towels: set[str] = set(next(input).split(", "))
assert not next(input)

cache: dict[str, int] = dict()


def possibilities(pattern: str) -> int:
    if not pattern:
        return 1

    if pattern in cache:
        return cache[pattern]

    result = 0
    for i in range(1, len(pattern) + 1):
        if pattern[:i] in towels:
            result += possibilities(pattern[i:])

    assert pattern not in cache
    cache[pattern] = result
    return result


total_possibilities = 0
for line in input:
    total_possibilities += possibilities(line)

print(total_possibilities)
