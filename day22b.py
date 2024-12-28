import fileinput
from collections import defaultdict

input = map(str.rstrip, fileinput.input())


def ones_digit(n: int) -> int:
    return int(str(n)[-1])


bananas: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
total = 0
for line in input:
    secret = int(line)
    last_digit = ones_digit(secret)
    data: list[tuple[int, int]] = []
    for _ in range(2000):
        secret = (secret * 64) ^ secret
        secret = secret % 16777216
        secret = (secret // 32) ^ secret
        secret = secret % 16777216
        secret = (secret * 2048) ^ secret
        secret = secret % 16777216
        digit = ones_digit(secret)
        data.append((digit, digit - last_digit))
        last_digit = digit

    seen: set[tuple[int, int, int, int]] = set()
    for i in range(3, 2000):
        this_tuple = (
            data[i - 3][1],
            data[i - 2][1],
            data[i - 1][1],
            data[i][1],
        )
        if this_tuple in seen:
            continue
        seen.add(this_tuple)
        bananas[this_tuple] += data[i][0]


print(max(bananas.values()))
