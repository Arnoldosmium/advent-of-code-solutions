# -*- coding: utf-8 -*-
"""
2019 day 9
Boring recap: Unlimited RAM and address pointer simulation
Arnold's difficulty eval:
1 - Easy
2 - Easy
Space optimal solutions is "Medium"
Fully functional unlimited RAM is "Medium + Hairy"
"""
from typing import List, Union
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from .common import IntCodeRunner


@inject_raw_input(2019, 9)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, ",").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


@print_return_value
def solve_part_1(payload: List[int]):
    outputs = IntCodeRunner(payload).append_input(1).run()
    return outputs[0]


@print_return_value
def solve_part_2(payload: List[int]):
    outputs = IntCodeRunner(payload).append_input(2).run()
    return outputs[0]
