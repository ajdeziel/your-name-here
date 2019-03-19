import re
from datetime import datetime


def parse_date(date_str):
    """Parse a date from an input string, in the order YYYYMMDD.

    Sometimes we get weird date formats, like this: "1882/.0/2.". In this
    case just try to match the year.
    :return datetime object or None
    """
    # Try to get full year, month and day
    ymd_match = re.match("(\d{4})[/\\\-]?(\d{2})[/\\\-]?(\d{2})", date_str)
    if ymd_match:
        return datetime(year=int(ymd_match.group(1)),
                        month=int(ymd_match.group(2)),
                        day=int(ymd_match.group(3)))

    else:
        # Can we just get the year?
        year_match = re.search("^\d{4}", date_str)
        if year_match:
            return datetime(year=int(year_match.group(0)), month=1, day=1)
        else:
            return None
