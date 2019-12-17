#!/usr/bin/env python3

import sys
from collections import deque

prog = list(map(int, open(sys.argv[1]).read().strip("\n").split(",")))


class Memory:
    def __init__(self):
        self.reset()

    def reset(self):
        self.program = prog.copy() + [0] * 10000
        self.inited = False
        self.pc = 0
        self.output = 0
        self.offset = 0


op_shift_num = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2]

op_arg = {
    1: 2,
    2: 2,
    3: 0,
    7: 2,
    8: 2,
}


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

    while memory.pc < len(program):
        code = program[memory.pc]
        op, modes = _parse_code(code)
        first, second, outpos = _get_params(modes, memory.pc + 1)
        if op == 1:
            program[outpos] = first + second
        elif op == 2:
            program[outpos] = first * second
        elif op == 3:
            program[first] = msg.popleft()
        elif op == 4:
            memory.pc += op_shift_num[op]
            memory.output = first
            return memory.output, False
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
            return None, True
        memory.pc += op_shift_num[op]


x = y = 0
memory = Memory()
scaffold = set()
robot = None
direction = None
msg = deque()

while True:
    output, should_stop = run_prog()
    if should_stop:
        break
    if output == 10:
        y += 1
        x = -1
    elif output == 35:
        scaffold.add((x, y))
    elif output == 46:
        pass
    else:
        robot = (x, y)
        direction = output
    x += 1


def is_intersection(s):
    x, y = s[0], s[1]
    if (
        (x - 1, y) in scaffold
        and (x + 1, y) in scaffold
        and (x, y - 1) in scaffold
        and (x, y + 1) in scaffold
    ):
        return True
    return False


# part 1
param = 0
for s in scaffold:
    if is_intersection(s):
        param += s[0] * s[1]

print(param)
