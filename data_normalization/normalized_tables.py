from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from engine_info import server_info
import urllib

Base = declarative_base()

class Product(Base):

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    product_name = Column(String)


class Container(Base):

    __tablename__ = 'container'

    id = Column(Integer, primary_key=True)
    container_name = Column(String)

