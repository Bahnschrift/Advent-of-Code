from typing import Callable, TypeVar, Union

import requests
import io
from rich import print

from .grid import Grid
from .utils import ints

_COOKIE_PATH = "cookie.txt"
_USER_AGENT = "Bahnschrift's Advent of Code Helper - https://github.com/Bahnschrift/Advent-of-Code"
_INPUT_URL = "https://adventofcode.com/{year}/day/{day}/input"
_INPUT_PATH = "../inputs/day{day:02d}.txt"


########################################################################################################################
# Input parsing                                                                                                        #
########################################################################################################################

_T = TypeVar("_T")


class Input(str):
    def __new__(cls, s: str):
        return super().__new__(cls, s.rstrip("\n"))

    def parse(self, parse_func: Callable[[str], _T]) -> _T:
        """Parses the input using the given function."""
        return parse_func(self)

    def parse_str(self) -> str:
        """Parses the input into a string."""
        return self

    def parse_int(self) -> int:
        """Parses the input into an integer."""
        return int(self)

    def parse_digits(self) -> list[int]:
        """Parses the input as a contiguous sequence of individual digits."""
        return list(map(int, self))

    def parse_lines(self) -> list[str]:
        """Parses the input into a list of lines."""
        return self.split("\n")

    def parse_ints(self) -> list[int]:
        """Parses the input into a list of integers."""
        return ints(self)

    def parse_int_lines(self) -> list[int]:
        """Parses the input into a list of integers, with one integer per line."""
        return [int(line) for line in self.parse_lines()]

    def parse_groups(self) -> list[list[str]]:
        """Parses the input into a list of groups of lines."""
        return [group.split("\n") for group in self.split("\n\n")]

    def parse_int_groups(self) -> list[list[int]]:
        """Parses the input into a list of groups of integers."""
        return [[int(line) for line in group] for group in self.parse_groups()]

    def parse_grid(self) -> Grid[str]:
        """Parses the input into a grid of characters."""
        return Grid(self.parse_lines())

    def parse_int_grid(self) -> Grid[int]:
        """Parses the input into a grid of integers."""
        return Grid([[int(char) for char in line] for line in self.parse_lines()])

    def parse_grid_groups(self) -> list[Grid[str]]:
        """Parses the input into a list of grids of characters."""
        return [Grid(group) for group in self.parse_groups()]

    def parse_int_grid_groups(self) -> list[Grid[int]]:
        """Parses the input into a list of grids of integers."""
        return [Grid([[int(char) for char in line] for line in group]) for group in self.parse_groups()]


########################################################################################################################
# Input downloading                                                                                                    #
########################################################################################################################


def _get_session_cookie() -> str:
    """Returns the session cookie from cookie.txt, or prompts the user to enter it if it doesn't exist."""
    try:
        with open(_COOKIE_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        _update_session_cookie()
        return _get_session_cookie()


def _update_session_cookie() -> None:
    """Prompts the user to enter their session cookie and saves it to cookie.txt."""
    print("Please enter your session cookie:")
    cookie = input()
    with open(_COOKIE_PATH, "w") as f:
        f.write(cookie)


def _download_input(day: int, year: int, path: str) -> None:
    """Downloads the Advent of Code input for the given day and year and saves it to the given path.
    If the session cookie is invalid, prompts the user to enter a new one and tries again.

    :param day: the day of the Advent of Code puzzle
    :param year: the year of the Advent of Code puzzle
    :param path: the path to save the input to
    """
    cookies = {"session": _get_session_cookie()}
    headers = {"User-Agent": _USER_AGENT}
    url = _INPUT_URL.format(day=day, year=year)
    response = requests.get(url, cookies=cookies, headers=headers)
    text = response.text
    response.close()

    if text.startswith("Puzzle inputs differ by user."):
        _update_session_cookie()
        _download_input(day, year, path)
        return
    elif text.startswith("Please don't repeatedly request this endpoint"):
        print(f"[bold red]Rate limited. Wait at least 15 minutes before requesting the input again")
        text = ""
    else:
        print(f"[bold green]Successfully downloaded input for day {day}")

    with io.open(path, "w+", newline="\n") as f:
        f.write(text)


def _ensure_input_file(day: int, year: int, path: str) -> None:
    """Ensures that the input file exists for the given day and year and is valid.

    :param day: the day of the Advent of Code puzzle
    :param year: the year of the Advent of Code puzzle
    :param path: the path to save the input to
    """
    try:
        with open(path, "r") as f:
            text = f.read()
            if text == "":
                raise ValueError
    except (FileNotFoundError, ValueError):
        _download_input(day, year, path)


def get_aoc_input(day: int, year: int, path: Union[str, None] = None) -> Input:
    """Returns the Advent of Code input for the given day and year.
    If the input file doesn't exist, it is downloaded.

    :param day: the day of the Advent of Code puzzle
    :param year: the year of the Advent of Code puzzle
    :param path: the path to save the input to
    :return: the Advent of Code input
    """
    if path is None:
        path = _INPUT_PATH.format(day=day, year=year)

    _ensure_input_file(day, year, path)
    with open(path, "r") as f:
        return Input(f.read())
