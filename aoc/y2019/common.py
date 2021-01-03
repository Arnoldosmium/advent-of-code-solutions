# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import List


class RAM:
    def __init__(self, payload: List[int]):
        self.payload = list(payload)
        self.extension = defaultdict(int)

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < len(self.payload):
                return self.payload[key]
            else:
                return self.extension[key]
        elif isinstance(key, slice):
            if key.step == 0:
                raise ValueError("Slice step cannot be 0")
            step = 1 if key.step is None else key.step
            if step < 0:
                return list(reversed(self[key.stop:key.start:-step]))
            start = key.start if key.start is not None else 0
            if key.stop is None:
                raise ValueError("Unlimited RAM need a literal stop index")
            stop = key.stop

            first_half = []
            if start < len(self.payload):
                if stop <= len(self.payload):
                    return self.payload[start:stop:step]
                first_half = self.payload[start::step]
                start = stop + (start - stop) % step

            if start >= stop:
                return first_half

            return first_half + [self[i] for i in range(start, stop, step)]
        elif isinstance(key, tuple):
            return [self[i] for i in key]
        else:
            raise ValueError("Unknown RAM address: %s" % key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key < len(self.payload):
                self.payload[key] = value
            else:
                self.extension[key] = value
        elif isinstance(key, slice):
            if key.step == 0:
                raise ValueError("Slice step cannot be 0")
            step = 1 if key.step is None else key.step
            if step < 0:
                self[key.stop:key.start:-step] = reversed(value)
                return
            start = key.start if key.start is not None else 0
            if key.stop is None:
                raise ValueError("Unlimited RAM need a literal stop index")
            stop = key.stop

            if start >= stop:
                return

            elem_count = 0
            if start < len(self.payload):
                elem_count = (stop - start) // step
                if stop <= len(self.payload):
                    self.payload[start:stop:step] = value[:elem_count]
                start = stop + (start - stop) % step

            for i, address in enumerate(range(start, stop, step)):
                self[address] = value[i + elem_count]
        elif isinstance(key, tuple):
            for k in key:
                self[k] = value
        else:
            raise ValueError("Unknown RAM address: %s" % key)


class IntCodeRunner:
    def __init__(self, payload: List[int]):
        self.ram = RAM(payload)
        self.pc = 0     # program counter
        self.rb = 0     # relative base
        self.input_buffer = []

    @staticmethod
    def of(payload: List[int], inputs: List[int] = []):
        runner = IntCodeRunner(payload)
        runner.append_input(*inputs)
        return runner

    def append_input(self, *inputs: int):
        for num in inputs:
            self.input_buffer.append(num)
        return self

    def read_with_mode(self, mode: int, argument: int):
        if mode == 0:
            return self.ram[argument]
        elif mode == 1:
            return argument
        elif mode == 2:
            return self.ram[self.rb + argument]
        else:
            raise ValueError("Unknown instruction for parameter: %s" % self.ram[self.pc])

    def write_with_mode(self, mode: int, argument: int, value: int):
        if mode == 0:
            self.ram[argument] = value
        elif mode == 1:
            raise ValueError("Cannot write to literal numbers: %s" % self.ram[self.pc])
        elif mode == 2:
            self.ram[self.rb + argument] = value
        else:
            raise ValueError("Unknown instruction for parameter: %s" % self.ram[self.pc])

    def outputs(self):
        while self.ram[self.pc] != 99:
            operation = self.ram[self.pc] % 100
            if operation in {1, 2, 7, 8}:
                left, right, to = self.ram[self.pc + 1: self.pc + 4]
                left_mode, right_mode, to_mode = [(self.ram[self.pc] // x) % 10 for x in (100, 1000, 10000)]

                left = self.read_with_mode(left_mode, left)
                right = self.read_with_mode(right_mode, right)

                if operation == 1:
                    to_value = left + right
                elif operation == 2:
                    to_value = left * right
                elif operation == 7:
                    to_value = int(left < right)
                elif operation == 8:
                    to_value = int(left == right)
                else:
                    raise ValueError("Unreachable branch reached.")

                self.write_with_mode(to_mode, to, to_value)

                self.pc += 4
            elif operation == 3:
                to = self.ram[self.pc + 1]
                to_mode = (self.ram[self.pc] // 100) % 10
                value = self.input_buffer.pop(0)
                self.write_with_mode(to_mode, to, value)

                self.pc += 2
            elif operation == 4:
                src = self.ram[self.pc + 1]
                src_mode = (self.ram[self.pc] // 100) % 10
                yield self.read_with_mode(src_mode, src)

                self.pc += 2
            elif operation in {5, 6}:
                val, to = self.ram[self.pc + 1: self.pc + 3]
                val_mode, to_mode = [(self.ram[self.pc] // x) % 10 for x in (100, 1000)]

                val = self.read_with_mode(val_mode, val)
                to = self.read_with_mode(to_mode, to)

                if (operation == 5 and val != 0) or (operation == 6 and val == 0):
                    self.pc = to
                else:
                    self.pc += 3
            elif operation == 9:
                diff = self.ram[self.pc + 1]
                diff_mode = (self.ram[self.pc] // 100) % 10
                self.rb += self.read_with_mode(diff_mode, diff)

                self.pc += 2
            else:
                raise ValueError("Unknown operation: %d" % operation)

    def run(self) -> List[int]:
        return list(self.outputs())
