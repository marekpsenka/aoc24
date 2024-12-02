import fileinput

input = map(str.rstrip, fileinput.input())

safe_count = 0


def check_safe(levels: list[int]) -> bool:
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

    return safe_increasing or safe_decreasing


for line in input:
    levels = list(map(int, line.split()))
    if check_safe(levels):
        safe_count += 1
    else:
        for i in range(len(levels)):
            levels_copy = levels.copy()
            levels_copy.pop(i)
            if check_safe(levels_copy):
                safe_count += 1
                break


print(safe_count)
