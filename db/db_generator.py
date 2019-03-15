import sys
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from db.db_models import Base, MarriageCert
from utils.bcmuseum_miner import FIELDS as MARRIAGECERT_FIELDS

DB = "sqlite:///proj_data.db"


def init_db(engine):
    Base.metadata.create_all(engine)


def extract_name_fields(name_str):
    """Extract first, middle and last name from a name string"""
    name_split = name_str.split(" ")
    if len(name_split) == 2:
        return name_split[0].upper(), None, name_split[1].upper()
    elif len(name_split) >= 3:
        first = name_split[0].upper()
        last = name_split[-1].upper()
        middle = " ".join(name_split[1:-1]).upper()
        return first, middle, last
    else:
        raise Exception("Can't handle name '%s'" % name_str)


def add_marriage_certs(csv_file, session):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, MARRIAGECERT_FIELDS)
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

            cert = MarriageCert(
                Bride_FirstName=bride_first,
                Bride_MiddleName=bride_middle,
                Bride_LastName=bride_last,

                Groom_FirstName=groom_first,
                Groom_MiddleName=groom_middle,
                Groom_LastName=groom_last,

                Event_Place=event_place,
                Event_Date=event_date
            )
            session.add(cert)


if __name__ == "__main__":
    engine = create_engine(DB)
    init_db(engine)

    DBSession = sessionmaker(engine)
    DBSession.bind = engine

    session = DBSession()

    add_marriage_certs(sys.argv[1], session)
    session.commit()
