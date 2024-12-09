import fileinput
from collections import deque

input = map(str.rstrip, fileinput.input())

files: deque[int] = deque()
spaces: list[int] = list()

for i, c in enumerate(next(input)):
    if i % 2 == 0:
        files.append(int(c))
    else:
        spaces.append(int(c))

spaces.reverse()

checksum = 0
file_index = 0
pos = 0
while len(files) > 0:
    for _ in range(files.popleft()):
        checksum += pos * file_index
        pos += 1

    to_fill = spaces.pop()
    while to_fill > 0 and len(files) > 0:
        file_size = files.pop()
        if to_fill >= file_size:
            for _ in range(file_size):
                checksum += pos * (len(files) + 1 + file_index)
                pos += 1
            to_fill -= file_size
        else:  # to_fill < file_size
            for _ in range(to_fill):
                checksum += pos * (len(files) + 1 + file_index)
                pos += 1
            files.append(file_size - to_fill)
            to_fill = 0
    file_index += 1

print(checksum)
