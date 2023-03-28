import pytest

from quadrocopter.data_reader import DataReader
from quadrocopter.pathfinder import PathFinder


@pytest.mark.parametrize(
    "fixture, safe_path_exists",
    (
        ("example-1", True),
        ("example-6", True),
        ("example-8", True),
        ("example-9", True),
        # stop not covered by transmitters
        ("example-2", False),
        ("example-10", False),
        # start not covered by transmitters
        ("example-3", False),
        ("example-11", False),
        # path not fully covered by transmitters
        ("example-4", False),
        ("example-5", False),
        ("example-7", False),
    ),
)
def test_exists_safe_path(fixture: str, safe_path_exists: bool):
    start, stop, transmitters = DataReader.read_from_file(f"tests/fixtures/{fixture}.txt")
    assert PathFinder.exists_safe_path(start, stop, transmitters) == safe_path_exists
