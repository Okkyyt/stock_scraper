from datetime import timedelta
from dataclasses import dataclass


@dataclass(slots=True)
class time_format:
    weeks: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0


def timedelta_to_interval_kwargs(td: timedelta) -> dict:
    total_seconda = int(td.total_seconds())
    weeks = total_seconda // (7 * 24 * 3600)
    days = (total_seconda % (7 * 24 * 3600)) // (24 * 3600)
    hours = (total_seconda % (24 * 3600)) // 3600
    minutes = (total_seconda % 3600) // 60
    seconds = total_seconda % 60
    return time_format(
        weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds
    )
