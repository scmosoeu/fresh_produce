from sqlalchemy import create_engine, Column, Table, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from engine_info import server_info
import urllib

Base = declarative_base()

class Product(Base):

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    product_sales = relationship('Sales', backref='product_sale')
    product_inventories = relationship('Inventory', backref='product_inventory')


class Container(Base):

    __tablename__ = 'container'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    container_sales = relationship('Sales', backref='container_sale')
    container_inventories = relationship('Inventory', backref='container_inventory')


class Inventory(Base):

    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    available = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    container_id = Column(Integer, ForeignKey('container.id'), nullable=False)


class ProductCombination(Base):

    __tablename__ = 'product_combination'

    id = Column(Integer, primary_key=True)  
    name = Column(String(200), nullable=False, unique=True)
    combination_sales = relationship('Sales', backref='combination_sale')


class Sales(Base):

    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    kg_sold = Column(Float, nullable=False)
    value = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)
    highest_price = Column(Float, nullable=False)
    product_combination_id = Column(Integer, ForeignKey('product_combination.id'), nullable=False)
    container_id = Column(Integer, ForeignKey('container.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)

if __name__ == "__main__":
    
    params = urllib.parse.quote_plus(server_info)
    engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)
        
    Base.metadata.create_all(engine)