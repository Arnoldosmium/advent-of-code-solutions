from typing import Iterable, Union, Tuple


def product(nums: Iterable[Union[int, float]]):
    prod = 1
    for n in nums:
        prod *= n
    return prod


def num_in_range(num: int, valid_range: Tuple[int, int]):
    range_from = min(valid_range)
    range_to = max(valid_range)
    return range_from <= num <= range_to
