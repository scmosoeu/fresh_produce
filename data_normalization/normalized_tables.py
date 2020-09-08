from engine_info import server_info
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib

app = Flask(__name__)

params = urllib.parse.quote_plus(server_info)
database = f'mssql+pyodbc:///?odbc_connect={params}' 
app.config['SQLALCHEMY_DATABASE_URI'] = database
db = SQLAlchemy(app)

class Product(db.Model):

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    product_sales = db.relationship('Sales', backref='product_sale')
    product_inventories = db.elationship('Inventory', backref='product_inventory')


class Container(db.Model):

    __tablename__ = 'container'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    container_sales = db.relationship('Sales', backref='container_sale')
    container_inventories = db.relationship('Inventory', backref='container_inventory')


class Inventory(db.Model):

    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey('container.id'), nullable=False)


class ProductCombination(db.Model):

    __tablename__ = 'product_combination'

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(200), nullable=False, unique=True)
    combination_sales = db.relationship('Sales', backref='combination_sale')


class Sales(db.Model):

    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    kg_sold = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    average_price = db.Column(db.Float, nullable=False)
    highest_price = db.Column(db.Float, nullable=False)
    product_combination_id = db.Column(db.Integer, db.ForeignKey('product_combination.id'), nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey('container.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

if __name__ == "__main__":
    
    db.create_all()