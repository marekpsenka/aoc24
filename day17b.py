import fileinput
from itertools import takewhile
from dataclasses import dataclass
from typing import ClassVar, Callable


def read_register(s: str) -> int:
    _, num_str = s.split(": ")
    return int(num_str)


def read_program(s: str) -> list[int]:
    _, program_str = s.split(": ")
    return list(map(int, program_str.split(",")))


@dataclass
class Computer:
    a: int
    b: int
    c: int
    ptr: int
    program: list[int]
    output: list[int]

    def halted(self) -> bool:
        return self.ptr >= len(program)

    def read_combo(self) -> int:
        oper_in = program[self.ptr + 1]
        if oper_in <= 3:
            return oper_in
        match oper_in:
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise RuntimeError

    def read_literal(self) -> int:
        return program[self.ptr + 1]

    def adv(self) -> None:
        self.a = int(self.a / 2 ** self.read_combo())
        self.ptr += 2

    def bxl(self) -> None:
        self.b = self.b ^ self.read_literal()
        self.ptr += 2

    def bst(self) -> None:
        self.b = self.read_combo() % 8
        self.ptr += 2

    def jnz(self) -> None:
        if self.a == 0:
            self.ptr += 2
            return

        self.ptr = self.read_literal()

    def bxc(self) -> None:
        self.b = self.b ^ self.c
        self.ptr += 2

    def out(self) -> None:
        self.output.append(self.read_combo() % 8)
        self.ptr += 2

    def bdv(self) -> None:
        self.b = int(self.a / 2 ** self.read_combo())
        self.ptr += 2

    def cdv(self) -> None:
        self.c = int(self.a / 2 ** self.read_combo())
        self.ptr += 2

    ops: ClassVar[list[Callable[["Computer"], None]]] = [
        adv,
        bxl,
        bst,
        jnz,
        bxc,
        out,
        bdv,
        cdv,
    ]

    def execute(self) -> None:
        self.ops[self.program[self.ptr]](self)


input = map(str.rstrip, fileinput.input())

a, b, c = map(read_register, takewhile(lambda line: line, input))
program = read_program(next(input))

output_cache: list[int] = [0] * 1024

for i in range(1024):
    computer = Computer(i, 0, 0, 0, program, [])
    while not computer.halted():
        computer.execute()

    assert len(computer.output) > 0
    output_cache[i] = computer.output[0]


@dataclass
class State:
    hot: int
    shifted_out: list[int]
    idx_output: int


def evaluate(triplets: list[int]) -> int:
    result = 0
    for i in range(len(triplets)):
        result = result << 3 | triplets[len(triplets) - 1 - i]

    return result


candidates: set[int] = set()
queue: list[State] = [State(i, [], 0) for i in range(128)]
while len(queue) > 0:
    state = queue.pop()
    if state.idx_output == len(program):
        candidates.add(
            state.hot << (len(state.shifted_out) * 3)
            | evaluate(state.shifted_out)
        )
        continue
    for i in range(8):
        assert state.hot < 128
        k = i << 7 | state.hot
        if program[state.idx_output] == output_cache[k]:
            next_shifted_out = state.shifted_out.copy()
            next_shifted_out.append(k % 8)
            queue.append(
                State(
                    k >> 3,
                    next_shifted_out,
                    state.idx_output + 1,
                )
            )
        else:
            continue

print(min(candidates))
