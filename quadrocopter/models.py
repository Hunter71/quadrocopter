from dataclasses import dataclass
from math import pow, sqrt
from typing import List, Tuple


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Transmitter:
    x: int
    y: int
    m: int

    def has_intersection_with(self, other: "Transmitter") -> bool:
        distance = sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))
        return distance <= self.m + other.m

    def covers(self, point: Point) -> bool:
        dist_x = abs(self.x - point.x)
        dist_y = abs(self.y - point.y)
        return dist_x <= self.m and dist_y <= self.m and pow(dist_x, 2) + pow(dist_y, 2) <= pow(self.m, 2)


InputData = Tuple[Point, Point, List[Transmitter]]
