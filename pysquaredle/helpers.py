"""
Support functions for PySquaredle.
"""

import argparse
import random


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


def shuffle(letters: str) -> str:
    """
    Reorder the letters
    """
    return "".join(random.sample(letters, len(letters)))


def extend(letters: str, potential_side: float) -> str:
    """
    Add enough random letters to make the grid square
    """
    diff = (int(potential_side) + 1) ** 2 - len(letters)
    print(f"Adding {diff} letters to make a square grid.")
    letters += random_letters(diff)
    return letters
