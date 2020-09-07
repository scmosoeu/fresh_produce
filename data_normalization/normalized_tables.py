from sqlalchemy import create_engine, Column, Table, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from engine_info import server_info
import urllib

Base = declarative_base()


class ProductContainer(Base):

    __tablename__ = 'product_container'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    container_id = Column(Integer, ForeignKey('container.id'))
    inventory = relationship('Inventory', backref='inventory')

class Product(Base):

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    product_container = relationship('ProductContainer', backref='product_container')


class Container(Base):

    __tablename__ = 'container'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    product_container = relationship('ProductContainer', backref='product_container')
    product_combinations = relationship('ProductCombo', backref='product_combination')


class Inventory(Base):

    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    name = Column(String(50), nullable=False)
    available = Column(Integer, nullable=False)
    product_container_id = Column(Integer, ForeignKey('product_container.id'), nullable=False)


class ContainerProductCombination(Base):

    __tablename__ = 'container_product_combination'

    id = Column(Integer, primary_key=True)
    container_id = Column(Integer, ForeignKey('product.id'))
    product_combination_id = Column(Integer, ForeignKey('product_combination.id'))

class ProductCombo(Base):

    __tablename__ = 'product_combination'

    id = Column(Integer, primary_key=True)  
    name = Column(String(200), nullable=False)
    container_id = Column(Integer, ForeignKey('container_product_combination.id'), nullable=False)
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