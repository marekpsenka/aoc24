import fileinput
from dataclasses import dataclass

input = map(str.rstrip, fileinput.input())
towels: set[str] = set(next(input).split(", "))
assert not next(input)


@dataclass
class State:
    consumed: int


def is_possible(pattern: str) -> bool:
    q: list[State] = [State(0)]
    while len(q) > 0:
        s = q.pop()
        if s.consumed == len(pattern) - 1:
            return True
        i = s.consumed
        while i < len(pattern):
            if pattern[s.consumed : i] in towels:
                q.append(State(i))
            i += 1

    return False


possible = 0
for line in input:
    if is_possible(line):
        possible += 1

print(possible)
