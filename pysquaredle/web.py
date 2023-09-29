""" Module to handle web requests """

import re
import sys

import requests
from requests.exceptions import ReadTimeout


def get_letters_from_web(express: bool = False) -> str:
    """Get the letters from the web page."""

    url = "https://squaredle.app/api/today-puzzle-config.js"
    try:
        response = requests.get(url, timeout=5)
    except ReadTimeout:
        print("Web puzzle requested but nothing received in time.")

        sys.exit(255)

    puzzle_config = response.text

    date = get_latest_puzzle_date(puzzle_config)

    matches = re.findall(
        rf'"{date}(-xp)?": ' + r'\{\s?\n\s+"board": \[(.*?)\]', puzzle_config, re.DOTALL
    )

    letters = "NO PUZZLE FOUND"
    for config in matches:
        match config:
            case ("", board):
                if not express:
                    letters = clean_board(board)
            case ("-xp", board):
                if express:
                    letters = clean_board(board)
            case _:
                # Impossible to get here, but mypy doesn't know that
                pass

    return letters.upper()


def clean_board(raw_board: str) -> str:
    """Clean up the board string."""

    # first make a single-line string of quoted rows
    simple = re.sub(r"\n\s+", "", raw_board).strip().replace(" ", "_")

    # and clean the rest on the way out
    return re.sub(r'[",]', "", simple)


def get_latest_puzzle_date(puzzle_config: str) -> str:
    """Find the latest puzzle date in the puzzle config."""

    if date_match := re.search(r"const gTodayDateStr = '([0-9-/]+)';", puzzle_config):
        # escape the backslashes manually and then make sure regex likes them
        return re.escape(re.sub("/", "\\/", date_match.group(1)))
    return "Unknown"
