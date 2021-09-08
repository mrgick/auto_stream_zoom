from datetime import datetime, timedelta
from typing import Union
import re
import logging

logger = logging.getLogger(__name__)


def now() -> datetime:
    """
        Get now time.
    """
    return datetime.now()


def is_smaller_time(str_time: str) -> bool:
    return bool(re.match(r'\d\d:\d\d', str_time) or
                re.match(r'\d:\d\d', str_time) or
                re.match(r'\d\d:\d', str_time) or
                re.match(r'\d:\d', str_time))


def str_to_datetime(str_time: str,
                    next_day: bool = False) -> Union[datetime, None]:
    """
        Get datetime from string.
    """
    try:
        if is_smaller_time(str_time):
            hour, minute = map(int, str_time.split(":"))
            date = now()
            hour_now, minute_now = date.hour, date.minute
            if (hour_now > hour
                    or hour_now == hour and minute_now > minute
                    or next_day):
                date += timedelta(days=1)
            date = date.replace(hour=hour, minute=minute)
            return date
        elif re.match(r"\d{4}-\d\d-\d\d\s\d\d:\d\d", str_time):
            return datetime.fromisoformat(str_time)
        else:
            return None
    except Exception as e:
        logger.error(e)
        return None


def add_duration_to_datetime(date: datetime,
                             duration: str) -> Union[datetime, None]:
    """
        Adding string duration to date.
    """
    try:
        if is_smaller_time(duration):
            hour, minute = map(int, duration.split(":"))
            date += timedelta(hours=hour, minutes=minute)
            return date
        else:
            return None
    except Exception as e:
        logger.error(e)
        return None
