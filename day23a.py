import fileinput
from collections import defaultdict

input = map(str.rstrip, fileinput.input())

connections: defaultdict[str, set[str]] = defaultdict(set)

for line in input:
    left, right = line.split("-")
    connections[left].add(right)
    connections[right].add(left)

result: set[tuple[str, str, str]] = set()


def stupid_sort(c1: str, c2: str, c3: str) -> tuple[str, str, str]:
    temp = [c1, c2, c3]
    r1, r2, r3 = sorted(temp)
    return (r1, r2, r3)


for c1, cons in connections.items():
    for c2 in cons:
        for c3 in cons.intersection(connections[c2]):
            if not any(map(lambda c: c.startswith("t"), [c1, c2, c3])):
                continue
            triple = stupid_sort(c1, c2, c3)
            if triple not in result:
                result.add(triple)

print(len(result))
