# -*- coding: utf-8 -*-
"""
2019 day 5
Boring recap: Basic 10-based CPU and RAM simulation with bit extraction and jumps
Arnold's difficulty eval:
1 - Easy
2 - Easy
"""
from typing import List, Union
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from .common import IntCodeRunner


@inject_raw_input(2019, 5)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, ",").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


@print_return_value
def solve_part_1(payload: List[int]):
    outputs = IntCodeRunner.of(payload, [1]).run()
    print(outputs)
    return outputs[-1]


@print_return_value
def solve_part_2(payload: List[int]):
    outputs = IntCodeRunner.of(payload, [5]).run()
    print(outputs)
    return outputs[-1]
