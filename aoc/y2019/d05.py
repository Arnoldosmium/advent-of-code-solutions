# -*- coding: utf-8 -*-
from typing import List, Union
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from .common import int_code_runner

"""
2019 day 5
Boring recap: 
Arnold's difficulty eval:
1 - 
2 - 
"""


@inject_raw_input(2019, 5)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, ",").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


@print_return_value
def solve_part_1(payload: List[int]):
    _, outputs = int_code_runner(payload, [1])
    print(outputs)
    return outputs[-1]


@print_return_value
def solve_part_2(payload: List[int]):
    _, outputs = int_code_runner(payload, [5])
    print(outputs)
    return outputs[-1]
