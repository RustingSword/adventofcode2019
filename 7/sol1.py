#!/usr/bin/env python3
import sys
from itertools import permutations

prog = list(map(int, open(sys.argv[1]).read().strip("\n").split(",")))


def run_prog(phase, input_signal):
    program = prog.copy()

    def _parse_code(code):
        code = str(code)
        code = "0" * (5 - len(code)) + code
        op = int(code[-2:])
        modes = list(reversed(code[:-2]))
        modes[-1] = "1"  # output position should always in immediate mode
        if op == 3:
            modes[0] = "1"  # first argument of op '3' is output pos
        return op, modes

    def _get_params(modes, start_pos, number=3):
        res = []
        for mode, index in zip(modes, range(start_pos, start_pos + number)):
            try:
                res.append(program[index] if mode == "1" else program[program[index]])
            except IndexError:
                res.append(0)  # dummy data
        return res

    assert program[0] == 3
    program[program[1]] = phase
    op_shift_num = [0, 4, 4, 2, 2, 3, 3, 4, 4]
    i = 2
    output = None
    while i < len(program):
        code = program[i]
        op, modes = _parse_code(code)
        first, second, outpos = _get_params(modes, i + 1)
        if op == 1:
            program[outpos] = first + second
        elif op == 2:
            program[outpos] = first * second
        elif op == 3:
            program[first] = input_signal
        elif op == 4:
            output = first
        elif op == 5:
            if first != 0:
                i = second - op_shift_num[op]
        elif op == 6:
            if first == 0:
                i = second - op_shift_num[op]
        elif op == 7:
            program[outpos] = 1 if first < second else 0
        elif op == 8:
            program[outpos] = 1 if first == second else 0
        else:
            assert op == 99
            break
        i += op_shift_num[op]
    return output


def find_max_output():
    max_thrust = 0
    for order in permutations(range(5)):
        input_signal = 0
        for index in order:
            input_signal = run_prog(index, input_signal)
        max_thrust = max(max_thrust, input_signal)
    print(max_thrust)


find_max_output()
