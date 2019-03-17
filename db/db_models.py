from sqlalchemy import Column, String, Date, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MarriageCert(Base):
    __tablename__ = "Data_MarriageCerts"

    Id = Column(Integer, primary_key=True)

    Bride_FirstName = Column(String(100), nullable=False)
    Bride_MiddleName = Column(String(100))
    Bride_LastName = Column(String(100), nullable=False)
    Groom_FirstName = Column(String(100), nullable=False)
    Groom_MiddleName = Column(String(100))
    Groom_LastName = Column(String(100), nullable=False)

    Event_Place = Column(String(100))
    Event_Date = Column(Date)


class DeathRecord(Base):
    __tablename__ = "Data_DeathRecords"

    Id = Column(Integer, primary_key=True)

    FirstName = Column(String(100), nullable=False)
    MiddleName = Column(String(100))
    LastName = Column(String(100), nullable=False)

    DeathDate = Column(Date)
    DeathAge = Column(Integer)

    BirthCity = Column(String(100))
    BirthCountry = Column(String(100))
    PlaceOfDeath = Column(String(100))

    # Grave site location
    Block = Column(String(1), nullable=False)
    Road = Column(String(5), nullable=False)
    Row = Column(Integer, nullable=False)
    Side = Column(String(1), nullable=False)
    FullPlot = Column(String(10), nullable=False)

    GraveSitePts = Column(String(100), nullable=False)
    GraveSiteCentroid_X = Column(Float, nullable=False)
    GraveSiteCentroid_Y = Column(Float, nullable=False)
