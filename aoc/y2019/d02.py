# -*- coding: utf-8 -*-
"""
2019 day 2
Boring recap: Basic CPU and RAM simulation
Arnold's difficulty eval:
1 - Easy
2 - Easy
"""
from typing import List, Union
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from .common import IntCodeRunner


@inject_raw_input(2019, 2)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, ",").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


@print_return_value
def solve_part_1(nums: List[int]):
    payload = [nums[0]] + [12, 2] + nums[3:]
    code_runner = IntCodeRunner(payload)
    code_runner.run()
    return code_runner.ram[0]


@print_return_value
def solve_part_2(nums: List[int]):
    for noun in range(100):
        for verb in range(100):
            payload = [nums[0]] + [noun, verb] + nums[3:]
            code_runner = IntCodeRunner(payload)
            code_runner.run()
            if code_runner.ram[0] == 19690720:
                return 100 * noun + verb

    raise ValueError("Can't achieve target 19690720")
