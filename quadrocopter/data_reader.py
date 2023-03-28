from typing import Iterable, List

from quadrocopter.models import InputData, Point, Transmitter


class DataReader:
    @staticmethod
    def read_from_file(filepath: str) -> InputData:
        with open(f"{filepath}") as f:
            data = f.readlines()

        n = int(data[0])
        transmitters_coordinates = [row.split() for row in data[1 : n + 1]]

        if len(transmitters_coordinates) != n:
            raise ValueError(f"Register {len(transmitters_coordinates)} transmitters, while expected {n}")

        start_coordinates = data[n + 1].split()
        stop_coordinates = data[n + 2].split()

        return DataReader._convert_coordinates(start_coordinates, stop_coordinates, transmitters_coordinates)

    @staticmethod
    def read_prompt() -> InputData:
        print("Type transmitters count", end=": ")
        n = int(input())

        transmitters_coordinates = []
        for i in range(1, n + 1):
            print(f"Type transmitter {i} coordinates (space separated: x y m)", end=": ")
            transmitters_coordinates.append(input().split())

        print(f"Type starting point coordinates (space separated: x y)", end=": ")
        start_coordinates = input().split()
        print(f"Type finish point coordinates (space separated: x y)", end=": ")
        stop_coordinates = input().split()

        return DataReader._convert_coordinates(start_coordinates, stop_coordinates, transmitters_coordinates)

    @staticmethod
    def _convert_coordinates(
        start_coordinates: List[str],
        stop_coordinates: List[str],
        transmitters_coordinates: List[List[str]],
    ) -> InputData:
        start = Point(*DataReader._to_list_of_int(start_coordinates))
        stop = Point(*DataReader._to_list_of_int(stop_coordinates))
        transmitters = [Transmitter(*DataReader._to_list_of_int(cord)) for cord in transmitters_coordinates]
        return start, stop, transmitters

    @staticmethod
    def _to_list_of_int(coordinates: Iterable[str]) -> List[int]:
        return [int(x) for x in coordinates]
