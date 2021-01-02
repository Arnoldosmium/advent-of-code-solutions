# -*- coding: utf-8 -*-
from typing import List, Union
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from .common import int_code_runner

"""
2019 day 2
Boring recap: 
Arnold's difficulty eval:
1 - 
2 - 
"""


@inject_raw_input(2019, 2)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, ",").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


@print_return_value
def solve_part_1(nums: List[int]):
    payload = [nums[0]] + [12, 2] + nums[3:]
    ram, _ = int_code_runner(payload)
    return ram[0]


@print_return_value
def solve_part_2(nums: List[int]):
    for noun in range(100):
        for verb in range(100):
            payload = [nums[0]] + [noun, verb] + nums[3:]
            if int_code_runner(payload)[0][0] == 19690720:
                return 100 * noun + verb

    raise ValueError("Can't achieve 19690720")
