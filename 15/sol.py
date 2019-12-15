#!/usr/bin/env python3.7
import copy
import sys
from collections import defaultdict, deque

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


op_shift_num = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2]

op_arg = {
    1: 2,
    2: 2,
    3: 0,
    7: 2,
    8: 2,
}


def run_prog(memory, direction):
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
            program[first] = direction
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


memory = Memory()
NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

visited = set()
to_visit = deque([(0, 0, copy.deepcopy(memory))])

dxdy = {NORTH: (0, 1), SOUTH: (0, -1), WEST: (-1, 0), EAST: (1, 0)}

steps = 0
steps_to_oxygen = 0
oxygen_at = None

while True:
    size = len(to_visit)
    if size == 0:
        break
    steps += 1
    for _ in range(size):
        x, y, state = to_visit.popleft()
        visited.add((x, y))
        for direction in (NORTH, SOUTH, WEST, EAST):
            newmemory = copy.deepcopy(state)
            status, should_stop = run_prog(newmemory, direction)
            if should_stop:
                break
            if status == 0:
                continue
            dx, dy = dxdy[direction]
            newx, newy = x + dx, y + dy
            if (newx, newy) in visited:
                continue
            if status == 2:
                steps_to_oxygen = steps
                oxygen_at = (newx, newy)
            to_visit.append((newx, newy, newmemory))

print(f"oxygen system is at {oxygen_at}, step {steps_to_oxygen}")  # part 1

# part 2
reachable = visited
visited = set()
to_visit = deque([oxygen_at])
steps = -1  # no need to fill location of oxygen system
while True:
    size = len(to_visit)
    if size == 0:
        break
    for _ in range(size):
        x, y = to_visit.popleft()
        visited.add((x, y))
        for direction in (NORTH, SOUTH, WEST, EAST):
            dx, dy = dxdy[direction]
            newx, newy = x + dx, y + dy
            if (newx, newy) not in reachable:
                continue
            if (newx, newy) in visited:
                continue
            to_visit.append((newx, newy))
    steps += 1

print(f"It takes {steps} minutes to fill all area")  # part 2
