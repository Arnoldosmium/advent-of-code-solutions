from typing import Iterable, Union


def product(nums: Iterable[Union[int, float]]):
    prod = 1
    for n in nums:
        prod *= n
    return prod
