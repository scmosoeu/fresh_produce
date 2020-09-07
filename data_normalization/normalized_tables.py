from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from engine_info import server_info
import urllib

Base = declarative_base()

class Product(Base):

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Container(Base):

    __tablename__ = 'container'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Inventory(Base):

    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    available = Column(Integer)

class ProductCombo(Base):

    __tablename__ = 'product_combination'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    name = Column(String)


class Sales(Base):

    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    # Some foreignkey
    quantity_sold = Column(Integer)
    cost = Column(Float)
    average_price = Column(Float)
    highest_price = Column(Float)


if __name__ == "__main__":
    
    params = urllib.parse.quote_plus(server_info)
    engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)
        
    Base.metadata.create_all(engine)