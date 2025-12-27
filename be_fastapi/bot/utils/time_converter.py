import re
from datetime import timedelta


def parse_duration(duration_str: str):
    """
    Converts strings like '1h', '30m', '1d' into timedelta objects.
    Default to 5 minutes if parsing fails.
    """

    if not duration_str:
        return timedelta(minutes=5)

    regex = re.match(r"(\d+)([smhd])", duration_str)
    if not regex:
        return timedelta(minutes=5)

    value, unit = regex.groups()
    value = int(value)

    if unit == 's':
        return timedelta(seconds=value)
    elif unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)

    return timedelta(minutes=5)
