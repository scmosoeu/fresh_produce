from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Commodity(Base):

    __tablename__ = "product_raw"

    id = Column(Integer, primary_key=True)
    date = Column(String)
    commodity = Column(String)
    total_value_sold = Column(String)
    total_qty_sold = Column(String)
    total_kg_sold = Column(String)
    qty_available = Column(Integer)


class Container(Base):

    __tablename__ = 'container_raw'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    commodity = Column(String)
    container = Column(String)
    qty_available = Column(Integer)
    value_sold = Column(String)
    qty_sold = Column(String)
    kg_sold = Column(String)
    average_price_per_kg = Column(String)

class Container(Base):
    
    __tablename__ = 'container_raw'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    commodity = Column(String)
    container = Column(String)
    qty_available = Column(Integer)
    value_sold = Column(String)
    qty_sold = Column(String)
    kg_sold = Column(String)
    average_price_per_kg = Column(String)
