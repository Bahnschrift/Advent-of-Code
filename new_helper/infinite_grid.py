from __future__ import annotations

from itertools import product, permutations
from typing import TYPE_CHECKING, Callable, Generic, Iterable, Iterator, TypeVar

from .grid import Grid
from .utils import minmax

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

_T = TypeVar("_T")
_MAX_PRETTY_PRINT_WIDTH = 80
_MAX_PRETTY_PRINT_HEIGHT = 100
_MAX_PRETTY_PRINT_DEPTH = 10


class _ItemDefaultDict(dict[tuple[int, ...], _T]):
    def __init__(self, default_factory: Callable[[tuple[int, ...]], _T]):
        super().__init__()
        self.default_factory = default_factory

    def __missing__(self, key: tuple[int, ...]) -> _T:
        if self.default_factory is None:
            raise KeyError(key)
        else:
            return self.default_factory(key)


class InfiniteGrid(Generic[_T]):
    _items: _ItemDefaultDict[_T]

    @staticmethod
    def from_grid(grid: Grid[_T], default: None | _T | Callable[[tuple[int, ...]], _T] = None):
        if callable(default):
            return InfiniteGrid(grid.items(), default)
        else:
            return InfiniteGrid(grid.items(), lambda _: default)

    @staticmethod
    def from_points(
        points: Iterable[tuple[int, ...]], point: _T, default: None | _T | Callable[[tuple[int, ...]], _T] = None
    ):
        if callable(default):
            return InfiniteGrid(((x, point) for x in points), default)
        else:
            return InfiniteGrid(((x, point) for x in points), lambda _: default)

    def __init__(
        self,
        items: Iterable[tuple[tuple[int, ...], _T]],
        default: _T | Callable[[tuple[int, ...]], _T] = None,
    ):
        if callable(default):
            self._items = _ItemDefaultDict(default)
        else:
            self._items = _ItemDefaultDict(lambda _: default)

        dim = -1
        for pos, value in items:
            if dim == -1:
                dim = len(pos)
            elif dim != len(pos):
                raise ValueError("all positions must be of the same dimension")

            self._items[pos] = value

    def __getitem__(self, key: tuple[int, ...]) -> _T:
        return self._items[key]

    def __setitem__(self, key: tuple[int, ...], value: _T):
        if self.dimension() > 0 and len(key) != self.dimension():
            raise TypeError("position must be of the same dimension as the grid")

        self._items[key] = value

    def __delitem__(self, key: tuple[int, ...]):
        del self._items[key]

    def __contains__(self, key: tuple[int, ...]) -> bool:
        return key in self._items

    def __eq__(self, other: InfiniteGrid[_T]) -> bool:
        return self._items == other._items

    def __str__(self) -> str:
        if self.dimension() == 0:
            return "InfiniteGrid()"

        return f"InfiniteGrid({self._items})"

    def dimension(self):
        if len(self._items) == 0:
            return 0

        return len(next(iter(self._items.keys())))

    def copy(self):
        return InfiniteGrid(self._items.items())

    def set_default(self, default: _T | Callable[[tuple[int, ...]], _T]):
        if callable(default):
            self._items.default_factory = default
        else:
            self._items.default_factory = lambda _: default

    def width(self) -> int:
        """Returns the width of the grid (first position argument)."""
        if self.dimension() < 1:
            return 0

        return max(x[0] for x in self._items.keys()) - min(x[0] for x in self._items.keys()) + 1

    def height(self) -> int:
        """Returns the height of the grid (second position argument)."""
        if self.dimension() < 2:
            return 0

        return max(x[1] for x in self._items.keys()) + 1

    def depth(self) -> int:
        """Returns the depth of the grid (third position argument)."""
        if self.dimension() < 3:
            return 0

        return max(x[2] for x in self._items.keys()) + 1

    def length(self, dim: int) -> int:
        """Returns the length of the grid along the given dimension."""
        if self.dimension() < dim + 1:
            return 0

        return max(x[dim] for x in self._items.keys()) + 1

    def positions(self) -> Iterator[tuple[int, ...]]:
        """Returns an iterator over all positions in the grid."""
        return iter(self._items.keys())

    def values(self) -> Iterator[_T]:
        """Returns an iterator over all values in the grid."""
        return iter(self._items.values())

    def items(self) -> Iterator[tuple[tuple[int, ...], _T]]:
        """Returns an iterator over all positions and values in the grid."""
        return iter(self._items.items())

    def _pretty_layer(self, pos: tuple[int, ...] = ()) -> str:
        assert self.dimension() >= 2
        layer = []
        min_x = min(x[0] for x in self._items.keys() if x[2:] == pos)
        max_x = max(x[0] for x in self._items.keys() if x[2:] == pos)
        min_y = min(x[1] for x in self._items.keys() if x[2:] == pos)
        max_y = max(x[1] for x in self._items.keys() if x[2:] == pos)

        for y in range(min_y, max_y + 1):
            layer.append([self[(x, y) + pos] for x in range(min_x, max_x + 1)])

        y_axis_width = max(len(str(max_y)), len(str(min_y)))
        x_axis_height = max(len(str(max_x)), len(str(min_x)))
        column_widths = [max(*(len(str(i)) for i in column), 1) for column in zip(*layer)]

        # Should print x axis labels vertically
        s = ""
        for i in range(x_axis_height - 1, -1, -1):
            s += " " * (y_axis_width + 2) + "| "
            for x in range(min_x, max_x + 1):
                if len(str(x)) > i:
                    s += f"{str(x)[-i - 1]:>{column_widths[x - min_x]}} "
                else:
                    s += " " * column_widths[x - min_x] + " "
            s += " \n"

        s += "-" + "-" * y_axis_width + "-+-" + "-".join("-" * w for w in column_widths) + "\n"
        for y in range(min_y, max_y + 1):
            s += f" {y:>{y_axis_width}} | "
            s += " ".join(f"{x:>{w}}" for x, w in zip(layer[y - min_y], column_widths))
            s += "\n"

        return s

    def pretty(
        self,
        max_width: int = _MAX_PRETTY_PRINT_WIDTH,
        max_height: int = _MAX_PRETTY_PRINT_HEIGHT,
        max_depth: int = _MAX_PRETTY_PRINT_DEPTH,
    ) -> str:
        """Returns a pretty-printed string representation of the grid.

        `1D:`
        ```text
         -1  0    2    3
        -----------------
          1 22 None 4444
        ```

        `2D:`
        ```text
            |  -
            |  1  0    2    3
        ----+-----------------
         -1 |  a  b    d    e
          0 |  1 22 None 4444
          2 |  1 22 None 4444
        ```
        """
        if self.dimension() < 1:
            return "InfiniteGrid()"

        if (
            self.dimension() == 1
            or self.dimension() > 3
            or self.width() > max_width
            or self.height() > max_height
            or self.depth() > max_depth
        ):
            return f"InfiniteGrid({self._items})"

        if self.dimension() == 2:
            return self._pretty_layer()

        s = ""
        min_z = min(x[2] for x in self._items.keys())
        max_z = max(x[2] for x in self._items.keys())

        for z in range(min_z, max_z + 1):
            s += f"z={z}\n"
            s += self._pretty_layer((z,))
            s += "\n"

        return s

    def get_pos(self, value: _T):
        """Returns the position of the given value in the grid."""
        return next(x[0] for x in self._items.items() if x[1] == value)

    def bounds(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Returns the minimum and maximum positions in the grid."""
        if self.dimension() < 1:
            return ((), ())

        min_pos = tuple(min(x[i] for x in self._items.keys()) for i in range(self.dimension()))
        max_pos = tuple(max(x[i] for x in self._items.keys()) for i in range(self.dimension()))
        return (min_pos, max_pos)

    def max_value(self, key: Callable[[_T], SupportsRichComparison] | None = None) -> _T:
        """Returns the maximum value in the grid."""
        return max(self._items.values(), key=key)  # type: ignore

    def max_position(self, key: Callable[[_T], SupportsRichComparison] | None = None) -> tuple[int, ...]:
        """Returns the position of the maximum value in the grid."""
        return self.get_pos(self.max_value(key))

    def min_value(self, key: Callable[[_T], SupportsRichComparison] | None = None) -> _T:
        """Returns the minimum value in the grid."""
        return min(self._items.values(), key=key)  # type: ignore

    def min_position(self, key: Callable[[_T], SupportsRichComparison] | None = None) -> tuple[int, ...]:
        """Returns the position of the minimum value in the grid."""
        return self.get_pos(self.min_value(key))

    def transposed(self) -> InfiniteGrid[_T]:
        """Returns a transposed copy of the grid."""
        return InfiniteGrid(((pos[::-1], v) for pos, v in self.items()))

    def transpose(self) -> None:
        """Transposes the grid in place."""
        self._items = self.transposed()._items

    def adjacent_orth_posititions(self, pos: tuple[int, ...]) -> list[tuple[int, ...]]:
        """Returns the positions adjacent to the given position in the orthogonal directions."""
        return [
            x for x in self.adjacent_positions(pos) if sum(abs(x[i] - pos[i]) for i in range(self.dimension())) == 1
        ]

    def adjacent_orth_values(self, pos: tuple[int, ...]) -> list[_T]:
        """Returns the values adjacent to the given position in the orthogonal directions."""
        return [self[x] for x in self.adjacent_orth_posititions(pos)]

    def adjacent_orth_items(self, pos: tuple[int, ...]) -> list[tuple[tuple[int, ...], _T]]:
        """Returns the items adjacent to the given position in the orthogonal directions."""
        return [(x, self[x]) for x in self.adjacent_orth_posititions(pos)]

    def adjacent_positions(self, pos: tuple[int, ...]) -> list[tuple[int, ...]]:
        """Returns the positions adjacent to the given position in all directions."""
        directions = product((0, 1, -1), repeat=self.dimension())
        next(directions)
        return [tuple(x + y for x, y in zip(pos, d)) for d in directions]

    def adjacent_values(self, pos: tuple[int, ...]) -> list[_T]:
        """Returns the values adjacent to the given position in all directions."""
        return [self[x] for x in self.adjacent_positions(pos)]

    def adjacent_items(self, pos: tuple[int, ...]) -> list[tuple[tuple[int, ...], _T]]:
        """Returns the items adjacent to the given position in all directions."""
        return [(x, self[x]) for x in self.adjacent_positions(pos)]


def _test_infinite_grid():
    grid = InfiniteGrid.from_grid(Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]), lambda pos: " ")
    assert grid[0, 0] == 1
    assert grid[1, 0] == 2

    assert grid.width() == 3
    assert grid.height() == 4
    assert grid.depth() == 0
    assert grid.length(0) == 3
    assert grid.length(5) == 0

    # del grid[1, 0]
    # del grid[0, 3]

    # grid[-1, -2] = 10

    # grid = InfiniteGrid(
    #     [
    #         ((0, 0, 0), "#"),
    #         ((1, 0, 0), "#"),
    #         ((-1, 0, 0), "#"),
    #         ((0, 1, 0), "#"),
    #         ((0, -1, 0), "#"),
    #         ((0, 0, 1), "#"),
    #         ((0, 0, -1), "#"),
    #         # ((-10, 10, 2), "#"),
    #     ],
    #     default=" ",
    # )

    new_grid = InfiniteGrid(list(map(lambda pos: ((pos[0] - 2, pos[1] - 2), grid[pos]), grid.positions())), default=" ")
    print(new_grid.pretty())

    # assert grid[0, 0, 0] == "#"
    # assert grid.adjacent_orth_values((0, 0, 0)) == ["#", "#", "#", "#", "#", "#"]
