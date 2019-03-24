import os
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect

from db.db_models import Base
from scraping.deathrecords import scrape_death_records
from scraping.marriagecerts import scrape_marriagecerts_csv


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

    for cert in scrape_marriagecerts_csv(csv_file):
        session.merge(cert)

    session.commit()


@click.command()
@click.argument("kml_file")
@click.option("--db", default="proj_data.db", help="Output database file")
def add_death_records(kml_file, db):
    session = get_db_session(db)

    for person, record in scrape_death_records(kml_file):
        session.merge(person)

    session.commit()


def get_db_session(db_name):
    # Assume sqlite for now, might have to add postgres support later
    engine = create_engine("sqlite:///%s" % db_name)
    init_db(engine)

    DBSession = sessionmaker(engine)
    DBSession.bind = engine

    return DBSession()


if __name__ == "__main__":
    cli.add_command(add_marriage_certs)
    cli.add_command(add_death_records)
    cli()
