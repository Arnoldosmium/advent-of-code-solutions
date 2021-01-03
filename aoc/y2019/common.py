# -*- coding: utf-8 -*-
from typing import List, Tuple


class IntCodeRunner:
    def __init__(self, payload: List[int]):
        self.ram = list(payload)
        self.pc = 0     # program counter
        self.input_buffer = []

    @staticmethod
    def of(payload: List[int], inputs: List[int] = []):
        runner = IntCodeRunner(payload)
        runner.append_input(*inputs)
        return runner

    def append_input(self, *inputs: int):
        for num in inputs:
            self.input_buffer.append(num)

    def outputs(self):
        while self.ram[self.pc] != 99:
            operation = self.ram[self.pc] % 100
            if operation in {1, 2, 7, 8}:
                left, right, to = self.ram[self.pc + 1: self.pc + 4]
                left_mode, right_mode, to_mode = [(self.ram[self.pc] // x) % 10 for x in (100, 1000, 10000)]

                if left_mode == 0:
                    left = self.ram[left]
                elif left_mode == 1:
                    pass  # use number literal
                else:
                    raise ValueError("Unknown instruction for parameter 1: %s" % self.ram[self.pc])

                if right_mode == 0:
                    right = self.ram[right]
                elif right_mode == 1:
                    pass
                else:
                    raise ValueError("Unknown instruction for parameter 2: %s" % self.ram[self.pc])

                if to_mode == 0:
                    if operation == 1:
                        self.ram[to] = left + right
                    elif operation == 2:
                        self.ram[to] = left * right
                    elif operation == 7:
                        self.ram[to] = int(left < right)
                    elif operation == 8:
                        self.ram[to] = int(left == right)
                else:
                    raise ValueError("Unknown instruction for parameter 3: %s" % self.ram[self.pc])

                self.pc += 4
            elif operation == 3:
                to = self.ram[self.pc + 1]
                self.ram[to] = self.input_buffer.pop(0)
                self.pc += 2
            elif operation == 4:
                src = self.ram[self.pc + 1]
                yield self.ram[src]
                self.pc += 2
            elif operation in {5, 6}:
                val, to = self.ram[self.pc + 1: self.pc + 3]
                val_mode, to_mode = [(self.ram[self.pc] // x) % 10 for x in (100, 1000)]
                if val_mode == 0:
                    val = self.ram[val]
                elif val_mode == 1:
                    pass
                else:
                    raise ValueError("Unknown instruction for parameter 1: %s" % self.ram[self.pc])

                if to_mode == 0:
                    to = self.ram[to]
                elif to_mode == 1:
                    pass
                else:
                    raise ValueError("Unknown instruction for parameter 2: %s" % self.ram[self.pc])

                if (operation == 5 and val != 0) or (operation == 6 and val == 0):
                    self.pc = to
                else:
                    self.pc += 3
            else:
                raise ValueError("Unknown operation: %d" % operation)

    def run(self) -> List[int]:
        return list(self.outputs())
