# -*- coding: utf-8 -*-
"""
2019 day 4
Boring recap: Number digit based calculation
Arnold's difficulty eval:
1 - Easy
2 - Easy
"""
from collections import Counter
from typing import Set, Union
from streamer import streams, Stream
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner


@inject_raw_input(2019, 4)
def show_solution(raw_input: str, part: Union[int, None]):
    range_from, range_to = streams.split(raw_input, "-").map(int).collect_as_list()
    password_candidates = Stream(range(range_from, range_to + 1)) \
        .map(str) \
        .filter(lambda num_str: all(lead <= lag for lead, lag in zip(num_str[:-1], num_str[1:]))) \
        .collect_as_set()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(password_candidates)


@print_return_value
def solve_part_1(nums: Set[int]):
    return Stream(nums).filter(lambda num_str: max(Counter(num_str).values()) >= 2).count()


@print_return_value
def solve_part_2(nums: Set[int]):
    return Stream(nums).filter(lambda num_str: any(cnt == 2 for cnt in Counter(num_str).values())).count()
