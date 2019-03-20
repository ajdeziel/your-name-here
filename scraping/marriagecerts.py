"""
Scrapes data from a CSV file of marriage certificates mined from the Royal BC Museum's
genealogy database.
"""

import csv
from datetime import datetime
from db.db_models import MarriageCert
from scraping.utils import extract_name_fields
from utils.bcmuseum_miner import FIELDS


def scrape_marriagecerts_csv(csv_file):
    with open(csv_file, 'r', encoding="latin-1") as file:
        reader = csv.DictReader(file, FIELDS)
        next(reader)  # skip header

        for row in reader:
            # Extract bride and groom first, middle and last names
            groom_first, groom_middle, groom_last = extract_name_fields(row["Groom"])
            bride_first, bride_middle, bride_last = extract_name_fields(row["Bride"])

            date_str = row["Event Date (YYYY-MM-DD)"]
            if date_str:
                event_date = datetime.strptime(row["Event Date (YYYY-MM-DD)"], "%Y-%m-%d")
            else:
                event_date = None

            event_place = row["Event Place"].upper()

            yield MarriageCert(
                Bride_FirstName=bride_first,
                Bride_MiddleName=bride_middle,
                Bride_LastName=bride_last,

                Groom_FirstName=groom_first,
                Groom_MiddleName=groom_middle,
                Groom_LastName=groom_last,

                Event_Place=event_place,
                Event_Date=event_date
            )
