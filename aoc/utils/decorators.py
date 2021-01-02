import requests
from typing import Callable, Tuple, List, Any, Optional


def inject_raw_input(year: int, day: int):

    def _decorator(f: Callable[[str, Optional[int]], Tuple[str, str]]):
        def _wrap(session: requests.Session, part: Optional[int]):
            rsp = session.get("https://adventofcode.com/{year}/day/{day}/input".format(year=year, day=day))
            if rsp.status_code != 200:
                raise ValueError("Response from server was not successful: %s" % rsp.content)
            return f(rsp.content.decode("utf-8").strip(), part)
        return _wrap

    return _decorator


def split_by(delim: str):

    def _decorator(f: Callable[[List[str]], Tuple[str, str]]):
        def _wrap(raw_input: str):
            return f(raw_input.split(delim))
        return _wrap

    return _decorator


def print_return_value(f: Callable):
    def _wrap(*args) -> str:
        result = str(f(*args))
        print(result)
        return result

    return _wrap


def get_sub_task_runner(part: Optional[int], f1: Callable[[Any], str], f2: Callable[[Any], str]):

    def _runner(*args):
        if part == 1:
            return f1(*args), None
        elif part == 2:
            return None, f2(*args)
        else:
            return f1(*args), f2(*args)

    return _runner
