# General libraries
import pandas as pd
import numpy as np

# SQLAlchemy imports
import urllib
from sqlalchemy import create_engine, insert, Table, MetaData, select

# Custom upload with connection string
from database.engine_info import server_info

# Creating a connection to MS SQL SERVER
params = urllib.parse.quote_plus(server_info)
engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)
connection = engine.connect()
metadata = MetaData(bind=engine)

# Upload SQL databases
sales = pd.read_sql_table('Joburg_Fresh_produce_combined_cleaned', connection)
inventory = pd.read_sql_table('Joburg_Fresh_produce_container_cleaned', connection)

database = {
    'sales':sales[sales['total_value_sold'] > 0],
    'inventory':inventory
}
