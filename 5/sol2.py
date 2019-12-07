#!/usr/bin/env python3

data = list(map(int, open("input").read().strip("\n").split(",")))
assert data[0] == 3
data[data[1]] = 5  # input ID 5


def _parse_code(code):
    code = str(code)
    code = "0" * (5 - len(code)) + code
    op = int(code[-2:])
    modes = list(reversed(code[:-2]))
    modes[-1] = "1"  # output position should always in immediate mode
    if op == 3:
        modes[0] = "1"
    return op, modes


def get_params(modes, start_pos, number=3):
    res = []
    for mode, index in zip(modes, range(start_pos, start_pos + number)):
        try:
            res.append(data[index] if mode == "1" else data[data[index]])
        except IndexError:
            res.append(0)  # dummy data
    return res


op_shift_num = [0, 4, 4, 2, 2, 3, 3, 4, 4]
i = 2
while i < len(data):
    code = data[i]
    op, modes = _parse_code(code)
    first, second, outpos = get_params(modes, i + 1)
    if op == 1:
        data[outpos] = first + second
    elif op == 2:
        data[outpos] = first * second
    elif op == 3:
        raise RuntimeError("no input given")
    elif op == 4:
        print(first)
    elif op == 5:
        if first != 0:
            i = second - op_shift_num[op]
    elif op == 6:
        if first == 0:
            i = second - op_shift_num[op]
    elif op == 7:
        data[outpos] = 1 if first < second else 0
    elif op == 8:
        data[outpos] = 1 if first == second else 0
    else:
        assert op == 99
        break
    i += op_shift_num[op]
