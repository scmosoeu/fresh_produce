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

weight = database[database['Commodities'] == selected_commodity]['Weight_Kg'].unique()

selected_weight = st.sidebar.selectbox(
    label="Weight",
    options=weight
)

grade = database[
    (database['Commodities'] == selected_commodity) & \
    (database['Weight_Kg'] == selected_weight)
]['Size_Grade'].unique()

selected_grade = st.sidebar.selectbox(
    label="Size Grade",
    options=grade
)

df = database[
    (database['Commodities'] == selected_commodity) & \
    (database['Weight_Kg'] == selected_weight) & \
    (database['Size_Grdae'] == selected_grade)
][['Date', 'avg_per_kg']]

price = df.groupby('Date')['avg_per_kg'].mean()
price = pd.DataFrame(price)
price = price.asfreq('B', method='backfill')

result = plot_trend(price, 'avg_per_kg', selected_commodity)

st.plotly_chart(result)