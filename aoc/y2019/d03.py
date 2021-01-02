# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import List, Union
from streamer import streams, Stream
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from ..utils.maths import num_in_range

"""
2019 day 3
Boring recap: 
Arnold's difficulty eval:
1 - 
2 - 
"""
# TODO: re-write

class WireCoverage:
    def __init__(self, wire: List[str]):
        self.x_cover = defaultdict(list)   # vertical line, a range of x has wire presence
        self.y_cover = defaultdict(list)   # horizontal line, a range of y has wire presence
        self.initialize(wire)

    def initialize(self, wire: List[str]):
        x, y = 0, 0
        steps = 0
        for edge in wire:
            direction = edge[0]
            scale = int(edge[1:])
            if direction in 'LR':
                advance = ('LR'.index(direction) * 2 - 1) * scale
                self.y_cover[y].append(((x, x + advance), steps))
                x += advance
            elif direction in 'UD':
                advance = ('DU'.index(direction) * 2 - 1) * scale
                self.x_cover[x].append(((y, y + advance), steps))
                y += advance
            else:
                raise ValueError("Invalid direction %s" % edge[0])
            steps += scale

    def find_intersect(self, other):
        inter = []
        for x, y_ranges in self.x_cover.items():
            for y_range, self_steps in y_ranges:
                for y, x_ranges in other.y_cover.items():
                    if num_in_range(y, y_range):
                        for x_range, other_steps in x_ranges:
                            if num_in_range(x, x_range):
                                inter.append(
                                    (x, y, self_steps + abs(x - x_range[0]) + other_steps + abs(y - y_range[0])))
        for x, y_ranges in other.x_cover.items():
            for y_range, other_steps in y_ranges:
                for y, x_ranges in self.y_cover.items():
                    if num_in_range(y, y_range):
                        for x_range, self_steps in x_ranges:
                            if num_in_range(x, x_range):
                                inter.append(
                                    (x, y, self_steps + abs(y - y_range[0]) + other_steps + abs(x - x_range[0])))
        return inter


@inject_raw_input(2019, 3)
def show_solution(raw_input: str, part: Union[int, None]):
    wire_a, wire_b = streams.split(raw_input, "\n") \
        .map(lambda s: s.split(",")) \
        .collect_as_list()
    intersects = WireCoverage(wire_a).find_intersect(WireCoverage(wire_b))
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(intersects)


@print_return_value
def solve_part_1(intersects: List):
    return min(abs(x) + abs(y) for x, y, _ in intersects if x != 0 and y != 0)


@print_return_value
def solve_part_2(intersects: List):
    return min(t[2] for t in intersects if t[2])
