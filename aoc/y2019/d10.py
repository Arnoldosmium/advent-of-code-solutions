# -*- coding: utf-8 -*-
"""
2019 day 10
Boring recap:
Arnold's difficulty eval:
1 -
2 -
"""
from collections import defaultdict
from itertools import combinations
from typing import List, Union, Tuple, Dict
from streamer import streams, DictStream
from ..utils import inject_raw_input, print_return_value
from ..utils.maths import DirectionalRatio, manhattan_distance


@inject_raw_input(2019, 10)
def show_solution(raw_input: str, _: Union[int, None]):
    area = streams.split(raw_input, "\n").map(list).collect_as_list()
    asteroids = streams.cartesian_product_stream(range(len(area)), range(len(area[0]))) \
        .filter(lambda xy: area[xy[0]][xy[1]] == '#') \
        .collect_as_list()
    point_vectors = defaultdict(lambda: defaultdict(list))
    for a, b in combinations(asteroids, 2):
        point_vectors[a][DirectionalRatio.from_vector(a, b)].append(b)
        point_vectors[b][DirectionalRatio.from_vector(b, a)].append(a)

    laser, max_count = solve_part_1(point_vectors)
    print(max_count, 'at', laser)
    part2 = solve_part_2(laser, point_vectors)
    return max_count, part2


# Don't convert to string here
def solve_part_1(asteroid_vectors: Dict[Tuple[int, int], Dict[DirectionalRatio, List[Tuple[int, int]]]]):
    return DictStream(asteroid_vectors) \
        .map_values(len) \
        .max(lambda kv: kv[1])


@print_return_value
def solve_part_2(
        laser: Tuple[int, int],
        asteroid_vectors: Dict[Tuple[int, int], Dict[DirectionalRatio, List[Tuple[int, int]]]]):
    asteroid_vector = {
        ratio: sorted(point_list, key=lambda p: manhattan_distance(laser, p))
        for ratio, point_list in asteroid_vectors[laser].items()}
    counter = 0
    full_revolution = sorted((ratio for ratio in asteroid_vector if ratio.q < 0 <= ratio.p),
                             key=lambda ratio: -ratio.val) + \
        [DirectionalRatio(1, 0)] + \
        sorted((ratio for ratio in asteroid_vector if ratio.q > 0), key=lambda ratio: -ratio.val) + \
        [DirectionalRatio(-1, 0)] + \
        sorted((ratio for ratio in asteroid_vector if ratio.q < 0 and ratio.p < 0), key=lambda ratio: -ratio.val)
    while len(asteroid_vector.keys()):
        for dratio in full_revolution:
            if dratio in asteroid_vector:
                counter += 1
                current = asteroid_vector[dratio].pop(0)
                if counter == 200:
                    x, y = current
                    return 100 * y + x
                if len(asteroid_vector[dratio]) == 0:
                    del asteroid_vector[dratio]
    raise ValueError("Failed to achieve number 200")