import csv
import os
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from db.db_models import Base, MarriageCert, DeathRecord
from utils.kml_reader import read_kml_placemarks
from utils.bcmuseum_miner import FIELDS as MARRIAGECERT_FIELDS
from utils.timeutils import parse_date



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


@click.command()
@click.argument("kml_file")
@click.option("--db", default="proj_data.db", help="Output database file")
def add_death_records(kml_file, db):
    session = get_db_session(db)

    for ext_data, points in read_kml_placemarks(kml_file):
        # No real useful information in row without name - ignore!
        if "FullName" not in ext_data or type(ext_data["FullName"]) != str:
            continue

        name_first, name_middle, name_last = extract_name_fields(ext_data["FullName"].strip())

        # Try to parse date of death
        date_of_death = None
        if "DeathYYYYMMDD" in ext_data and ext_data["DeathYYYYMMDD"] is not None:
            date_of_death = parse_date(ext_data["DeathYYYYMMDD"])

            if date_of_death is None:
                print("WARN: Could not parse date string '%s'" % ext_data["DeathYYYYMMDD"])

        # Get birth city and country, if available
        birth_city = ext_data["BirthCity"] if "BirthCity" in ext_data else None
        birth_country = ext_data["BirthCountry"] if "BirthCountry" in ext_data else None
        place_of_death = ext_data["PlaceOfDeath"] if "PlaceOfDeath" in ext_data else None

        # Process polygon points and compute centroid
        poly_pts = set()
        for point in points:
            poly_pts.add((point.x, point.y))
        poly_pts_str = " ".join([str(x) + "," + str(y) for x, y in poly_pts])

        pts_x = list(map(lambda p: p[0], poly_pts))
        centroid_x = sum(pts_x) / len(pts_x)

        pts_y = list(map(lambda p: p[1], poly_pts))
        centroid_y = sum(pts_y) / len(pts_y)

        death_record = DeathRecord(
            FirstName=name_first,
            MiddleName=name_middle,
            LastName=name_last,
            DeathDate=date_of_death,
            DeathAge=None,  # TODO
            BirthCity=birth_city,
            BirthCountry=birth_country,
            PlaceOfDeath=place_of_death,
            Block=ext_data["Block"],
            Road=ext_data["Road"],
            Row=ext_data["Row"],
            Side=ext_data["Side"],
            FullPlot=ext_data["FullPlot"],
            GraveSitePts=poly_pts_str,
            GraveSiteCentroid_X=centroid_x,
            GraveSiteCentroid_Y=centroid_y
        )
        session.add(death_record)

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


def parse_age(age_str):
    """Parse an age in years from years, months and days. Age will be rounded
    to the nearest year.

    "Stb." indicates stillborn, which will give an age of 0 years.
    :return {int} Age in years.
    """
    return None


if __name__ == "__main__":
    cli.add_command(add_marriage_certs)
    cli.add_command(add_death_records)
    cli()
