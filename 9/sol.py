#!/usr/bin/env python3
import sys

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


def run_prog(input_signal):
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
            if not memory.inited:
                program[first] = input_signal
                memory.inited = True
            else:
                raise ValueError("duplicate input command")
        elif op == 4:
            print(first)
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
            break
        memory.pc += op_shift_num[op]


run_prog(input_signal=1)  # part 1
memory.reset()
run_prog(input_signal=2)  # part 2
