from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
import json

Base = declarative_base()


class District(Base):

    __tablename__ = "district"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Facility(Base):

    __tablename__ = "facility"

    id = Column(String, primary_key=True)
    name = Column(String)
    district_id = Column(Integer, ForeignKey("district.id"))

    district_info = relationship("District")


class Population(Base):

    __tablename__ = "population"

    id = Column(Integer, primary_key=True, autoincrement=True)
    district_id = Column(Integer, ForeignKey("district.id"))
    year = Column(Integer, nullable=False)
    male = Column(Integer)
    female = Column(Integer)
    total = Column(Integer)
    childbearing_age = Column(Integer)
    pregnant = Column(Integer)
    not_pregnant = Column(Integer)
    births = Column(Integer)
    u1 = Column(Integer)
    u5 = Column(Integer)
    u15 = Column(Integer)
    suspect_tb = Column(Integer)

    district_info = relationship("District")

    def serialize(self):
        return {
            "district_name": self.district_info.name,
            "year": self.year,
            "female": self.female,
            "total": self.total,
            "childbearing_age": self.childbearing_age,
            "pregnant": self.childbearing_age,
            "not_pregnant": self.not_pregnant,
            "births": self.births,
            "u1": self.u1,
            "u5": self.u5,
            "u15": self.u15,
            "suspect_tb": self.suspect_tb,
        }


class IndicatorGroup(Base):

    __tablename__ = "indicator_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    indicator_id = Column(String, ForeignKey("indicator.id"))


class Indicator(Base):

    __tablename__ = "indicator"

    id = Column(String, primary_key=True)
    name = Column(String)
    view = Column(String)


class Repository(Base):

    __tablename__ = "repository"

    id = Column(Integer, primary_key=True, autoincrement=True)

    facility_id = Column(String, ForeignKey("facility.id"))
    date = Column(Date, nullable=False)
    indicator = Column(String, ForeignKey("indicator.id"))
    value_raw = Column(Integer)
    value_iqr = Column(Integer)
    value_std = Column(Integer)
    value_rep = Column(String)

    indicator_info = relationship("Indicator")
    facility_info = relationship("Facility")

    @property
    def display_data_dict(self):

        serializeable = {
            "district_name": self.facility_info.district_info.name,
            "facility_name": self.facility_info.name,
            "date": self.date,
            "indicator_name": self.indicator_info.name,
            "indicator_view": self.indicator_info.view,
            "value_raw": self.value_raw,
            "value_iqr": self.value_iqr,
            "value_std": self.value_std,
        }

        return serializeable


class FetchDate(Base):

    __tablename__ = "fetch_date"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

    def serialize(self):
        return self.date


class PopulationTarget(Base):

    __tablename__ = "population_target"
    id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(String, ForeignKey("indicator.id"))
    cat = Column(String)

    indicator_info = relationship("Indicator")

    def serialize(self):

        return {"indicator": self.indicator_info.name, "car": self.cat}
