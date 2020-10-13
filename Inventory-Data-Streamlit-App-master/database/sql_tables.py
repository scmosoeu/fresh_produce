# General libraries
import pandas as pd
import numpy as np
import streamlit as st

# SQLAlchemy imports
import urllib
from sqlalchemy import create_engine, insert, Table, MetaData, select
#import pyodbc

# Custom upload with connection string
from database.engine_info import server_info

# Creating a connection to MS SQL SERVER
params = urllib.parse.quote_plus(server_info)
engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)
connection = engine.connect()
metadata = MetaData(bind=engine)

# Upload SQL database
sales = pd.read_sql_table(
    table_name='Durban_Fresh_produce_market',
    con=connection,
    parse_dates=['Date']
)

@st.cache(suppress_st_warning=True)
def data_preparation(data_frame):
    """
    Returns a cleaned dataframe for data analysis

    Parameters
    -----------
    data_frame: DataFrame
        A dataframe with prices for fresh produce commodities

    Returns
    --------
    DataFrame
        A dataframe with the data set to the correct datatype
    """

    # Convert some of the columns to their appropriate data type
    float_columns = ['Weight_Kg', 'Low_Price', 'High_Price', 'Average_Price',
                    'Sales_Total', 'Total_Kg_Sold', 'Total_Qty_Sold', 'Stock_On_Hand']

    # Convert the columns to numeric
    for col in float_columns:
        # sales[col] = sales[col].astype(float)
        data_frame[col] = pd.to_numeric(data_frame[col])

    # Remove days whereby total sales equal 0 because it registers average_price as zero.
    filtered = data_frame[data_frame['Sales_Total'] != 0]

    # Consolidation of repeated sales in a single day of the same product to one day
    df = filtered.groupby(
        ['Province', 'Container', 'Size_Grade', 'Weight_Kg', 'Commodities', 'Date']
    )[
        ['Low_Price', 'High_Price', 'Sales_Total', 'Total_Qty_Sold', 'Total_Kg_Sold', 'Stock_On_Hand']
    ].agg(
            {
                'Low_Price':min,
                'High_Price':max,
                'Sales_Total':sum,
                'Total_Qty_Sold':sum,
                'Total_Kg_Sold':sum,
                'Stock_On_Hand':sum
            }
    ).reset_index()

    df['avg_per_kg'] = round(df['Sales_Total'] / df['Total_Kg_Sold'], 2)

    return df

database = data_preparation(sales)
