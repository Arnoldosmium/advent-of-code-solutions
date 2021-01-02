# -*- coding: utf-8 -*-
from collections import Counter
from typing import List, Union, Tuple
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner

"""
2020 day 2
Boring recap: 
Arnold's difficulty eval:
1 - 
2 - 
"""


@inject_raw_input(2020, 2)
def show_solution(raw_input: str, part: Union[int, None]):
    rule_checks = streams.split(raw_input, "\n")

    def parse_line(line):
        rule, to_check = line.split(": ")
        count_range, char = rule.split()
        a, b = count_range.split("-")
        return int(a), int(b), char, to_check

    rule_checks = rule_checks.map(parse_line).collect_as_list()

    return get_sub_task_runner(part, solve_part_1, solve_part_2)(rule_checks)


@print_return_value
def solve_part_1(rule_checks: List[Tuple]):
    return sum(
        count_low <= Counter(to_check)[char] <= count_high
        for count_low, count_high, char, to_check in rule_checks)


@print_return_value
def solve_part_2(rule_checks: List[Tuple]):
    return sum(
        (to_check[idx_a - 1] == char) ^ (to_check[idx_b - 1] == char)
        for idx_a, idx_b, char, to_check in rule_checks)
