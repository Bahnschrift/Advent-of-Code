from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, Iterator, Sequence, TypeVar, overload

from .constants import *

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

_T = TypeVar("_T")
_U = TypeVar("_U")


class Grid(Generic[_T]):
    """A 2D grid of elements.

    All indexing is 0-based, in the form `(x, y)`.
    For example, the element to the right of the top left is given by `(1, 0)`.

    Slices can also be used for indexing, also in the form `(x, y)`.
    The `x` slice places a restriction of the columns (the x values) of the grid,
    while the `y` slice places a restriction on the rows (the y values) of the grid.
    For example, the first column of the grid is given by `(0, :)`,
    and everything but the first row is given by `(:, 1:)`.

    Note that `position` refers to an `(x, y)` pair, `value` refers the value at a position,
    and `item` refers to a `(position, value)` pair.
    """

    _grid: list[list[_T]]
    width: int
    height: int

    @staticmethod
    def of_size(width: int, height: int, default: _T) -> Grid[_T]:
        """Returns a grid of the given size, filled with the default value."""
        return Grid([[default] * width for _ in range(height)])

    @staticmethod
    def from_sequence(sequence: Sequence[_T], width: int) -> Grid[_T]:
        """Returns a grid of the given size, filled with the values from the iterable."""
        if len(sequence) % width != 0:
            raise ValueError("Sequence length must be a multiple of width")

        return Grid([list(sequence[i : i + width]) for i in range(0, len(sequence), width)])

    def __init__(self, grid: Sequence[Sequence[_T]], default: _T | None = None) -> None:
        if len(grid) == 0:
            raise ValueError("Grid cannot be empty")

        if all(len(row) == len(grid[0]) for row in grid):
            self._grid = [list(row) for row in grid]
        elif default is not None:
            max_width = max(len(row) for row in grid)
            self._grid = [list(row) + [default] * (max_width - len(row)) for row in grid]
        else:
            raise ValueError("Grid must have consistent width or specify a default value")

        self.width = len(self._grid[0])
        self.height = len(self._grid)

    @overload
    def __getitem__(self, index: tuple[int, int]) -> _T:
        """Returns the element at the given (x, y) coordinate."""
        ...

    @overload
    def __getitem__(self, index: tuple[int, slice]) -> list[_T]:
        """Returns a slice of the ith row of the grid."""
        ...

    @overload
    def __getitem__(self, index: tuple[slice, int]) -> list[_T]:
        """Returns a slice of the ith column of the grid."""
        ...

    @overload
    def __getitem__(self, index: tuple[slice, slice]) -> list[list[_T]]:
        """Returns a slice of the grid."""
        ...

    def __getitem__(self, index: tuple[int | slice, int | slice]) -> _T | list[_T] | list[list[_T]]:
        x, y = index
        if isinstance(x, int) and isinstance(y, int):
            return self._grid[y][x]

        if isinstance(x, slice) and isinstance(y, slice):
            return [row[x] for row in self._grid[y]]

        if isinstance(x, int) and isinstance(y, slice):
            return [row[x] for row in self._grid[y]]

        if isinstance(x, slice) and isinstance(y, int):
            return self._grid[y][x]

        raise TypeError(f"invalid index types: {type(x)}, {type(y)}")

    @overload
    def __setitem__(self, index: tuple[int, int], value: _T) -> None:
        """Sets the element at the given (x, y) coordinate."""
        ...

    @overload
    def __setitem__(self, index: tuple[int, slice], value: Sequence[_T]) -> None:
        """Sets a slice of the ith column of the grid."""
        ...

    @overload
    def __setitem__(self, index: tuple[slice, int], value: Sequence[_T]) -> None:
        """Sets a slice of the ith row of the grid."""
        ...

    @overload
    def __setitem__(self, index: tuple[slice, slice], value: Sequence[Sequence[_T]]) -> None:
        """Sets a slice of the grid."""
        ...

    def __setitem__(
        self, index: tuple[int | slice, int | slice], value: _T | Sequence[_T] | Sequence[Sequence[_T]]
    ) -> None:
        x, y = index
        if isinstance(x, int) and isinstance(y, int):
            self._grid[y][x] = value  # type: ignore since we cannot type check generics at runtime
            return

        elif isinstance(x, slice) and isinstance(y, slice):
            if not isinstance(value, Sequence):
                raise TypeError("can only assign an sequence of sequences")

            if not all(isinstance(row, Sequence) for row in list(value)):
                raise TypeError("can only assign a sequence of sequences")

            if len(value) != len(self[0, y]):
                raise ValueError(f"cannot assign a sequence of different length ({len(value)} != {len(self[x, 0])})")

            if not all(len(row) == len(self[x, 0]) for row in value):  # type: ignore
                raise ValueError("cannot assign a sequence of different length")

            for i, row in enumerate(self._grid[y]):
                row[x] = value[i]  # type: ignore

            return

        elif isinstance(x, int) and isinstance(y, slice):
            if not isinstance(value, Sequence):
                raise TypeError("can only assign a sequence")

            if len(value) != len(self[0, y]):
                raise ValueError(f"cannot assign a sequence of different length ({len(value)} != {len(self[0, y])})")

            for i, row in enumerate(self._grid[y]):
                row[x] = value[i]  # type: ignore

            return

        elif isinstance(x, slice) and isinstance(y, int):
            if not isinstance(value, Sequence):
                raise TypeError("can only assign a sequence")

            if len(value) != len(self[x, 0]):
                raise ValueError(f"cannot assign a sequence of different length ({len(value)} != {len(self[x, 0])})")

            self._grid[y][x] = value  # type: ignore since we cannot type check generics at runtime
            return

        raise TypeError(f"invalid index types: {type(x)}, {type(y)}")

    def __str__(self) -> str:
        return "\n".join(map(str, self._grid))

    def __repr__(self) -> str:
        return "Grid(\n\t" + "\n\t".join(map(repr, self._grid)) + "\n)"

    def __eq__(self, other: object) -> bool:
        """Grids are equal if they have the same width, height, and elements."""
        if not isinstance(other, Grid):
            return False

        if self.width != other.width or self.height != other.height:
            return False

        for x, y in self.positions():
            if self[x, y] != other[x, y]:
                return False

        return True

    def __ne__(self, __o: object) -> bool:
        return not self == __o

    def _binary_operation(self, other: Grid | Any, operation: Callable[[_T, Any], Any]) -> Grid[_T]:
        if isinstance(other, Grid):
            if self.width != other.width or self.height != other.height:
                raise ValueError(
                    "cannot perform binary operation on grids of different sizes"
                    + f" ({self.width} x {self.height}) and ({other.width} x {other.height})"
                )
            return self.mapped_positions(lambda x, y: operation(self[x, y], other[x, y]))

        return self.mapped_positions(lambda x, y: operation(self[x, y], other))

    def _inplace_binary_operation(self, other: Grid | Any, operation: Callable[[_T, Any], Any]) -> None:
        if isinstance(other, Grid):
            if self.width != other.width or self.height != other.height:
                raise ValueError(
                    "cannot perform binary operation on grids of different sizes"
                    + f" ({self.width} x {self.height}) and ({other.width} x {other.height})"
                )
            for x, y in self.positions():
                self[x, y] = operation(self[x, y], other[x, y])
            return

        for x, y in self.positions():
            self[x, y] = operation(self[x, y], other)

    @overload
    def __add__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __add__(self, other: _T) -> Grid[_T]:
        ...

    def __add__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a + b)

    @overload
    def __iadd__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __iadd__(self, other: _T) -> Grid[_T]:
        ...

    def __iadd__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a + b)
        return self

    @overload
    def __sub__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __sub__(self, other: _T) -> Grid[_T]:
        ...

    def __sub__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a - b)

    @overload
    def __isub__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __isub__(self, other: _T) -> Grid[_T]:
        ...

    def __isub__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a - b)
        return self

    @overload
    def __mul__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __mul__(self, other: _T) -> Grid[_T]:
        ...

    def __mul__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a * b)

    @overload
    def __imul__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __imul__(self, other: _T) -> Grid[_T]:
        ...

    def __imul__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a * b)
        return self

    @overload
    def __truediv__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __truediv__(self, other: _T) -> Grid[_T]:
        ...

    def __truediv__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a / b)

    @overload
    def __itruediv__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __itruediv__(self, other: _T) -> Grid[_T]:
        ...

    def __itruediv__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a / b)
        return self

    @overload
    def __floordiv__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __floordiv__(self, other: _T) -> Grid[_T]:
        ...

    def __floordiv__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a // b)

    @overload
    def __ifloordiv__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __ifloordiv__(self, other: _T) -> Grid[_T]:
        ...

    def __ifloordiv__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a // b)
        return self

    @overload
    def __mod__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __mod__(self, other: _T) -> Grid[_T]:
        ...

    def __mod__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a % b)

    @overload
    def __imod__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __imod__(self, other: _T) -> Grid[_T]:
        ...

    def __imod__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a % b)
        return self

    @overload
    def __pow__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __pow__(self, other: _T) -> Grid[_T]:
        ...

    def __pow__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a**b)

    @overload
    def __ipow__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __ipow__(self, other: _T) -> Grid[_T]:
        ...

    def __ipow__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a**b)
        return self

    @overload
    def __lshift__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __lshift__(self, other: _T) -> Grid[_T]:
        ...

    def __lshift__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a << b)

    @overload
    def __ilshift__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __ilshift__(self, other: _T) -> Grid[_T]:
        ...

    def __ilshift__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a << b)
        return self

    @overload
    def __rshift__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __rshift__(self, other: _T) -> Grid[_T]:
        ...

    def __rshift__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a >> b)

    @overload
    def __irshift__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __irshift__(self, other: _T) -> Grid[_T]:
        ...

    def __irshift__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a >> b)
        return self

    @overload
    def __and__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __and__(self, other: _T) -> Grid[_T]:
        ...

    def __and__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a & b)

    @overload
    def __iand__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __iand__(self, other: _T) -> Grid[_T]:
        ...

    def __iand__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a & b)
        return self

    @overload
    def __xor__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __xor__(self, other: _T) -> Grid[_T]:
        ...

    def __xor__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a ^ b)

    @overload
    def __ixor__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __ixor__(self, other: _T) -> Grid[_T]:
        ...

    def __ixor__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a ^ b)
        return self

    @overload
    def __or__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __or__(self, other: _T) -> Grid[_T]:
        ...

    def __or__(self, other: Grid | Any) -> Grid[_T]:
        return self._binary_operation(other, lambda a, b: a | b)

    @overload
    def __ior__(self, other: Grid[_T]) -> Grid[_T]:
        ...

    @overload
    def __ior__(self, other: _T) -> Grid[_T]:
        ...

    def __ior__(self, other: Grid | Any) -> Grid[_T]:
        self._inplace_binary_operation(other, lambda a, b: a | b)
        return self

    def __neg__(self) -> Grid[_T]:
        return self.mapped_values(lambda v: -v)  # type: ignore

    def __pos__(self) -> Grid[_T]:
        return self.mapped_values(lambda v: +v)  # type: ignore

    def __abs__(self) -> Grid[_T]:
        return self.mapped_values(lambda v: abs(v))  # type: ignore

    def __invert__(self) -> Grid[_T]:
        return self.mapped_values(lambda v: ~v)  # type: ignore

    def __len__(self) -> int:
        return self.width * self.height

    def __contains__(self, value: _T) -> bool:
        """Returns whether the given item is in the grid."""
        return any(value == v for v in self.values())

    def positions(self) -> Iterator[tuple[int, int]]:
        """Returns an iterator over all positions in the grid, left to right, then top to bottom."""
        for y in range(self.height):
            for x in range(self.width):
                yield x, y

    def values(self) -> Iterator[_T]:
        """Returns an iterator over all values in the grid, left to right, then top to bottom."""
        for x, y in self.positions():
            yield self[x, y]

    def items(self) -> Iterator[tuple[tuple[int, int], _T]]:
        """Returns an iterator over all positions and values in the grid, left to right, then top to bottom."""
        for x, y in self.positions():
            yield (x, y), self[x, y]

    def copy(self) -> Grid[_T]:
        """Returns a copy of the grid."""
        return Grid(self._grid)  # Since the Grid constructor itself copies the given list, this is sufficient.

    def mapped_values(self, func: Callable[[_T], _U]) -> Grid[_U]:
        """Returns a new grid with the given function applied to every value in the grid."""
        return Grid.from_sequence([func(i) for i in self.values()], self.width)

    def mapped_positions(self, func: Callable[[int, int], _U]) -> Grid[_U]:
        """Returns a new grid with the given function applied to every position in the grid."""
        return Grid.from_sequence([func(x, y) for x, y in self.positions()], self.width)

    def mapped_items(self, func: Callable[[tuple[int, int], _T], _U]) -> Grid[_U]:
        """Returns a new grid with the given function applied to every position and value in the grid."""
        return Grid.from_sequence([func(pos, i) for pos, i in self.items()], self.width)

    def row(self, y: int) -> list[_T]:
        """Returns the row at the given y position."""
        return self[:, y]

    def col(self, x: int) -> list[_T]:
        """Returns the column at the given x position."""
        return self[x, :]

    def pretty(self) -> str:
        """Returns a pretty string representation of the grid in the following format:
        ```text
           | 0  1  2  3  4
        ---+----------------
         0 |  1  2  3  4  5
         1 |  6  7  8  9 10
         3 | 11 12 13 14 15
         4 | 16 17 18 19 20
        ```
        """
        y_axis_width = len(str(self.height - 1))
        s = " " * (y_axis_width + 2) + "| "

        column_widths = [max(*(len(str(i)) for i in self.col(x)), len(str(x))) for x in range(self.width)]
        s += " ".join(f"{i:>{width}}" for i, width in enumerate(column_widths))
        s += "\n"

        s += "-" * (y_axis_width + 2) + "+-" + "-".join("-" * width for width in column_widths) + "\n"

        for y in range(self.height):
            s += f" {y:>{y_axis_width}} | "
            s += " ".join(f"{i:>{width}}" for i, width in zip(self.row(y), column_widths))
            s += "\n"

        return s

    def in_bounds(self, x: int, y: int) -> bool:
        """Returns whether the given position is in the grid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def adjacent_4_positions(self, x: int, y: int) -> list[tuple[int, int]]:
        """Returns the 4 adjacent positions to the given position."""
        return [(x + dx, y + dy) for dx, dy in ADJACENT_4 if self.in_bounds(x + dx, y + dy)]

    def adjacent_4_values(self, x: int, y: int) -> list[_T]:
        """Returns the 4 adjacent values to the given position."""
        return [self[x + dx, y + dy] for dx, dy in ADJACENT_4 if self.in_bounds(x + dx, y + dy)]

    def adjacent_4_items(self, x: int, y: int) -> list[tuple[tuple[int, int], _T]]:
        """Returns the 4 adjacent positions and values to the given position."""
        return [((x + dx, y + dy), self[x + dx, y + dy]) for dx, dy in ADJACENT_4 if self.in_bounds(x + dx, y + dy)]

    def adjacent_5_positions(self, x: int, y: int) -> list[tuple[int, int]]:
        """Returns the 5 adjacent positions to the given position."""
        return [(x + dx, y + dy) for dx, dy in ADJACENT_5 if self.in_bounds(x + dx, y + dy)]

    def adjacent_5_values(self, x: int, y: int) -> list[_T]:
        """Returns the 5 adjacent values to the given position."""
        return [self[x + dx, y + dy] for dx, dy in ADJACENT_5 if self.in_bounds(x + dx, y + dy)]

    def adjacent_5_items(self, x: int, y: int) -> list[tuple[tuple[int, int], _T]]:
        """Returns the 5 adjacent positions and values to the given position."""
        return [((x + dx, y + dy), self[x + dx, y + dy]) for dx, dy in ADJACENT_5 if self.in_bounds(x + dx, y + dy)]

    def adjacent_8_positions(self, x: int, y: int) -> list[tuple[int, int]]:
        """Returns the 8 adjacent positions to the given position."""
        return [(x + dx, y + dy) for dx, dy in ADJACENT_8 if self.in_bounds(x + dx, y + dy)]

    def adjacent_8_values(self, x: int, y: int) -> list[_T]:
        """Returns the 8 adjacent values to the given position."""
        return [self[x + dx, y + dy] for dx, dy in ADJACENT_8 if self.in_bounds(x + dx, y + dy)]

    def adjacent_8_items(self, x: int, y: int) -> list[tuple[tuple[int, int], _T]]:
        """Returns the 8 adjacent positions and values to the given position."""
        return [((x + dx, y + dy), self[x + dx, y + dy]) for dx, dy in ADJACENT_8 if self.in_bounds(x + dx, y + dy)]

    def adjacent_9_positions(self, x: int, y: int) -> list[tuple[int, int]]:
        """Returns the 9 adjacent positions to the given position."""
        return [(x + dx, y + dy) for dx, dy in ADJACENT_9 if self.in_bounds(x + dx, y + dy)]

    def adjacent_9_values(self, x: int, y: int) -> list[_T]:
        """Returns the 9 adjacent values to the given position."""
        return [self[x + dx, y + dy] for dx, dy in ADJACENT_9 if self.in_bounds(x + dx, y + dy)]

    def adjacent_9_items(self, x: int, y: int) -> list[tuple[tuple[int, int], _T]]:
        """Returns the 9 adjacent positions and values to the given position."""
        return [((x + dx, y + dy), self[x + dx, y + dy]) for dx, dy in ADJACENT_9 if self.in_bounds(x + dx, y + dy)]

    def append_row(self, row: list[_T]) -> None:
        """Appends the given row to the grid."""
        if len(row) != self.width:
            raise ValueError("Row length must match grid width.")
        self._grid.append(row)
        self.height += 1

    def append_col(self, col: list[_T]) -> None:
        """Appends the given column to the grid."""
        if len(col) != self.height:
            raise ValueError("Column length must match grid height.")
        for i, v in enumerate(col):
            self._grid[i].append(v)
        self.width += 1

    def insert_row(self, y: int, row: list[_T]) -> None:
        """Inserts the given row at the given y position."""
        if len(row) != self.width:
            raise ValueError("Row length must match grid width.")
        self._grid.insert(y, row)
        self.height += 1

    def insert_col(self, x: int, col: list[_T]) -> None:
        """Inserts the given column at the given x position."""
        if len(col) != self.height:
            raise ValueError("Column length must match grid height.")
        for i, v in enumerate(col):
            self._grid[i].insert(x, v)
        self.width += 1

    def extend_rows(self, rows: list[list[_T]]) -> None:
        """Extends the grid with the given rows."""
        for row in rows:
            self.append_row(row)

    def extend_cols(self, cols: list[list[_T]]) -> None:
        """Extends the grid with the given columns."""
        for col in cols:
            self.append_col(col)

    def extend_right(self, grid: Grid[_T]) -> None:
        """Extends the grid to the right with the given grid."""
        if self.height != grid.height:
            raise ValueError("Grids must have the same height.")
        for y in range(self.height):
            self._grid[y].extend(grid._grid[y])
        self.width += grid.width

    def extend_down(self, grid: Grid[_T]) -> None:
        """Extends the grid downwards with the given grid."""
        if self.width != grid.width:
            raise ValueError("Grids must have the same width.")
        self._grid.extend(grid._grid)
        self.height += grid.height

    def delete_row(self, y: int) -> None:
        """Deletes the row at the given y position."""
        del self._grid[y]
        self.height -= 1

    def delete_col(self, x: int) -> None:
        """Deletes the column at the given x position."""
        for row in self._grid:
            del row[x]
        self.width -= 1

    def prepend_row(self, row: list[_T]) -> None:
        """Prepends the given row to the grid."""
        self.insert_row(0, row)

    def prepend_col(self, col: list[_T]) -> None:
        """Prepends the given column to the grid."""
        self.insert_col(0, col)

    def pop_row(self, y: int = -1) -> list[_T]:
        """Pops the row at the given y position."""
        row = self._grid.pop(y)
        self.height -= 1
        return row

    def pop_col(self, x: int = -1) -> list[_T]:
        """Pops the column at the given x position."""
        col = [row.pop(x) for row in self._grid]
        self.width -= 1
        return col

    def get_pos(self, value: _T) -> tuple[int, int]:
        """Returns the position of the given value."""
        for pos, v in self.items():
            if v == value:
                return pos

        raise ValueError(f"{value} not in grid.")

    def replace(self, old: _T, new: _T, count: int = -1) -> None:
        """Replaces all occurrences of the given value with the new value.
        If a count is given, only that many occurrences will be replaced."""
        for pos, v in self.items():
            if v == old:
                self[pos] = new
                count -= 1
                if count == 0:
                    return

    def replaced(self, old: _T, new: _T, count: int = -1) -> Grid[_T]:
        """Returns a new grid with all occurrences of the given value replaced with the new value.
        If a count is given, only that many occurrences will be replaced."""
        new_grid = self.copy()
        new_grid.replace(old, new, count)
        return new_grid

    def count(self, value: _T) -> int:
        """Returns the number of occurrences of the given value."""
        return sum(v == value for v in self.values())

    def max_value(self, key: Callable[[_T], SupportsRichComparison] | None = None) -> _T:
        """Returns the maximum value in the grid."""
        return max(self.values(), key=key)  # type: ignore

    def max_position(self, key: Callable[[_T], SupportsRichComparison] | None = None) -> tuple[int, int]:
        """Returns the position of the maximum value in the grid."""
        return self.get_pos(self.max_value(key))

    def min_value(self, key: Callable[[_T], SupportsRichComparison] | None = None) -> _T:
        """Returns the minimum value in the grid."""
        return min(self.values(), key=key)  # type: ignore

    def min_position(self, key: Callable[[_T], SupportsRichComparison] | None = None) -> tuple[int, int]:
        """Returns the position of the minimum value in the grid."""
        return self.get_pos(self.min_value(key))

    def transposed(self) -> Grid[_T]:
        """Returns a transposed copy of the grid."""
        return Grid(list(zip(*self._grid)))

    def transpose(self) -> None:
        """Transposes the grid."""
        self._grid = self.transposed()._grid
        self.width, self.height = self.height, self.width

    def flipped_x(self) -> Grid[_T]:
        """Returns a copy of the grid across the X axis."""
        return Grid(self._grid[::-1])

    def flip_x(self) -> None:
        """Flips the grid across the X axis."""
        self._grid = self.flipped_x()._grid

    def flipped_y(self) -> Grid[_T]:
        """Returns a copy of the grid across the Y axis."""
        return Grid([row[::-1] for row in self._grid])

    def flip_y(self) -> None:
        """Flips the grid across the Y axis."""
        self._grid = self.flipped_y()._grid

    def rotated(self, n: int = 1) -> Grid[_T]:
        """Rotates the grid clockwise n times."""
        n %= 4
        if n == 0:
            return self.copy()
        else:
            return self.transposed().flipped_y().rotated(n - 1)

    def rotate(self, n: int = 1) -> None:
        """Rotates the grid by the given number of times."""
        self._grid = self.rotated(n)._grid

    def rotatations(self) -> Iterator[Grid[_T]]:
        """Returns an iterator of all possible rotations of the grid."""
        last = self
        for _ in range(3):
            yield last
            last = last.rotated()
        yield last

    def permutations(self) -> Iterator[Grid[_T]]:
        """Returns an iterator of all possible permutations of the grid."""
        for rotation in self.rotatations():
            yield rotation
            yield rotation.flipped_y()

    def bounds(self) -> tuple[int, int, int, int]:
        """Returns the bounds of the grid as a tuple of (x, y, width, height)."""
        return 0, 0, self.width, self.height


def _test_grid():
    # Some sanity tests

    create_test_grid = lambda: Grid(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
    )
    test_grid = create_test_grid()

    assert test_grid[:, 0] == [1, 2, 3]
    assert test_grid[0, :] == [1, 4, 7]
    assert test_grid[:, :] == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    assert test_grid[1:, 0] == [2, 3]
    assert test_grid[0, 1:] == [4, 7]
    assert test_grid[-1, :] == [3, 6, 9]

    assert test_grid[1:, 1:] == [[5, 6], [8, 9]]
    assert test_grid[:, 1:] == [[4, 5, 6], [7, 8, 9]]
    assert test_grid[1:, :] == [[2, 3], [5, 6], [8, 9]]
    assert test_grid[-2:, -2:] == [[5, 6], [8, 9]]

    assert test_grid[0, 0] == 1
    assert test_grid[1, 0] == 2
    assert test_grid[2, 0] == 3
    assert test_grid[0, 1] == 4

    test_grid[1:, :] = [[12, 13], [15, 16], [18, 19]]
    assert test_grid[1:, :] == [[12, 13], [15, 16], [18, 19]]

    test_grid = create_test_grid()
    test_grid[0, 1:] = [14, 17]
    assert test_grid[0, 1:] == [14, 17]

    test_grid = create_test_grid()
    test_grid[1:, 0] = [12, 13]
    assert test_grid[1:, 0] == [12, 13]

    test_grid = create_test_grid()
    test_grid[0, 0] = 10
    assert test_grid[0, 0] == 10

    assert 10 in test_grid

    test_grid = create_test_grid()
    test_grid += 1
    assert test_grid == Grid([[2, 3, 4], [5, 6, 7], [8, 9, 10]])

    test_grid += create_test_grid()
    assert test_grid == Grid([[3, 5, 7], [9, 11, 13], [15, 17, 19]])
    test_grid **= 2
    assert test_grid == Grid([[9, 25, 49], [81, 121, 169], [225, 289, 361]])

    test_grid = create_test_grid()
    test_grid = -test_grid
    assert test_grid == Grid([[-1, -2, -3], [-4, -5, -6], [-7, -8, -9]])

    test_grid = create_test_grid()
    assert test_grid.row(1) == [4, 5, 6]
    assert test_grid.col(1) == [2, 5, 8]

    test_grid.insert_row(1, [12, 13, 14])
    assert test_grid.get_pos(9) == (2, 3)

    assert test_grid.count(9) == 1
    assert test_grid.max_value() == 14
    assert test_grid.max_value(key=lambda v: -v + 3) == 1
    assert test_grid.min_value() == 1

    test_grid = create_test_grid()
    test_grid.rotate()
    assert test_grid == Grid([[7, 4, 1], [8, 5, 2], [9, 6, 3]])

    test_grid.rotate(2)
    assert test_grid == Grid([[3, 6, 9], [2, 5, 8], [1, 4, 7]])

    assert create_test_grid().transposed() in create_test_grid().permutations()

    test_grid = Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9], ["a", "b", "c"]])

    # test_grid = create_test_grid()
    # test_grid.insert_col(1, [12, 13, 14])
    # test_grid.append_row([150, 16, 17, 18])
    print(test_grid.pretty())
    # print(Grid(test_grid.pretty().splitlines()).pretty())
    # print(Grid(test_grid[2:, 1:]).pretty())
