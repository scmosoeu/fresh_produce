from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from engine_info import server_info
import urllib

Base = declarative_base()

class Product(Base):

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    containers = relationship('Container', backref='product')


class Container(Base):

    __tablename__ = 'container'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    inventories = relationship('Inventory', backref='inventory')
    product_combinations = relationship('ProductCombo', backref='product_combination')


class Inventory(Base):

    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    name = Column(String(50), nullable=False)
    available = Column(Integer, nullable=False)
    container_id = Column(Integer, ForeignKey('container.id'), nullable=False)

class ProductCombo(Base):

    __tablename__ = 'product_combination'

    id = Column(Integer, primary_key=True)  
    name = Column(String(200), nullable=False, unique=True)
    container_id = Column(Integer, ForeignKey('container.id'), nullable=False)
    product_sales = relationship('Sales', backref='sales')


class Sales(Base):

    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    kg_sold = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)
    highest_price = Column(Float, nullable=False)
    product_combination_id = Column(Integer, ForeignKey('product_combination.id'), nullable=False)


if __name__ == "__main__":
    
    params = urllib.parse.quote_plus(server_info)
    engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)
        
    Base.metadata.create_all(engine)