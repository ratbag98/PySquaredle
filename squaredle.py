#!/usr/bin/env python
"""
Solve Squaredle puzzles, main entry point.
"""

import argparse
import math
import random
import sys

from PyQt6.QtWidgets import QApplication

from pysquaredle.solver import Solver
from pysquaredle.web import get_letters_from_web
from ui.main_window import MainWindow


class Application(QApplication):
    """
    Main application for the GUI application. Ignored unless --gui is set.
    """

    def __init__(self, solver: Solver, alpha_sort: bool = True, multiple: bool = False):
        super().__init__(sys.argv)

        self.main_window = MainWindow(solver, alpha_sort, multiple)
        self.main_window.show()


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

    #    print(f"Letters: {letters} {potential_side} {len(letters)}")

    # must be square, optionally add letters
    if potential_side % 1 != 0:
        if not args.auto_extend:
            print("Invalid puzzle: letters must form a square grid.")
            sys.exit(-1)

        # add letters to make a square
        diff = (int(potential_side) + 1) ** 2 - length
        print(f"Adding {diff} letters to make a square grid.")
        letters += random_letters(diff)

    # superfluous if square is set, but harmless to randomize them again
    if args.random:
        letters = "".join(random.sample(letters, len(letters)))

    if args.slow_mode:

        def report(word: str, chain: list[int], hit_count: int) -> None:
            print(f"Checking {word} at {chain}. Hits: {hit_count}")

        solver = Solver(letters.upper(), args.word_list, report)
    else:
        solver = Solver(letters.upper(), args.word_list)

    solver.solve()

    if args.neighbours:
        print(solver.list_neighbours)

    if args.gui:
        app = Application(solver, args.sort, args.multiple)
        sys.exit(app.exec())

    # no point showing grid if GUI is running
    if args.grid or args.random or args.square or args.auto_extend:
        print(solver.grid)

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
        help="""the puzzle letters. If not specified will try to download
        from https://squaredle.app. For puzzles with gaps, use underscores
        ('_') to represent the gaps.""",
        nargs="?",
    )
    parser.add_argument(
        "-c",
        "--single-column",
        action="store_true",
        help="display results as a single column.",
    )
    parser.add_argument(
        "-g",
        "--grid",
        action="store_true",
        help="display letters in grid layout.",
    )
    parser.add_argument(
        "-l",
        "--length",
        action="store_true",
        help="group solutions by word length.",
    )
    parser.add_argument(
        "-n",
        "--neighbours",
        action="store_true",
        help="display cell neighbour list for debugging.",
    )
    parser.add_argument(
        "-N",
        "--no-headers",
        dest="no_headers",
        action="store_true",
        help="don't display headers for length-grouped solutions.",
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
        help="sort solutions alphabetically.",
    )
    parser.add_argument(
        "-w",
        "--word-list",
        help="use different word list to default (./word_list.txt)",
        default="./word_list.txt",
    )
    parser.add_argument(
        "-u",
        "--gui",
        action="store_true",
        help="run in GUI mode. Other flags affect text output, not GUI",
    )
    parser.add_argument(
        "-m",
        "--multiple",
        help="in GUI mode, show all solutions for a given word. (messy)",
        action="store_true",
    )
    parser.add_argument(
        "-x",
        "--square",
        help="generate random square of x by x letters. Letter"
        " distribution matches a popular grid-based word game rhyming"
        " with scrabble",
        type=int,
    )
    parser.add_argument(
        "-t",
        "--auto-extend",
        help="add extra letters to the grid to make it square",
        action="store_true",
    )
    parser.add_argument(
        "-z", "--slow-mode", action="store_true", help="show progress as it goes"
    )

    args = parser.parse_args()
    return args


def random_letters(count: int) -> str:
    """
    Generate a string of count nicely distributed random letters
    """
    return "".join(
        random.choice(
            "EEEEEEEEEEEEEEEEAAAAAAAAAIIIIIIIIIOOOOOOOONNNNNN"
            "RRRRRRTTTTTTLLLLSSSSUUUDDDDGGGBBCCMMPPFFHHVVWWYYKJXQZ"
        )
        for _ in range(count)
    )


if __name__ == "__main__":
    main()
