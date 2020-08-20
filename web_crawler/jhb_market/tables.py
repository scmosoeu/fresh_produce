from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from engine_info import server_info
import urllib

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

class ProductCombination(Base):
    
    __tablename__ = 'product_combination_raw'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    commodity = Column(String)
    container = Column(String)
    unit_mass = Column(Integer)
    product_combination = Column(String)
    total_value_sold = Column(String)
    total_qty_sold = Column(Integer)
    total_kg_sold = Column(Float)
    average = Column(String)
    highest_price = Column(String)
    ave_per_kg = Column(String)
    highest_price_per_kg = Column(String)

if __name__ == "__main__":

    params = urllib.parse.quote_plus(f'{server_info};DATABASE=jhb_market;Trusted_Connection=yes')
    engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)

    Base.metadata.create_all(engine)