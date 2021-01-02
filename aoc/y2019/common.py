# -*- coding: utf-8 -*-
from typing import List, Tuple


def int_code_runner(payload: List[int], inputs: List[int] = []) -> Tuple[List[int], List[int]]:
    ram = list(payload)
    pc = 0      # program counter
    outputs = []
    while ram[pc] != 99:
        operation = ram[pc] % 100
        if operation in {1, 2, 7, 8}:
            left, right, to = ram[pc + 1: pc + 4]
            left_mode, right_mode, to_mode = [(ram[pc] // x) % 10 for x in (100, 1000, 10000)]

            if left_mode == 0:
                left = ram[left]
            elif left_mode == 1:
                pass    # use number literal
            else:
                raise ValueError("Unknown instruction for parameter 1: %s" % ram[pc])

            if right_mode == 0:
                right = ram[right]
            elif right_mode == 1:
                pass
            else:
                raise ValueError("Unknown instruction for parameter 2: %s" % ram[pc])

            if to_mode == 0:
                if operation == 1:
                    ram[to] = left + right
                elif operation == 2:
                    ram[to] = left * right
                elif operation == 7:
                    ram[to] = int(left < right)
                elif operation == 8:
                    ram[to] = int(left == right)
            else:
                raise ValueError("Unknown instruction for parameter 3: %s" % ram[pc])

            pc += 4
        elif operation == 3:
            to = ram[pc + 1]
            ram[to] = inputs.pop(0)
            pc += 2
        elif operation == 4:
            src = ram[pc + 1]
            outputs.append(ram[src])
            pc += 2
        elif operation in {5, 6}:
            val, to = ram[pc + 1: pc + 3]
            val_mode, to_mode = [(ram[pc] // x) % 10 for x in (100, 1000)]
            if val_mode == 0:
                val = ram[val]
            elif val_mode == 1:
                pass
            else:
                raise ValueError("Unknown instruction for parameter 1: %s" % ram[pc])

            if to_mode == 0:
                to = ram[to]
            elif to_mode == 1:
                pass
            else:
                raise ValueError("Unknown instruction for parameter 2: %s" % ram[pc])

            if (operation == 5 and val != 0) or (operation == 6 and val == 0):
                pc = to
            else:
                pc += 3
        else:
            raise ValueError("Unknown operation: %d" % operation)

    return ram, outputs
