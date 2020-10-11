# General libraries
import pandas as pd
import numpy as np

# App libraries 
import streamlit as st

# import sql DATABASE
from database.sql_tables import database

# Custom libraries
from visuals.trend import plot_trend

############################### STREAMLIT APP #########################################################

commodity = database['Commodities'].unique()

selected_commodity = st.sidebar.selectbox(
    label="Commodity",
    options=commodity
)

df = database[database['Commodities'] == selected_commodity][['Date', 'avg_per_kg']]

price = df.groupby('Date')['avg_per_kg'].mean()
price = pd.DataFrame(price)
price = price.asfreq('B', method='backfill')

result = plot_trend(price, selected_commodity)

st.plotly_chart(result)