# -*- coding: utf-8 -*-
"""
2019 day 3
Boring recap: Road map intersection detection
Arnold's difficulty eval:
1 - Medium
2 - Medium
"""
from __future__ import nested_scopes
from collections import defaultdict, namedtuple
from typing import List, Union, Dict, Tuple
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from ..utils.maths import num_in_range


class WireCoverage:
    def __init__(self, wire: List[str]):
        self.x_cover = defaultdict(list)   # vertical line, a range of x has wire presence
        self.y_cover = defaultdict(list)   # horizontal line, a range of y has wire presence
        self.initialize(wire)

    def initialize(self, wire: List[str]):
        x, y = 0, 0
        step_counter = 0
        for step in wire:
            direction = step[0]
            scale = int(step[1:])
            if direction in 'LR':
                advance = ('LR'.index(direction) * 2 - 1) * scale
                self.y_cover[y].append(((x, x + advance), step_counter))
                x += advance
            elif direction in 'UD':
                advance = ('DU'.index(direction) * 2 - 1) * scale
                self.x_cover[x].append(((y, y + advance), step_counter))
                y += advance
            else:
                raise ValueError("Invalid direction %s" % step[0])
            step_counter += scale

    @staticmethod
    def find_intersect_from_coverage_map(x_cover: Dict[int, List[Tuple]], y_cover: Dict[int, List[Tuple]]):
        CoordTestTuple = namedtuple("CoordTestTuple", "x,y,x_range,y_range,steps")
        return streams.cartesian_product_stream(x_cover.keys(), y_cover.keys()) \
            .flat_map(lambda xy: (CoordTestTuple(
                                    x=xy[0], y=xy[1], x_range=x_range, y_range=y_range, steps=x_steps + y_steps)
                                  for y_range, x_steps in x_cover[xy[0]]
                                  for x_range, y_steps in y_cover[xy[1]])) \
            .filter(lambda ttuple: num_in_range(ttuple.x, ttuple.x_range) and num_in_range(ttuple.y, ttuple.y_range)) \
            .map(lambda ttuple: (ttuple.x,
                                 ttuple.y,
                                 ttuple.steps + abs(ttuple.x - ttuple.x_range[0]) + abs(ttuple.y - ttuple.y_range[0])))\
            .collect_as_list()

    def find_intersect(self, other: 'WireCoverage'):
        return WireCoverage.find_intersect_from_coverage_map(self.x_cover, other.y_cover) + \
               WireCoverage.find_intersect_from_coverage_map(other.x_cover, self.y_cover)


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
