# -*- coding: utf-8 -*-
"""
2019 day 8
Boring recap:
Arnold's difficulty eval:
1 -
2 -
"""
from collections import Counter
from typing import Set, Union
from streamer import streams, Stream
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner

WIDE, TALL = 25, 6


@inject_raw_input(2019, 8)
def show_solution(raw_input: str, part: Union[int, None]):
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(raw_input)


@print_return_value
def solve_part_1(data: str):
    layer_size = WIDE * TALL
    layer_counters = [Counter(data[i: i + layer_size]) for i in range(0, len(data), WIDE * TALL)]
    chosen_layer = min(layer_counters, key=lambda c: c['0'])
    return chosen_layer['1'] * chosen_layer['2']


@print_return_value
def solve_part_2(data: str):
    layer_size = WIDE * TALL
    pixels = Stream(data[i::layer_size] for i in range(layer_size)) \
        .map(lambda layer: Stream(layer).exclude(lambda c: c == '2').find_first()) \
        .map(lambda c: " @"[int(c)]) \
        .collect_as_list()
    rows = ["".join(pixels[i: i + WIDE]) for i in range(0, layer_size, WIDE)]
    print("This is raw pixels, you need to read it out")
    for r in rows:
        print(r)
    return rows
