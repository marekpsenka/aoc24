import fileinput

input = map(str.rstrip, fileinput.input())

safe_count = 0

for line in input:
    levels = list(map(int, line.split()))
    safe_increasing = True
    for i in range(len(levels) - 1):
        diff = levels[i + 1] - levels[i]
        if diff < 1 or diff > 3:
            safe_increasing = False
            break

    safe_decreasing = True
    for i in range(len(levels) - 1):
        diff = levels[i] - levels[i + 1]
        if diff < 1 or diff > 3:
            safe_decreasing = False
            break

    if safe_increasing or safe_decreasing:
        safe_count += 1

print(safe_count)
