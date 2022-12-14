from typing import Any

import requests
from bs4 import BeautifulSoup
from rich import print

from .aoc_input import _get_session_cookie, _update_session_cookie


def _submit(x: int, ans: Any, day: int, year: int) -> None:
    """Submit answer for part x.

    :param x: the part to _submit
    :param ans: the answer to _submit
    :param day: the day of the AoC challenge
    :param year: the year of the AoC challenge (default: CURRENT_YEAR)
    """
    headers = {"session": _get_session_cookie()}
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    data = {"level": x, "answer": str(ans)}
    response = requests.post(url, cookies=headers, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    assert soup.article is not None
    message = soup.article.text
    response.close()

    if message.startswith("--- Day"):
        _update_session_cookie()
        _submit(x, ans, day, year)
        return

    print(f"[bold]Part {x} submission:")
    if message.startswith("That's the right answer!"):
        print(f"[bold green]Correct answer.")
    elif message.startswith("That's not the right answer"):
        if "too low" in message:
            print(f" [bold red]Too low.")
        elif "too high" in message:
            print(f" [bold red]Too high.")
        else:
            print(f"[bold red]Incorrect answer.")
    elif message.startswith("You don't seem to be solving the right level"):
        print(f"[bold yellow]Already solved{' or part 1 not yet completed' if x == 2 else ''}.")
    elif message.startswith("You gave an answer too recently"):
        print(f"[bold yellow]Too fast. {message.split('.')[1].strip()}.")
    else:
        print(f"[bold red]Unknown response:[/]")
        print(message)


def submit_part_1(ans: Any, day: int, year: int) -> None:
    """Submit answer for part 1.

    :param ans: the answer to _submit
    :param day: the day of the AoC challenge
    :param year: the year of the AoC challenge
    """
    _submit(1, ans, day, year)


def submit_part_2(ans: Any, day: int, year: int) -> None:
    """Submit answer for part 2.

    :param ans: the answer to _submit
    :param day: the day of the AoC challenge
    :param year: the year of the AoC challenge (default: CURRENT_YEAR)
    """
    _submit(2, ans, day, year)
