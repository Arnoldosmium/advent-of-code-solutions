# -*- coding: utf-8 -*-
"""
2019 day 7
Boring recap: State machine context switch & i/o stream pipes simulation
Arnold's difficulty eval:
1 - Easy
2 - Medium
"""
from itertools import permutations, repeat
from typing import List, Union
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from .common import IntCodeRunner


@inject_raw_input(2019, 7)
def show_solution(raw_input: str, part: Union[int, None]):
    nums = streams.split(raw_input, ",").map(int).collect_as_list()
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(nums)


@print_return_value
def solve_part_1(payload: List[int]):
    max_signal = 0
    for sequence in permutations(range(5), 5):
        signal = 0
        for phase in sequence:
            outputs = IntCodeRunner.of(payload, [phase, signal]).run()
            signal = outputs[0]
        max_signal = max(max_signal, signal)

    return max_signal


@print_return_value
def solve_part_2(payload: List[int]):
    max_signal = 0
    for sequence in permutations(range(5, 10), 5):
        signal = 0
        runners = [IntCodeRunner.of(payload, [phase]) for phase in sequence]
        output_generators = [runner.outputs() for runner in runners]
        stopped = False
        while not stopped:
            for i, phase in enumerate(sequence):
                runners[i].append_input(signal)
                try:
                    signal = next(output_generators[i])
                except StopIteration:
                    stopped = True
                    break
        max_signal = max(max_signal, signal)

    return max_signal
