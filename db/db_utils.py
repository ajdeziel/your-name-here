from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.db_models import Base


def init_db(engine):
    Base.metadata.create_all(engine)


def get_db_session(db_name):
    # Assume sqlite for now, might have to add postgres support later
    engine = create_engine("sqlite:///%s" % db_name, echo=True)
    init_db(engine)

    DBSession = sessionmaker(engine)
    DBSession.bind = engine

    return DBSession()
