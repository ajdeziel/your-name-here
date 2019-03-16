import csv
import os
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from db.db_models import Base, MarriageCert
from utils.bcmuseum_miner import FIELDS as MARRIAGECERT_FIELDS


@click.group()
def cli():
    pass


def init_db(engine):
    Base.metadata.create_all(engine)


@click.command()
@click.argument("csv_file")
@click.option("--db", default="proj_data.db", help="Output database file")
def add_marriage_certs(csv_file, db):
    session = get_db_session(db)

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

    session.commit()


def get_db_session(db_name):
    # Assume sqlite for now, might have to add postgres support later
    engine = create_engine("sqlite:///%s" % db_name)
    if not os.path.exists(db_name):
            init_db(engine)

    DBSession = sessionmaker(engine)
    DBSession.bind = engine

    return DBSession()


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


if __name__ == "__main__":
    cli.add_command(add_marriage_certs)
    cli()
