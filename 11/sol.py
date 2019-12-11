#!/usr/bin/env python3.7
import sys
from collections import namedtuple

from recordtype import recordtype

prog = list(map(int, open(sys.argv[1]).read().strip("\n").split(",")))


class Memory:
    def __init__(self):
        self.reset()

    def reset(self):
        self.program = prog.copy() + [0] * 1000
        self.inited = False
        self.pc = 0
        self.output = 0
        self.offset = 0


memory = Memory()


op_shift_num = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2]

op_arg = {
    1: 2,
    2: 2,
    3: 0,
    7: 2,
    8: 2,
}


Panel = namedtuple("Panel", "x y")
State = recordtype("State", "painted_num color")


def run_prog():
    program = memory.program

    def _parse_code(code):
        code = str(code)
        code = "0" * (5 - len(code)) + code
        op = int(code[-2:])
        modes = list(reversed(code[:-2]))
        return op, modes

    def _get_params(modes, start_pos, number=3):
        res = []
        for idx, (mode, index) in enumerate(
            zip(modes, range(start_pos, start_pos + number))
        ):
            try:
                if mode == "1":
                    pos = index
                elif mode == "0":
                    pos = program[index]
                else:
                    pos = program[index] + memory.offset
                if op_arg.get(op, -1) == idx:
                    res.append(pos)
                else:
                    res.append(program[pos])
            except IndexError:
                res.append(0)  # dummy data
        return res

    output = []
    while memory.pc < len(program):
        code = program[memory.pc]
        op, modes = _parse_code(code)
        first, second, outpos = _get_params(modes, memory.pc + 1)
        if op == 1:
            program[outpos] = first + second
        elif op == 2:
            program[outpos] = first * second
        elif op == 3:
            g = grids[Panel(x, y)]
            program[first] = g.color
        elif op == 4:
            output.append(first)
            if len(output) == 2:
                memory.pc += op_shift_num[op]
                return output, False
        elif op == 5:
            if first != 0:
                memory.pc = second - op_shift_num[op]
        elif op == 6:
            if first == 0:
                memory.pc = second - op_shift_num[op]
        elif op == 7:
            program[outpos] = 1 if first < second else 0
        elif op == 8:
            program[outpos] = 1 if first == second else 0
        elif op == 9:
            memory.offset += first
        else:
            assert op == 99
            return [None, None], True
        memory.pc += op_shift_num[op]


x = y = 0
dx = 0
dy = 1
grids = {Panel(0, 0): State(0, 0)}

grids[(0, 0)] = State(0, 1)  # part 2

while True:
    (color, turn), should_stop = run_prog()
    if should_stop:
        break
    state = grids[Panel(x, y)]
    state.color = color
    state.painted_num += 1

    if turn == 0:
        dx, dy = -dy, dx
    else:
        dx, dy = dy, -dx
    x += dx
    y += dy
    p = Panel(x, y)
    if p not in grids:
        grids[p] = State(0, 0)

print(sum(s.painted_num > 0 for s in grids.values()))  # part 1

x_pos = [p.x for p in grids]
y_pos = [p.y for p in grids]
x_range = max(x_pos) - min(x_pos) + 1
y_range = max(y_pos) - min(y_pos) + 1

canvas = [[" "] * x_range for _ in range(y_range)]
for p, s in grids.items():
    if s.color == 1:
        canvas[-p.y][p.x] = "#"
print("\n".join(("".join(line) for line in canvas)))  # part 2
