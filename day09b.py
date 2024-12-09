import fileinput


input = map(str.rstrip, fileinput.input())

files: list[tuple[int, int]] = list()
spaces: list[tuple[int, int]] = list()

pos = 0
for i, c in enumerate(next(input)):
    size = int(c)
    if i % 2 == 0:
        files.append((pos, size))
    else:
        spaces.append((pos, size))
    pos += size

checksum = 0
while len(files) > 0:
    file_loc, file_size = files.pop()
    space_found = False
    for i in range(len(spaces)):
        space_loc, space_size = spaces[i]
        if space_loc > file_loc:
            break
        if space_size >= file_size:
            pos = space_loc
            for _ in range(file_size):
                checksum += pos * len(files)
                pos += 1
            space_found = True
            spaces[i] = (pos, space_size - file_size)
            break
    if not space_found:
        pos = file_loc
        for _ in range(file_size):
            checksum += pos * len(files)
            pos += 1


print(checksum)
