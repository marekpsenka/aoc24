import fileinput
from itertools import takewhile
from dataclasses import dataclass

input = map(str.rstrip, fileinput.input())


@dataclass
class Gate:
    left: str
    right: str
    op: str


def parse_input(s: str) -> tuple[str, bool]:
    name, value = s.split(": ")
    return (name, True if value == "1" else False)


def parse_gate(s: str) -> tuple[str, Gate]:
    defn, out = s.split(" -> ")
    left, op, right = defn.split()
    return (out, Gate(left, right, op))


known: dict[str, bool] = dict(
    map(parse_input, takewhile(lambda line: line, input))
)

gates: dict[str, Gate] = dict(map(parse_gate, input))


def evaluate(name: str) -> bool:
    if name in known:
        return known[name]
    gate = gates.get(name)
    assert gate is not None

    left_value = evaluate(gate.left)
    right_value = evaluate(gate.right)
    match gate.op:
        case "OR":
            return left_value or right_value
        case "AND":
            return left_value and right_value
        case "XOR":
            return left_value ^ right_value
        case _:
            raise RuntimeError


result = 0
for i, output_wire in enumerate(
    sorted(filter(lambda name: name.startswith("z"), gates.keys()))
):
    if evaluate(output_wire):
        result += 1 << i

print(result)
