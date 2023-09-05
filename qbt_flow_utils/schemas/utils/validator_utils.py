"""Utils for validating schemas."""
import re
from datetime import timedelta


def parse_time(time_str: str) -> timedelta:
    """
    Parse a time string e.g. (2h 13m) into a timedelta object.
    :param time_str: A string identifying a duration.  (eg. 2h 13m)
    :return datetime.timedelta: A datetime.timedelta object
    """
    regex = re.compile(
        r"^((?P<weeks>[\.\d]+?)w)? *"
        r"^((?P<days>[\.\d]+?)d)? *"
        r"((?P<hours>[\.\d]+?)h)? *"
        r"((?P<minutes>[\.\d]+?)m)? *"
        r"((?P<seconds>[\.\d]+?)s?)?$",
    )
    parts = regex.match(time_str)
    assert parts is not None, (  # noqa: S101
        f"Could not parse any time information from '{time_str}'.  Examples of valid strings: '8h',"
        " '2d8h5m20s', '2m4s'"
    )
    time_params = {name: float(param) for name, param in parts.groupdict().items() if param}
    return timedelta(**time_params)
