# -*- coding: utf-8 -*-
"""
2019 day 1
Boring recap: Array traverse and loop
Arnold's difficulty eval:
1 - Super easy
2 - Easy
"""
from typing import List, Union
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner


@inject_raw_input(2019, 1)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, "\n").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


@print_return_value
def solve_part_1(nums: List[int]):
    return sum(n // 3 - 2 for n in nums)


@print_return_value
def solve_part_2(nums: List[int]):
    def fuel_of(weight: int):
        return (streams.iterate(weight, lambda w: w // 3 - 2)       # constantly apply the cal to the previous result
                .skip(1)                                            # skip the initial module weight, not fuel!
                .takewhile(lambda w: w > 0)
                .collect(sum))

    return sum(fuel_of(n) for n in nums)
