import fileinput
from collections import defaultdict
from dataclasses import dataclass
from collections import deque

input = map(str.rstrip, fileinput.input())

connections: defaultdict[str, set[str]] = defaultdict(set)

for line in input:
    left, right = line.split("-")
    connections[left].add(right)
    connections[right].add(left)


@dataclass
class State:
    clique: list[str]
    candidate: str


def gen_key(ss: list[str]) -> str:
    return ",".join(sorted(ss))


visited: set[str] = set()

max_clique: list[str] = list()
for c1, cons in connections.items():
    q: deque[State] = deque(State([c1], c2) for c2 in cons)
    while len(q) > 0:
        s = q.popleft()
        for_key = s.clique.copy()
        for_key.append(s.candidate)
        key = gen_key(for_key)
        if key in visited:
            continue
        else:
            visited.add(key)

        if not all(map(lambda c: s.candidate in connections[c], s.clique)):
            if len(s.clique) > len(max_clique):
                max_clique = s.clique
            continue

        for c in connections[s.candidate]:
            new_clique = s.clique.copy()
            new_clique.append(s.candidate)
            q.append(State(new_clique, c))

print(gen_key(max_clique))
