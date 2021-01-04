# -*- coding: utf-8 -*-
"""
2019 day 13
Boring recap: Canvas simulation + State machine blocking + Simple state-based game decision making
Arnold's difficulty eval:
1 - Easy
2 - Hard
"""
from collections import defaultdict
from typing import List, Union, Dict, Tuple
from streamer import streams
from .common import IntCodeRunner, BLOCK_FOR_INPUT
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from ..utils.maths import sign_of


def update_game_status(game_tiles: Dict[Tuple[int, int], int], output_generator):
    score = None
    while True:
        try:
            x = next(output_generator)
        except StopIteration:
            return game_tiles, score
        if x == BLOCK_FOR_INPUT:
            return game_tiles, score
        y = next(output_generator)
        tile_id = next(output_generator)
        if x == -1:
            score = tile_id
        else:
            game_tiles[(x, y)] = tile_id


def get_tile_type_locations(game_tiles: Dict[Tuple[int, int], int], tile_type: int):
    return [coord for coord, tile_id in game_tiles.items() if tile_id == tile_type]


@inject_raw_input(2019, 13)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, ",").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


@print_return_value
def solve_part_1(payload: List[int]):
    runner = IntCodeRunner(payload)
    tiles, _ = update_game_status(defaultdict(int), runner.outputs())
    return len(get_tile_type_locations(tiles, 2))


@print_return_value
def solve_part_2(payload: List[int]):
    runner = IntCodeRunner([2] + payload[1:])
    output_generator = runner.outputs()

    tiles, score = update_game_status(defaultdict(int), output_generator)
    while len(get_tile_type_locations(tiles, 2)) > 0:
        ball_x, _ = get_tile_type_locations(tiles, 4)[0]
        paddle_x, _ = get_tile_type_locations(tiles, 3)[0]
        runner.append_input(sign_of(ball_x - paddle_x))
        tiles, score = update_game_status(tiles, output_generator)
    return score
