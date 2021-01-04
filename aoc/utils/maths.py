# -*- coding: utf-8 -*-
from __future__ import nested_scopes
from typing import Iterable, Union, Tuple
import sys
from math import gcd

def product(nums: Iterable[Union[int, float]]):
    prod = 1
    for n in nums:
        prod *= n
    return prod


def num_in_range(num: int, valid_range: Tuple[int, int]):
    range_from = min(valid_range)
    range_to = max(valid_range)
    return range_from <= num <= range_to


def lcm(x: int, y: int):
    """
    Find least common multiple
    """
    return abs(x * y) // gcd(x, y)

def sign_of(x: float) -> int:
    if x == 0:
        return 0
    return int(x / abs(x))


def manhattan_distance(point_a: Tuple, point_b: Tuple):
    return sum(abs(a - b) for a, b in zip(point_a, point_b))


class DirectionalRatio:
    p: int
    q: int

    def __init__(self, num: int, denom: int):
        dgcd = gcd(num, denom)
        self.p, self.q = (num // dgcd, denom // dgcd)

    def __str__(self):
        return f"({self.p}/{self.q})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other: 'DirectionalRatio'):
        return self.p == other.p and self.q == other.q

    def __hash__(self):
        return hash(str(self))

    @property
    def val(self):
        return self.p / self.q if self.q != 0 else self.p * sys.float_info.max

    @staticmethod
    def from_vector(base: Tuple[int, int], to: Tuple[int, int]):
        bx, by = base
        tx, ty = to
        return DirectionalRatio(ty - by, tx - bx)
    

class Ratio(DirectionalRatio):
    
    def __init__(self, num: int, denom: int):
        super(Ratio, self).__init__(num, denom)
        if self.p < 0:
            self.p, self.q = -self.p, -self.q
        elif self.p == 0 and self.q < 0:
            self.q = -self.q


class RationalLine:
    slope: Ratio
    intercept: Ratio

    def __init__(self, a: Tuple[int, int], b: Tuple[int, int]):
        ax, ay = a
        bx, by = b
        dx = ax - bx
        dy = ay - by
        self.slope = Ratio(dy, dx)
        if self.slope.q == 0:
            self.intercept = Ratio(1, 1)
        else:
            inter = self.slope.q * ay - self.slope.p * ax
            self.intercept = Ratio(inter, self.slope.q)

    def __str__(self):
        return f"y = {self.slope}x + {self.intercept}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other: 'RationalLine'):
        return self.slope == other.slope and self.intercept == other.intercept
