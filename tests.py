from unittest import TestCase
from mama import (
    follow_regulations,
    DateInterval,
)


class FollowRegulationsTest(TestCase):
    def test_one_interval__ok__returns_true(self):
        intervals = [
            DateInterval.from_raw_interval('2017-01-01', '2017-01-01'),
        ]

        self.assertTrue(follow_regulations(intervals, 2, 1))

    def test_one_interval__not_ok__returns_false(self):
        intervals = [
            DateInterval.from_raw_interval('2017-01-01', '2017-01-01'),
        ]

        self.assertFalse(follow_regulations(intervals, 2, 0))

    def test_two_intervals__ok__returns_true(self):
        intervals = [
            DateInterval.from_raw_interval('2017-01-01', '2017-01-01'),
            DateInterval.from_raw_interval('2017-01-03', '2017-01-03'),
        ]

        self.assertTrue(follow_regulations(intervals, 2, 1))

    def test_two_intervals__not_ok__returns_false(self):
        intervals = [
            DateInterval.from_raw_interval('2017-01-01', '2017-01-01'),
            DateInterval.from_raw_interval('2017-01-03', '2017-01-03'),
        ]

        self.assertFalse(follow_regulations(intervals, 3, 1))