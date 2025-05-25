# after running :
# alembic revision --autogenerate -m "refactor: dimensions + fact table"
# alembic upgrade head


from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataSource(Base):
    __tablename__ = 'datasource'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Gas(Base):
    __tablename__ = 'gas'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Sector(Base):
    __tablename__ = 'sector'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class EmissionsFact(Base):
    __tablename__ = 'emissions_fact'
    id = Column(Integer, primary_key=True)
    datasource_id = Column(Integer, ForeignKey('datasource.id'), nullable=False)
    region_id     = Column(Integer, ForeignKey('region.id'), nullable=False)
    gas_id        = Column(Integer, ForeignKey('gas.id'), nullable=False)
    sector_id     = Column(Integer, ForeignKey('sector.id'), nullable=True)
    year          = Column(Integer, nullable=False)
    value         = Column(Float, nullable=False)
    ingested_at   = Column(DateTime, default=datetime.utcnow, nullable=False)
    source_file   = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            'datasource_id', 'region_id', 'gas_id', 'sector_id', 'year',
            name='uq_emissions_fact'
        ),
    )


