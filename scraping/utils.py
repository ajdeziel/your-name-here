"""
Utility functions for data scraping tasks.
"""

import re
from datetime import datetime


def parse_age(age_str):
    """Parse an age in years from years, months and days. Age will be rounded
    to the nearest year.
    :return {int} Age in years.
    """
    # Stb. indicates stillborn, which will give an age of 0 years
    if "stb." in age_str.lower():
        return 0

    age_years = None
    age_years_match = re.search("(\d+) *y(ears)?", age_str)
    if age_years_match:
        age_years = int(age_years_match.group(1))

    age_months = 0
    age_months_match = re.search("(\d+) *m(onths)?", age_str)
    if age_months_match:
        age_months = int(age_months_match.group(1))

    if age_years and age_months >= 6:
        age_years += 1

    return age_years


def extract_name_fields(name_str):
    """Extract first, middle and last name from a name string"""
    name_split = name_str.split(" ")
    if len(name_split) == 1:
        return name_split[0].upper(), None, "UNKNOWN"
    elif len(name_split) == 2:
        return name_split[0].upper(), None, name_split[1].upper()
    elif len(name_split) >= 3:
        first = name_split[0].upper()
        last = name_split[-1].upper()
        middle = " ".join(name_split[1:-1]).upper()
        return first, middle, last
    else:
        raise Exception("Can't handle name '%s'" % name_str)


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
