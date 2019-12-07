#!/usr/bin/env python3
import sys
from itertools import permutations

prog = list(map(int, open(sys.argv[1]).read().strip("\n").split(",")))


class Memory:
    def __init__(self):
        self.reset()

    def reset(self):
        self.program = prog.copy()
        self.inited = False
        self.pc = 0
        self.output = 0


memories = [Memory() for _ in range(5)]


def run_prog(amplifier_id, phase, input_signal):
    memory = memories[amplifier_id]
    program = memory.program

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

    op_shift_num = [0, 4, 4, 2, 2, 3, 3, 4, 4]
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
                program[first] = phase
                memory.inited = True
            else:
                program[first] = input_signal
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
        else:
            assert op == 99
            return 0, True
        memory.pc += op_shift_num[op]
    return memory.output, False


def find_max_thrust():
    best_phase_order = None
    max_thrust = 0
    for phase_order in permutations(range(5, 10)):
        input_signal = 0
        should_stop = False
        for i in range(5):
            memories[i].reset()
        while not should_stop:
            for amplifier_id, phase in enumerate(phase_order):
                input_signal, should_stop = run_prog(amplifier_id, phase, input_signal)
        if memories[4].output > max_thrust:
            max_thrust = memories[4].output
            best_phase_order = phase_order
    print(max_thrust, best_phase_order)


find_max_thrust()
