import pytest

from quadrocopter.models import Point, Transmitter


@pytest.mark.parametrize(
    "transmitter, point, is_covered",
    (
        (Transmitter(6, 11, 4), Point(17, 10), False),
        (Transmitter(6, 11, 4), Point(11, 17), False),
        (Transmitter(8, 17, 3), Point(17, 10), False),
        (Transmitter(8, 17, 3), Point(11, 17), True),
        (Transmitter(19, 19, 2), Point(17, 10), False),
        (Transmitter(19, 19, 2), Point(11, 17), False),
        (Transmitter(19, 11, 4), Point(17, 10), True),
        (Transmitter(19, 11, 4), Point(11, 17), False),
        (Transmitter(15, 7, 6), Point(17, 10), True),
        (Transmitter(15, 7, 6), Point(11, 17), False),
        (Transmitter(12, 19, 4), Point(17, 10), False),
        (Transmitter(12, 19, 4), Point(11, 17), True),
        # in touch
        (Transmitter(1, 1, 1), Point(1, 0), True),
        (Transmitter(1, 1, 1), Point(2, 1), True),
    ),
)
def test_transmitter_covers(transmitter: Transmitter, point: Point, is_covered: bool):
    assert transmitter.covers(point) == is_covered


@pytest.mark.parametrize(
    "transmitter1, transmitter2, are_overlapping",
    (
        (Transmitter(6, 11, 4), Transmitter(8, 17, 3), True),
        (Transmitter(6, 11, 4), Transmitter(19, 19, 2), False),
        (Transmitter(6, 11, 4), Transmitter(19, 11, 4), False),
        (Transmitter(6, 11, 4), Transmitter(15, 7, 6), True),
        (Transmitter(6, 11, 4), Transmitter(12, 19, 4), False),
        (Transmitter(8, 17, 3), Transmitter(6, 11, 4), True),
        (Transmitter(8, 17, 3), Transmitter(19, 19, 2), False),
        (Transmitter(8, 17, 3), Transmitter(19, 11, 4), False),
        (Transmitter(8, 17, 3), Transmitter(15, 7, 6), False),
        (Transmitter(8, 17, 3), Transmitter(12, 19, 4), True),
        (Transmitter(19, 19, 2), Transmitter(6, 11, 4), False),
        (Transmitter(19, 19, 2), Transmitter(8, 17, 3), False),
        (Transmitter(19, 19, 2), Transmitter(19, 11, 4), False),
        (Transmitter(19, 19, 2), Transmitter(15, 7, 6), False),
        (Transmitter(19, 19, 2), Transmitter(12, 19, 4), False),
        (Transmitter(19, 11, 4), Transmitter(6, 11, 4), False),
        (Transmitter(19, 11, 4), Transmitter(8, 17, 3), False),
        (Transmitter(19, 11, 4), Transmitter(19, 19, 2), False),
        (Transmitter(19, 11, 4), Transmitter(15, 7, 6), True),
        (Transmitter(19, 11, 4), Transmitter(12, 19, 4), False),
        (Transmitter(15, 7, 6), Transmitter(6, 11, 4), True),
        (Transmitter(15, 7, 6), Transmitter(8, 17, 3), False),
        (Transmitter(15, 7, 6), Transmitter(19, 19, 2), False),
        (Transmitter(15, 7, 6), Transmitter(19, 11, 4), True),
        (Transmitter(15, 7, 6), Transmitter(12, 19, 4), False),
        (Transmitter(12, 19, 4), Transmitter(6, 11, 4), False),
        (Transmitter(12, 19, 4), Transmitter(8, 17, 3), True),
        (Transmitter(12, 19, 4), Transmitter(19, 19, 2), False),
        (Transmitter(12, 19, 4), Transmitter(19, 11, 4), False),
        (Transmitter(12, 19, 4), Transmitter(15, 7, 6), False),
        # in touch
        (Transmitter(1, 1, 1), Transmitter(3, 1, 1), True),
        (Transmitter(1, 1, 1), Transmitter(1, 3, 1), True),
    ),
)
def test_transmitter_has_intersection_with(transmitter1: Transmitter, transmitter2: Transmitter, are_overlapping: bool):
    assert transmitter1.has_intersection_with(transmitter2) == are_overlapping
