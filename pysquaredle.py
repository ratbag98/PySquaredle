#!/usr/bin/env python3
"""
Solve Squaredle puzzles, main entry point.
"""


import argparse
import random
import sys

from solver import Solver

# from trie import Trie


def main() -> int:
    """
    Main entry point for pysquaredle. Solves or sets Squaredle-type puzzles.
    """

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

    parser.add_argument("letters", help="the puzzle letters")
    parser.add_argument(
        "-c",
        "--single-column",
        action="store_true",
        help="display results as a single column",
    )
    parser.add_argument(
        "-g", "--grid", action="store_true", help="display letters in grid layout"
    )
    parser.add_argument(
        "-l", "--length", action="store_true", help="group solutions by word length"
    )
    parser.add_argument(
        "-n",
        "--neighbours",
        action="store_true",
        help="display cell neighbour list for debugging",
    )
    parser.add_argument(
        "-N",
        "--no-headers",
        dest="headers",
        action="store_true",
        help="don't display headers for length-grouped solutions",
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="randomise letter order. For setting puzzles. Automatically shows grid",
    )
    parser.add_argument(
        "-s", "--sort", action="store_true", help="sort solutions alphabetically"
    )
    parser.add_argument(
        "-w", "--word-list", help="use different word list to default (./word_list.txt)"
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
