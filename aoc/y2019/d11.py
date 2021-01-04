# -*- coding: utf-8 -*-
"""
2019 day 11
Boring recap: 2-D plane painting and cursor movements
Arnold's difficulty eval:
1 - Easy
2 - Easy
"""
from collections import defaultdict
from typing import List, Union, Dict, Tuple
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from .common import IntCodeRunner

DISPLACEMENT = [(0, 1), (1, 0), (0, -1), (-1, 0)]


@inject_raw_input(2019, 11)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, ",").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


def paint(program: List[int], panel: Dict[Tuple[int, int], int]):
    direction = 0
    loc_x, loc_y = 0, 0

    runner = IntCodeRunner(program)
    output_generator = runner.outputs()
    while True:
        runner.append_input(panel[(loc_x, loc_y)])
        try:
            color = next(output_generator)
        except StopIteration:
            return
        turn = next(output_generator)
        panel[(loc_x, loc_y)] = color
        direction = (direction + (turn * 2) - 1) % 4
        dx, dy = DISPLACEMENT[direction]
        loc_x += dx
        loc_y += dy


@print_return_value
def solve_part_1(payload: List[int]):
    panel = defaultdict(int)
    paint(payload, panel)
    return len(panel.keys())


@print_return_value
def solve_part_2(payload: List[int]):
    panel = defaultdict(int)
    panel[(0, 0)] = 1
    paint(payload, panel)
    print("This is raw only, need to read it out!")
    x_min = min(x for x, _ in panel)
    x_max = max(x for x, _ in panel)
    y_min = min(y for _, y in panel)
    y_max = max(y for _, y in panel)
    pixels = ["".join('@' if panel[(x, y)] else " " for x in range(x_min, x_max + 1)) for y in range(y_max, y_min - 1, -1)]
    for row in pixels:
        print(row)
    print()
    return pixels
