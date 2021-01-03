# -*- coding: utf-8 -*-
"""
2019 day 6
Boring recap: Tree construction and traversing (BFS/DFS)
Arnold's difficulty eval:
1 - Easy
2 - Easy
"""
from collections import deque
from typing import Union
from streamer import streams
from ..utils import inject_raw_input, print_return_value, get_sub_task_runner
from ..utils.structures import Tree


@inject_raw_input(2019, 6)
def show_solution(raw_input: str, part: Union[int, None]):
    connects = streams.split(raw_input, "\n").map(lambda s: s.split(")")).collect_as_list()
    root = Tree.of_edges(connects)
    return get_sub_task_runner(part, solve_part_1, solve_part_2)(root)


@print_return_value
def solve_part_1(root: Tree):
    def add_count(top: Tree):
        top.attr['count'] = -1 if top.parent is None else top.parent.attr['count'] + 1
        for child in top.children.values():
            add_count(child)
    add_count(root)

    return sum(node.attr['count'] for node in root._nodes.values()) + 1     # root is -1 for calc purpose


@print_return_value
def solve_part_2(root: Tree):
    you_orbit = root['YOU'].parent
    san_orbit_id = root['SAN'].parent.node_id

    next_stops = deque([(you_orbit, 0)])
    reached = set()
    while len(next_stops):
        next_stop, count = next_stops.popleft()
        reached.add(next_stop.node_id)
        for reachable in [next_stop.parent] + list(next_stop.children.values()):
            if reachable is not None and reachable.node_id not in reached:
                if reachable.node_id == san_orbit_id:
                    return count + 1
                next_stops.append((reachable, count + 1))

    raise ValueError("Cannot reach SAN's orbit")
