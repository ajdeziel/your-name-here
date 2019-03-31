from sqlalchemy import (
    Column, String, Date, Integer, Float, ForeignKey, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Person(Base):
    __tablename__ = "Data_People"

    Id = Column(Integer, primary_key=True)

    FirstName = Column(String(100), nullable=False)
    MiddleName = Column(String(100))
    LastName = Column(String(100), nullable=False)

    # Death record info
    DeathDate = Column(Date)
    DeathAge = Column(Integer)
    EstBirthYear = Column(Integer)
    BirthCity = Column(String(100))
    BirthCountry = Column(String(100))
    PlaceOfDeath = Column(String(100))

    # Foreign keys
    FamilyCluster_Id = Column(Integer, ForeignKey("Data_FamilyClusters.Id"))
    MarriageCert_Id = Column(Integer, ForeignKey("Data_MarriageCerts.Id"))
    DeathRecord_Id = Column(Integer, ForeignKey("Data_DeathRecords.Id"))

    # Relationships
    FamilyCluster = relationship("FamilyCluster", uselist=False, back_populates="People")
    DeathRecord = relationship("DeathRecord", uselist=False, back_populates="Person")

    def __repr__(self):
        return "%s %s" % (self.FirstName, self.LastName)


class MarriageCert(Base):
    __tablename__ = "Data_MarriageCerts"

    Id = Column(Integer, primary_key=True)
    Bride_Id = Column(Integer, ForeignKey("Data_People.Id"))
    Groom_Id = Column(Integer, ForeignKey("Data_People.Id"))

    Event_Place = Column(String(100))
    Event_Date = Column(Date)


class DeathRecord(Base):
    __tablename__ = "Data_DeathRecords"

    Id = Column(Integer, primary_key=True)

    # Grave site location
    Block = Column(String(1), nullable=False)
    Road = Column(String(5), nullable=False)
    Row = Column(Integer, nullable=False)
    Side = Column(String(1), nullable=False)
    FullPlot = Column(String(10), nullable=False)

    GraveSitePts = Column(String(100), nullable=False)
    GraveSiteCentroid_Long = Column(Float, nullable=False)
    GraveSiteCentroid_Lat = Column(Float, nullable=False)

    Arcgis_OID = Column(String(100), nullable=False)

    Person = relationship("Person", back_populates="DeathRecord")


class FamilyCluster(Base):
    __tablename__ = "Data_FamilyClusters"

    Id = Column(Integer, primary_key=True)
    Centroid_Long = Column(Float, nullable=False)
    Centroid_Lat = Column(Float, nullable=False)
    NumPeople = Column(Integer, nullable=False)

    People = relationship("Person", back_populates="FamilyCluster")

    def centroid(self):
        return self.Centroid_Lat, self.Centroid_Long
