"""
Module to handle web requests
"""
import re

import requests


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
            letters += "".join(re.findall(r"\"([a-zA-Z ]+)\"", line))
            letters = letters.replace(" ", "_")

    return letters.upper()
