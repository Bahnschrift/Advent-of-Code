from typing import Iterator


Point = tuple[int, int]

class Polygon:
    points: list[Point]

    def __init__(self, points: list[Point]) -> None:
        self.points = points
    
    def __repr__(self) -> str:
        return f"Polygon({self.points})"

    def __iter__(self) -> Iterator[Point]:
        return iter(self.points)

    def __len__(self) -> int:
        return len(self.points)

    def add_point(self, point: Point) -> None:
        self.points.append(point)

    def perimeter(self) -> int:
        """
        Assumes exclusively horizontal and vertical lines
        """
        p = 0
        for (x1, x2), (y1, y2) in zip(self.points, self.points[1:]):
            p += abs(x1 - x2) + abs(y1 - y2)  # Shoelace formula

        return p

    def area_internal(self) -> int:
        """
        Assumes exclusively horizontal and vertical lines
        """
        a = 0
        for (x1, x2), (y1, y2) in zip(self.points, self.points[1:]):
            a += abs(x1 - x2) * abs(y1 - y2)

        return a // 2

    def area(self) -> int:
        """
        Assumes exclusively horizontal and vertical lines
        """
        return self.area_internal() + self.perimeter() + 1  # Pick's theorem
