import datetime
from typing import (
    List,
    Tuple,
)

CHECK_PERIOD = 180
ALLOWED_DAYS_PER_CHECK_PERIOD = 90


class DateInterval:
    DATE_FORMAT: str = '%Y-%m-%d'

    def __init__(self, begin: datetime.date, end: datetime.date):
        if begin > end:
            raise ValueError("Interval end date is higher than begin date.")

        self.begin = begin
        self.end = end

    @property
    def day_count(self):
        return (self.end - self.begin).days + 1

    @classmethod
    def from_raw_interval(cls, begin: str, end: str):
        return DateInterval(
            datetime.datetime.strptime(begin, cls.DATE_FORMAT).date(),
            datetime.datetime.strptime(end, cls.DATE_FORMAT).date()
        )

    def __str__(self):
        return '{begin} - {end}'.format(
            begin=self.begin.strftime(self.DATE_FORMAT),
            end=self.end.strftime(self.DATE_FORMAT)
        )


def parse_intervals(dates_raw: List[Tuple[str, str]]) -> List[DateInterval]:
    return [DateInterval.from_raw_interval(*interval) for interval in dates_raw]


def follow_regulations(date_intervals: List[DateInterval], check_period: int, allowed_days_per_check_period: int):
    first_day = date_intervals[0].begin
    day_count = (date_intervals[-1].end - first_day).days + 1
    days = [0] * day_count
    for date_interval in date_intervals:
        for day_no in range(date_interval.day_count):
            day = date_interval.begin + datetime.timedelta(days=day_no)
            day_idx = (day - first_day).days
            days[day_idx] += 1

    if max(days) > 1:
        raise ValueError("Overlapping intervals are not allowed")

    for day_idx in range(day_count):
        if sum(days[day_idx:day_idx + check_period]) > allowed_days_per_check_period:
            return False

    return True


def find_next_interval(previous_visits: List[DateInterval],
                       planned_duration: int,
                       check_period: int,
                       allowed_days_per_check_period: int):
    """Finds soonest possible interval that satisfies regulations.
    Given that the data is small, it computes result very fast
    even with current implementation.
    Algorithm checks whether there are more in country days than allowed
    during any `check_period` by checking all possible `check_period`
    intervals, starting from first date seen.
    """
    if planned_duration > allowed_days_per_check_period:
        raise ValueError("Planned duration is higher than allowed days.")

    if not follow_regulations(previous_visits, check_period, allowed_days_per_check_period):
        raise ValueError("Regulations are already violated")

    after = previous_visits[-1].end
    i = 1
    while True:
        # If desired duration is 3 days (for example 20, 21, 22),
        # then last day of the visit is first day + planned_duration - 1
        interval_candidate = DateInterval(
            after + datetime.timedelta(days=i),
            after + datetime.timedelta(days=i + planned_duration - 1)
        )

        if follow_regulations(previous_visits + [interval_candidate], check_period, allowed_days_per_check_period):
            return interval_candidate

        i += 1


if __name__ == '__main__':
    previous_date_intervals = parse_intervals([
        ('2017-03-19', '2017-04-02'),
        ('2017-07-21', '2017-08-25'),
        ('2017-10-16', '2017-11-28'),
        ('2018-01-15', '2018-02-27'),
        ('2018-04-16', '2018-05-29'),
        ('2018-07-16', '2018-08-28'),
        ('2018-10-15', '2018-11-27'),
        ('2019-01-14', '2019-02-26'),
    ])

    interval = find_next_interval(
        previous_date_intervals,
        planned_duration=45,
        check_period=CHECK_PERIOD,
        allowed_days_per_check_period=ALLOWED_DAYS_PER_CHECK_PERIOD,
    )

    intervals = previous_date_intervals + [interval]
    for i1, i2 in zip(intervals[:-1], intervals[1:]):
        days_between = (i2.begin - i1.end).days - 1
        print(i1, i2, f"day_count={i1.day_count}", f"days_between={days_between}")

    # print(interval)
