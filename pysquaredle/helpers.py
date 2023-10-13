"""Support functions for PySquaredle."""

import argparse
import math
import random
import sys

from pysquaredle.web import get_letters_from_web


def puzzle_letters(args: argparse.Namespace) -> str:
    """Use the arguments to determine the letters to use."""
    if args.square:
        return random_letters(args.square**2)

    if not args.letters:
        return get_letters_from_web(args.express)

    letters = str(args.letters)
    length = len(letters)
    potential_side = math.sqrt(length)

    # must be square, optionally add letters
    if potential_side % 1:
        if not args.auto_extend:
            print("Invalid puzzle: letters must form a square grid.")
            sys.exit(-1)

        letters = extend(letters, potential_side)
    return letters


def parse_args() -> argparse.Namespace:
    """Interpret the command-line arguments and store for later use."""
    parser = argparse.ArgumentParser(
        description="Solves Squaredle puzzles",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "letters",
        help="""the puzzle letters. If not specified will try to download
        from https://squaredle.app. For puzzles with gaps, use underscores
        ('_') to represent the gaps. See also --express""",
        nargs="?",
    )
    group.add_argument(
        "-x",
        "--square",
        help="generate random square of x by x letters. Letter"
        " distribution matches a popular grid-based word game rhyming"
        " with scrabble",
        type=int,
    )

    output_group = parser.add_argument_group("output options")

    output_group.add_argument(
        "-c",
        "--single-column",
        action="store_true",
        help="display results as a single column. (default: %(default)s)",
    )

    output_group.add_argument(
        "-g",
        "--grid",
        action="store_true",
        help="display letters grid. (default: %(default)s)",
    )
    output_group.add_argument(
        "-H",
        "--headers",
        dest="headers",
        action="store_true",
        help="display headers for length-grouped solutions "
             "(default: %(default)s)",
    )
    output_group.add_argument(
        "-l",
        "--length",
        action="store_true",
        help="group solutions by word length (default: %(default)s)",
    )
    output_group.add_argument(
        "-m",
        "--multiple",
        help="in GUI mode, show all solutions for a given word "
             "(default: %(default)s)",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="randomise letter order, for setting puzzles. \
        Shows grid (default: %(default)s)",
    )
    output_group.add_argument(
        "-s",
        "--sort",
        action="store_true",
        help="sort solutions alphabetically (default: %(default)s)",
    )
    output_group.add_argument(
        "-u",
        "--gui",
        action="store_true",
        help="run in GUI mode. Some flags only affect text output, not GUI \
        (default: %(default)s)",
    )

    parser.add_argument(
        "-t",
        "--auto-extend",
        help="add extra letters to the grid to make it square "
             "(default: %(default)s)",
        action="store_true",
    )

    parser.add_argument(
        "-p",
        "--colour",
        "--color",
        help="adds painterly colour to the text version",
        action="store_true",
    )

    advanced_group = parser.add_argument_group("advanced options")
    advanced_group.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="display cell neighbour list for debugging (default: %(default)s)",
    )

    advanced_group.add_argument(
        "-e",
        "--express",
        action="store_true",
        help="use express puzzle, otherwise standard. \
        Only used when letters are downloaded (default: %(default)s)",
    )

    advanced_group.add_argument(
        "-f",
        "--file",
        help="specify word list (default: %(default)s)",
        default="./word_list.txt",
    )
    advanced_group.add_argument(
        "-z",
        "--slow-mode",
        action="store_true",
        help="show progress as it goes (default: %(default)s)",
    )

    args = parser.parse_args()
    return args


def random_letters(count: int) -> str:
    """Generate a string of count nicely distributed random letters."""
    return "".join(
        random.sample(
            "EEEEEEEEEEEEEEEEAAAAAAAAAIIIIIIIIIOOOOOOOONNNNNN"
            "RRRRRRTTTTTTLLLLSSSSUUUDDDDGGGBBCCMMPPFFHHVVWWYYKJXQZ",
            count,
        )
    )


def shuffle(letters: str) -> str:
    """Reorder the letters."""
    return "".join(random.sample(letters, len(letters)))


def extend(letters: str, potential_side: float) -> str:
    """Add enough random letters to make the grid square."""
    diff = (int(potential_side) + 1) ** 2 - len(letters)
    print(f"Adding {diff} letters to make a square grid.")
    letters += random_letters(diff)
    return letters
