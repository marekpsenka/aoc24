import fileinput

input = map(str.rstrip, fileinput.input())


def f(test: int, current: int, i: int, numbers: list[int]) -> int:
    if current > test:
        return 0

    if i == len(numbers):
        if test == current:
            return 1
        else:
            return 0
    else:
        return (
            f(test, current + numbers[i], i + 1, numbers)
            + f(test, current * numbers[i], i + 1, numbers)
            + f(test, int(str(current) + str(numbers[i])), i + 1, numbers)
        )


total = 0

for line in input:
    test_str, numbers_str = line.split(": ")
    numbers = list(map(int, numbers_str.split()))
    test = int(test_str)
    if f(test, numbers[0], 1, numbers) > 0:
        total += test

print(total)
