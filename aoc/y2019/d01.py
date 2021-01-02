# -*- coding: utf-8 -*-
from typing import List, Union
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner

"""
2019 day 1
Boring recap: 
Arnold's difficulty eval:
1 - 
2 - 
"""


@inject_raw_input(2019, 1)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, "\n").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


@print_return_value
def solve_part_1(nums: List[int]):
    return sum(n // 3 - 2 for n in nums)


@print_return_value
def solve_part_2(nums: List[int]):
    def fuel_of(n: int):
        total = 0
        module = n
        while True:
            module = max(module // 3 - 2, 0)
            if module == 0:
                break
            total += module
        return total

    return sum(fuel_of(n) for n in nums)
