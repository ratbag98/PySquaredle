from pysquaredle.console import console
from rich.columns import Columns
from rich.rule import Rule
from rich.emoji import Emoji
from itertools import groupby


def output_formatted_results(words: list[str], length_group: bool, headers: bool, single_column: bool) -> None:
    """
    Output nicely formatted results to console
    """
    if not length_group:
        _output_block(words, single_column)
        return

    for key, group in groupby(words, key=len):
        if headers:
            console.print("\n")
            console.print(Rule(f"{key} letter words", align="left", end="\n\n"))
        _output_block(list(group), single_column)

    return

def _output_block(words: list[str], single_column=False) -> None:
    emojied = [_emojify(word) for word in words]
    if not single_column:
        col = Columns(emojied, equal=True)
        console.print(col)
    else:
        console.print("\n".join(emojied))
    return

def _emojify(word: str) -> str:
    emoji = Emoji.replace(f":{word}:")
    if emoji == f":{word}:":
        return f"{word} " # nice spacing

    return f"{word}{emoji}"
