import argparse
import importlib
import sys

import requests
import requests.utils
from streamer import streams
import yaml


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="Year of advent of code project", type=int)
    parser.add_argument("question", help="Question # / day #", type=int)
    parser.add_argument("-c", "--conf", help="Configuration file with cookie", default="conf.yml")

    return parser


def cookie_dict(conf_file):
    with open(conf_file, "r") as file_input:
        conf_dict = yaml.safe_load(file_input)
    return streams.split(conf_dict['cookie_raw'], "; ") \
        .map(str.strip) \
        .map(lambda s: s.split("=")) \
        .collect_dict()


def main():
    parser = setup_parser()
    args = parser.parse_args(sys.argv[1:])
    solution_module = importlib.import_module("aoc.y{0.year}.d{0.question:02d}".format(args))

    with requests.Session() as s:
        requests.utils.add_dict_to_cookiejar(s.cookies, cookie_dict(args.conf))
        solution_module.show_solution(s)


if __name__ == '__main__':
    main()
