from sqlalchemy import Column, String, Date, Integer, create_engine
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
