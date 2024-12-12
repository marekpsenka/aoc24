import fileinput

input = list(map(list, map(str.rstrip, fileinput.input())))


Point = tuple[int, int]


def within_bounds(p: Point, max_i: int, max_j: int) -> bool:
    i, j = p
    if i < 0:
        return False
    elif i >= max_i:
        return False
    elif j < 0:
        return False
    elif j >= max_j:
        return False
    else:
        return True


def neighbors_4_naive(p: Point) -> list[Point]:
    i, j = p
    return [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]


def search(input: list[list[str]], start: Point) -> set[Point]:
    visited: set[Point] = set()
    queue: list[Point] = [start]
    bound_i = len(input)
    bound_j = len(input[0])
    region = input[start[0]][start[1]]

    while len(queue) > 0:
        current = queue.pop()
        visited.add(current)
        for n in neighbors_4_naive(current):
            if not within_bounds(n, bound_i, bound_j):
                continue
            if n in visited:
                continue
            if input[n[0]][n[1]] != region:
                continue
            queue.append(n)

    return visited


def components(input: list[list[str]]) -> dict[int, set[Point]]:
    bound_i = len(input)
    bound_j = len(input[0])
    visited: set[Point] = set()
    components: dict[int, set[Point]] = dict()
    free_id = 0

    for i in range(bound_i):
        for j in range(bound_j):
            if (i, j) in visited:
                continue

            search_result = search(input, (i, j))
            visited = visited.union(search_result)
            components[free_id] = search_result
            free_id += 1

    return components


cs = components(input)

total_price = 0
for _, plots in cs.items():
    perimeter = 0
    for plot in plots:
        for n in neighbors_4_naive(plot):
            if n not in plots:
                perimeter += 1

    total_price += perimeter * len(plots)


print(total_price)
