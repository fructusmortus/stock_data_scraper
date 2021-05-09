from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Companies(Base):
    __tablename__ = "companies"

    ticker = Column('ticker', String, unique=True, primary_key=True)
    full_name = Column('full_name', String)
    sector = Column('sector', String)
    industry = Column('industry', String)
    country = Column('country', String)
    table_1 = relationship("Table1", back_populates="companies")
    created_at = Column('created_at', DateTime, default=func.now())


class Table1(Base):
    __tablename__ = "table_1"

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    ticker = Column(String, ForeignKey('companies.ticker'))
    companies = relationship("Companies", back_populates="table_1")
    table_1 = Column('table_1', JSON)
    created_at = Column('created_at', DateTime, default=func.now())

