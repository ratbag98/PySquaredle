#!/usr/bin/env python
"""
Solve Squaredle puzzles, main entry point.
"""


import argparse
import random
import sys

import requests

from gui import Application
from pysquaredle.solver import Solver


def get_letters_from_web() -> str:
    """
    Get the letters from the web page.
    """
    url = "https://squaredle.app/api/today-puzzle-config.js"
    response = requests.get(url, timeout=5)
    lines = response.text.splitlines()

    parsing = False
    letters = ""
    for line in lines:
        if r'"board": [' in line:
            parsing = True
        elif r"]," in line:
            break
        elif parsing:
            letters += line.replace('"', "").replace(",", "").replace(" ", "")

    return letters.upper()


def main() -> int:
    """
    Main entry point for pysquaredle. Solves or sets Squaredle-type puzzles.
    """

    args = parse_args()

    letters = args.letters

    args = parse_args()

    letters = args.letters

    if args.random:
        letters = "".join(random.sample(letters, len(letters)))

    try:
        if args.word_list:
            solver = Solver(letters, args.word_list)
        else:
            solver = Solver(letters)

    except ValueError:
        print("Letters cannot form a square grid.")
        sys.exit(-1)

    if args.gui:
        solver.solve()
        app = Application(solver)
        app.exec()
        return 0

    if args.grid or args.random:
        print(solver.grid())

    if args.neighbours:
        print(solver.list_neighbours())

    solver.solve()

    solver.print_solutions(vars(args))

    # be nice to pipelines
    return 0


def parse_args() -> argparse.Namespace:
    """
    Interpret the command-line arguments and store for later use.
    """
    parser = argparse.ArgumentParser(
        prog="PySquaredle",
        description="Solves the Squaredle puzzle, as seen on https://squaredle.app",
        epilog="(C) 2022 Robert Rainthorpe.",
    )

    parser.add_argument(
        "letters",
        help="the puzzle letters. If not specified will try to download from https://squaredle.app",
        default=get_letters_from_web(),
        nargs="?",
    )
    parser.add_argument(
        "-c",
        "--single-column",
        action="store_true",
        help="display results as a single column. Only option in GUI mode.",
    )
    parser.add_argument(
        "-g",
        "--grid",
        action="store_true",
        help="display letters in grid layout. Only option in GUI mode.",
    )
    parser.add_argument(
        "-l",
        "--length",
        action="store_true",
        help="group solutions by word length. Only option in GUI mode.",
    )
    parser.add_argument(
        "-n",
        "--neighbours",
        action="store_true",
        help="display cell neighbour list for debugging. Not appropriate for GUI mode.",
    )
    parser.add_argument(
        "-N",
        "--no-headers",
        dest="headers",
        action="store_true",
        help="don't display headers for length-grouped solutions. Not appropriate for GUI mode.",
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="randomise letter order. For setting puzzles. Automatically shows grid.",
    )
    parser.add_argument(
        "-s",
        "--sort",
        action="store_true",
        help="sort solutions alphabetically. Only option in GUI mode.",
    )
    parser.add_argument(
        "-w", "--word-list", help="use different word list to default (./word_list.txt)"
    )
    parser.add_argument(
        "-u", "--gui", action="store_true", help="run in GUI mode. Most args ignored."
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
