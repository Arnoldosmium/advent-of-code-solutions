import requests
from typing import Callable, Tuple, List


def inject_raw_input(year: int, day: int):

    def _decorator(f: Callable[[str], Tuple[str, str]]):
        def _wrap(session: requests.Session):
            rsp = session.get("https://adventofcode.com/{year}/day/{day}/input".format(year=year, day=day))
            if rsp.status_code != 200:
                raise ValueError("Response from server was not successful: %s" % rsp.content)
            return f(rsp.content.decode("utf-8").strip())
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