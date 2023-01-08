#!/usr/bin/env python
"""
Solve Squaredle puzzles, main entry point.
"""

import argparse
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

    def __init__(self, solver: Solver, args: argparse.Namespace):
        super().__init__(sys.argv)

        self.main_window = MainWindow(solver, args.sort, args.multiple)
        self.main_window.show()


def main() -> int:
    """
    Main entry point for pysquaredle. Solves or sets Squaredle-type puzzles.

    If the --gui flag is set, the GUI is launched.
    """

    args = parse_args()
    if args.letters:
        letters = args.letters
    else:
        letters = get_letters_from_web()

    if args.random:
        letters = "".join(random.sample(letters, len(letters)))

    try:
        solver = Solver(letters, args.word_list)

    except ValueError:
        print("Invalid puzzle: letters must form a square grid.")
        sys.exit(-1)

    solver.solve()

    if args.neighbours:
        print(solver.list_neighbours)

    if args.gui:
        app = Application(solver, args)
        sys.exit(app.exec())

    # no point showing grid if GUI is running
    if args.grid or args.random:
        print(solver.grid)

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
        dest="headers",
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

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
