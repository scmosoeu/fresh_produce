from engine_info import server_info
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import urllib

app = Flask(__name__)

params = urllib.parse.quote_plus(server_info)
database = f'mssql+pyodbc:///?odbc_connect={params}' 
app.config['SQLALCHEMY_DATABASE_URI'] = database
db = SQLAlchemy(app)

class RetailerProducts(db.Model):

    __tablename__ = 'RetailerProducts'

    RetailerProductID = db.Column(db.Integer, primary_key=True)
    RetailerProduct = db.Column(db.String(100), nullable=False, unique=True)


class Retailers(db.Model):

    __tablename__ = 'Retailers'

    RetailerID = db.Column(db.Integer, primary_key=True)
    RetailerName = db.Column(db.String(50), nullable=False, unique=True)

class Date(db.Model):

    __tablename__ = 'Date'

    DateID = db.Column(db.Integer, primary_key=True)
    date_key = db.Column(db.DateTime, db.ForeignKey('master_date.date_key'), nullable=False)

class RetailerPrices(db.Model):

    __tablename__ = 'RetailerPrices'

    RetailerProductID = db.Column(db.Integer, db.ForeignKey('RetailerProducts.RetailerProductID'), nullable=False, primary_key=True)
    Price = db.Column(db.Float, nullable=False)
    DateID = db.Column(db.Integer, db.ForeignKey('Date.DateID'), nullable=False)
    RetailerID = db.Column(db.Integer, db.ForeignKey("Retailes.RetailerID"))

class MasterDate(db.Model):

    __tablename__ = 'master_date'
    date_key = db.Column(db.DateTime, primary_key=True)
    calendar_date = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    half_of_year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(20), nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)
    day = db.Column(db.String(20), nullable=False)

    inventory_dates = db.relationship('Inventory', backref='inventory_date')
    invoice_dates = db.relationship('Sales', backref='sales_date')

if __name__ == "__main__":
    
    db.create_all()