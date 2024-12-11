import fileinput
from collections import defaultdict

input = map(str.rstrip, fileinput.input())

stones: defaultdict[int, int] = defaultdict(int)

for mark_str in next(input).split():
    stones[int(mark_str)] = 1


for _ in range(25):
    next_stones: defaultdict[int, int] = defaultdict(int)
    for mark, count in stones.items():
        mark_str = str(mark)
        if mark == 0:
            next_stones[1] += count
        elif len(mark_str) % 2 == 0:
            next_stones[int(mark_str[0 : len(mark_str) // 2])] += count
            next_stones[int(mark_str[len(mark_str) // 2 :])] += count
        else:
            next_stones[mark * 2024] += count

    stones = next_stones

print(sum(stones.values()))
