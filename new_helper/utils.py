from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING, Any, Iterable, TypeVar, overload

from rich import print

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

    _C = TypeVar("_C", bound=SupportsRichComparison)


_T = TypeVar("_T")
_T2 = TypeVar("_T2")


def digits(s: str) -> list[int]:
    """Returns a list of all digits in the given string.

    :param s: the string to parse
    :return: a list of all digits in the given string"""
    return list(map(int, filter(str.isdigit, s)))


def ints(s: str) -> list[int]:
    """Returns a list of all integers in the given string.

    :param s: the string to parse
    :return: a list of all integers in the given string"""
    return list(map(int, re.findall(r"[+-]?\d+", s)))


def floats(s: str) -> list[float]:
    """Returns a list of all floats in the given string.

    :param s: the string to parse
    :return: a list of all floats in the given string"""
    return list(map(float, re.findall(r"([\-+]?\d*(?:\d|\d\.|\.\d)\d*)", s)))


def flatten(l: list[list[_T]]) -> list[_T]:
    """Flattens a list of lists.

    :param l: the list to flatten
    :return: the flattened list"""
    return [item for sublist in l for item in sublist]


def flatten_full(l: list, max_depth=-1) -> list:
    """Flattens a list of lists recursively.

    :param l: the list to flatten
    :param max_depth: the maximum depth to flatten to
    :return: the flattened list"""
    if max_depth == 0:
        return l

    result = []
    for item in l:
        if isinstance(item, list):
            result.extend(flatten_full(item, max_depth - 1))
        else:
            result.append(item)

    return result


def distance(p1: tuple[int, ...], p2: tuple[int, ...]) -> float:
    """Returns the euclidian distance between two points."""
    return math.sqrt(sum((p1[i] - p2[i]) ** 2 for i in range(len(p1))))


def manhattan_distance(p1: tuple[int, ...], p2: tuple[int, ...]) -> int:
    """Returns the Manhattan distance between two points."""
    return sum(abs(p1[i] - p2[i]) for i in range(len(p1)))


def dot_product(v1: tuple[int, ...], v2: tuple[int, ...]) -> int:
    """Returns the dot product of two vectors."""
    return sum(v1[i] * v2[i] for i in range(len(v1)))


def sign(n: int) -> int:
    """Returns the sign of the given number.

    :param n: the number to get the sign of
    :return: the sign of the given number"""
    return (n > 0) - (n < 0)


def minmax(l: Iterable[_C]) -> tuple:
    """Returns the minimum and maximum values in the given iterable.

    :param l: the iterable to get the minimum and maximum values of
    :return: the minimum and maximum values in the given iterable"""
    return min(l), max(l)


def invert_dict(d: dict[_T, _T2]) -> dict[_T2, _T]:
    return {v: k for k, v in d.items()}


def sort(a, *args, **kwargs):
    """Sometimes I'm silly and I forget that I'm meant to .sort() a list."""
    return a.sort(*args, **kwargs)


@overload
def turn_right(d: tuple[int, int]) -> tuple[int, int]: ...


@overload
def turn_right(d: int, dy: int) -> tuple[int, int]: ...


def turn_right(d: int | tuple[int, int], dy: int | None = None) -> tuple[int, int]:
    if isinstance(d, tuple):
        dx, dy = d
    else:
        dx = d

    return dy * -1, dx  # type: ignore


@overload
def turn_left(d: tuple[int, int]) -> tuple[int, int]: ...


@overload
def turn_left(d: int, dy: int) -> tuple[int, int]: ...


def turn_left(d: int | tuple[int, int], dy: int | None = None) -> tuple[int, int]:
    if isinstance(d, tuple):
        dx, dy = d
    else:
        dx = d

    return dy, dx * -1  # type: ignore


clockwise = cw = tr = turn_right
counterclocwise = cclockwise = ccw = tl = turn_left


def _print_part(n: int, ans: Any) -> None:
    print(f"[bold green]Part {n}[/]: {ans}")


def print_part_1(ans: Any) -> None:
    """Prints the answer to part 1.

    :param ans: the answer to part 1"""
    _print_part(1, ans)


def print_part_2(ans: Any) -> None:
    """Prints the answer to part 2.

    :param ans: the answer to part 2"""
    _print_part(2, ans)


if __name__ == "__main__":
    assert digits("12d3.4") == [1, 2, 3, 4]
    assert ints("12d3.4") == [12, 3, 4]
    assert floats("12d3.4") == [12.0, 3.4]

    assert flatten([[1, 2], [[3, 4], 5]]) == [1, 2, [3, 4], 5]
    assert flatten_full([[1, 2], [[3, 4], 5]]) == [1, 2, 3, 4, 5]
    assert flatten_full([1, [2, [3, [4, [5]]]]]) == [1, 2, 3, 4, 5]
    assert flatten_full([1, [2, [3, [4, [5]]]]], 2) == [1, 2, 3, [4, [5]]]

    assert distance((0, 0), (1, 1)) == math.sqrt(2)
    assert manhattan_distance((0, 0), (1, 1)) == 2
    assert dot_product((1, 2, 3), (4, 5, 6)) == 4 + 10 + 18

    assert sign(10) == 1
    assert sign(-10) == -1
    assert sign(0) == 0
