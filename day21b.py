import fileinput
from collections import Counter

input = map(str.rstrip, fileinput.input())

Point = tuple[int, int]

# fmt: off
large_kp = {"7": (0, 0), "8": (0, 1), "9": (0, 2), "4": (1, 0), "5": (1, 1),
            "6": (1, 2), "1": (2, 0), "2": (2, 1), "3": (2, 2), "m": (3, 0),
            "0": (3, 1), "A": (3, 2)}

small_kp = {"m": (0, 0), "^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1),
            ">": (1, 2)}
# fmt: on


def find_path(p1: Point, p2: Point, m: Point) -> str:
    if p1 == p2:
        return "A"
    ud = (p2[0] - p1[0]) * "v" if p2[0] > p1[0] else (p1[0] - p2[0]) * "^"
    lr = (p2[1] - p1[1]) * ">" if p2[1] > p1[1] else (p1[1] - p2[1]) * "<"

    if p2[1] < p1[1]:
        if p1[0] == m[0] and p2[1] == m[1]:
            return f"{ud}{lr}A"
        else:
            return f"{lr}{ud}A"
    elif p2[1] > p1[1]:
        if p2[0] == m[0] and p1[1] == m[1]:
            return f"{lr}{ud}A"
        else:
            return f"{ud}{lr}A"

    return f"{lr}{ud}A"


def expand(kp: dict[str, Point], s: str) -> list[str]:
    result = []
    prev = "A"
    for c in s:
        result.append(find_path(kp[prev], kp[c], kp["m"]))
        prev = c

    return result


total = 0
for line in input:
    counts = Counter(expand(large_kp, line))
    for _ in range(25):
        new_counts: Counter[str] = Counter()
        for seq, count in counts.items():
            subseqs = expand(small_kp, seq)
            for subseq in subseqs:
                new_counts[subseq] += count
        counts = new_counts

    sequence_length = sum(map(lambda p: len(p[0]) * p[1], counts.items()))
    numeric_part = int("".join(c for c in line if c.isdigit()))
    total += sequence_length * numeric_part

print(total)
