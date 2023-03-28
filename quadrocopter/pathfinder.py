from queue import LifoQueue
from typing import Iterable, List

from quadrocopter.models import Point, Transmitter


class PathFinder:
    @staticmethod
    def exists_safe_path(start: Point, stop: Point, transmitters: List[Transmitter]) -> bool:
        """Check if there is a safe path between `start` and `stop` points, fully covered by transmitters range."""
        start_point_transmitters = PathFinder._find_covering_transmitters(start, transmitters)
        stop_point_transmitters = PathFinder._find_covering_transmitters(stop, transmitters)

        if not start_point_transmitters or not stop_point_transmitters:
            # there is no safe path, as start and/or stop point are not covered by transmitters
            return False

        return PathFinder._find_path(start_point_transmitters, stop_point_transmitters, transmitters)

    @staticmethod
    def _find_covering_transmitters(point: Point, transmitters: Iterable[Transmitter]) -> List[Transmitter]:
        """Return list of transmitters that cover given point."""
        return [t for t in transmitters if t.covers(point)]

    @staticmethod
    def _find_path(
        start_transmitters: Iterable[Transmitter],
        stop_transmitters: Iterable[Transmitter],
        all_transmitters: List[Transmitter],
    ) -> bool:
        """
        For given start transmitters and stop transmitters
        check if there is a chain of transmitters between them, that have overlapping range.

        Algorithm description (forward checking):
            1) store all starting transmitters as possible beginning of the path
            2) pick most recent element (path) from stack (LIFO queue) to forward check if it has valid continuation
            3) find all the transmitters that overlaps range of the last transmitter in current path
            4.1) if overlapping transmitters list contains any stop transmitters --> path exists, Done
            4.2) otherwise for every overlapping transmitters (o_transmitter):
                  - declare possible path as current path followed by o_transmitter
                  - put possible path at the top of the stack to further validation
            5) repeat 1-4 until find the correct path (3) or the stack will become empty
            6) empty stack means: all possible path were checked and any of them were valid, thus path not exists, Done


        Note: Using LIFO will allow quickly fall back to the latest possible path, that was not yet tested,
              as LIFO implementation is about picking the most recently stored item from the stack.
        """
        stack = LifoQueue()
        for t in start_transmitters:
            stack.put([t])

        while not stack.empty():
            current_path = stack.get()
            last_transmitter_in_path = current_path[-1]

            overlapping_transmitters = [
                t
                for t in all_transmitters
                if t not in current_path and t.has_intersection_with(last_transmitter_in_path)
            ]

            if any(t in overlapping_transmitters for t in stop_transmitters):
                return True

            for t in overlapping_transmitters:
                possible_path = current_path + [t]
                stack.put(possible_path)

        return False
