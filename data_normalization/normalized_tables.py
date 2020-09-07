from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from engine_info import server_info
import urllib

Base = declarative_base()

class Product(Base):

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Container(Base):

    __tablename__ = 'container'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Inventory(Base):

    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    name = Column(String, nullable=False)
    available = Column(Integer, nullable=False)

class ProductCombo(Base):

    __tablename__ = 'product_combination'

    id = Column(Integer, primary_key=True)  
    name = Column(String, nullable=False, unique=True)


class Sales(Base):

    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    # Some foreignkey
    quantity_sold = Column(Integer, nullable=False)
    kg_sold = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)
    highest_price = Column(Float, nullable=False)


if __name__ == "__main__":
    
    params = urllib.parse.quote_plus(server_info)
    engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)
        
    Base.metadata.create_all(engine)