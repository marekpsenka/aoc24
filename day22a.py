import fileinput

input = map(str.rstrip, fileinput.input())

total = 0
for line in input:
    secret = int(line)
    for _ in range(2000):
        secret = (secret * 64) ^ secret
        secret = secret % 16777216
        secret = (secret // 32) ^ secret
        secret = secret % 16777216
        secret = (secret * 2048) ^ secret
        secret = secret % 16777216

    total += secret

print(total)
