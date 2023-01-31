#!/usr/bin/env python
"""
Solve Squaredle puzzles, main entry point.
"""

import math
import sys

from pysquaredle.helpers import extend, parse_args, random_letters, shuffle
from pysquaredle.puzzle import Puzzle
from pysquaredle.solver import Solver
from pysquaredle.ui.application import Application
from pysquaredle.web import get_letters_from_web


def main() -> int:
    """
    Main entry point for pysquaredle. Solves or sets Squaredle-type puzzles.

    If the --gui flag is set, the GUI is launched.
    """

    args = parse_args()

    if args.square and args.letters:
        print("Cannot specify both --square and letters")
        sys.exit(-1)

    if args.square:
        letters = random_letters(args.square**2)
    elif args.letters:
        letters = args.letters
    else:
        letters = get_letters_from_web()

    length = len(letters)
    potential_side = math.sqrt(length)

    # must be square, optionally add letters
    if potential_side % 1 != 0:
        if not args.auto_extend:
            print("Invalid puzzle: letters must form a square grid.")
            sys.exit(-1)

        letters = extend(letters, potential_side)

    # superfluous if square is set, but harmless to randomize them again
    if args.random:
        letters = shuffle(letters)

    puzzle = Puzzle(letters.upper())

    if args.slow_mode:

        def report(word: str, chain: list[int], hit_count: int) -> None:
            print(f"Checking {word} at {chain}. Hits: {hit_count}")

        solver = Solver(puzzle, args.word_list, report)
    else:
        solver = Solver(puzzle, args.word_list)

    if args.neighbours:
        print(puzzle.list_neighbours)

    if args.gui:
        app = Application(puzzle, solver, args.sort, args.multiple)
        sys.exit(app.exec())

    # no point showing grid if GUI is running
    if args.grid or args.random or args.square or args.auto_extend:
        print(puzzle.grid)

    print(
        solver.formatted_solutions(
            alpha_sort=args.sort,
            length_group=args.length,
            headers=not args.no_headers,
            single_column=args.single_column,
        )
    )

    # be nice to pipelines
    return 0


if __name__ == "__main__":
    main()
