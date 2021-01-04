# -*- coding: utf-8 -*-
"""
2019 day 12
Boring recap: Inter-object interaction simulation + vector decomposition method + lcm
Arnold's difficulty eval:
1 - Easy
2 - Hard + Burning
"""
from __future__ import nested_scopes
from itertools import combinations
from typing import Union, List, Tuple, Iterable
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from ..utils.maths import sign_of, lcm


class MoonDimensionCoord:
    def __init__(self, coord: int):
        self.at = coord
        self.v = 0

    def influenced_by(self, other: 'MoonDimensionCoord'):
        self.v += sign_of(other.at - self.at)

    def move(self):
        self.at += self.v


@inject_raw_input(2019, 12)
def show_solution(raw_input: str, part: Union[int, None]):
    def parse_moon(expr: str):
        return streams.split(expr[1:-1], ", ") \
            .map(lambda eqn: int(eqn.split("=")[1])) \
            .collect(tuple)

    moons = streams.split(raw_input, "\n") \
        .map(parse_moon) \
        .collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(moons)


@print_return_value
def solve_part_1(raw_moons: List[Tuple[int, int, int]]):
    moons = [tuple(map(MoonDimensionCoord, coords)) for coords in raw_moons]
    for _ in range(1000):
        for moon_a, moon_b in combinations(moons, 2):
            for moon_coord_a, moon_coord_b in zip(moon_a, moon_b):
                moon_coord_a.influenced_by(moon_coord_b)
                moon_coord_b.influenced_by(moon_coord_a)
        for moon in moons:
            for each_coord in moon:
                each_coord.move()
    return sum(sum(abs(coord.at) for coord in m) * sum(abs(coord.v) for coord in m) for m in moons)


@print_return_value
def solve_part_2(moons: List[Tuple[int, int, int]]):
    def find_repeat(raw_coords: Iterable[int]):
        coords = list(map(MoonDimensionCoord, raw_coords))
        count = 0
        while True:
            count += 1
            for coord_a, coord_b in combinations(coords, 2):
                coord_a.influenced_by(coord_b)
                coord_b.influenced_by(coord_a)
            for coord in coords:
                coord.move()
            if all(coord.at == raw_coord and coord.v == 0 for coord, raw_coord in zip(coords, raw_coords)):
                return count

    repetitive_periods = [find_repeat(raw_coords) for raw_coords in zip(*moons)]
    px, py, pz = repetitive_periods
    return lcm(lcm(px, py), pz)