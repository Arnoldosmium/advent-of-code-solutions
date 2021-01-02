# -*- coding: utf-8 -*-
from typing import Set
from streamer import streams
from ..utils import inject_raw_input, print_return_value

"""
2020 day 1
Boring recap: Finding number subset with a target sum
Arnold's difficulty eval:
1 - Super Easy
2 - Easy
"""


@inject_raw_input(2020, 1)
def show_solution(raw_input: str):
    nums = streams.split(raw_input, "\n").map(int).collect_as_set()
    return solve_part_1(nums), solve_part_2(nums)


@print_return_value
def solve_part_1(nums: Set[int]):
    complement = set(2020 - n for n in nums)
    a, b = nums & complement
    return a * b


@print_return_value
def solve_part_2(_nums: Set[int]):
    nums = list(_nums)
    any_two_complement = {2020 - a - b: (a, b) for i, a in enumerate(nums) for b in nums[i + 1:]}
    c = list(set(any_two_complement.keys()) & _nums)[0]
    a, b = any_two_complement[c]
    return a * b * c
