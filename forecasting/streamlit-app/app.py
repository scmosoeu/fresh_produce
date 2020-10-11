# General libraries
import pandas as pd
import numpy as np

# App libraries 
import streamlit as st
import datetime

# import sql DATABASE
from database.sql_tables import database

# Custom libraries
from visuals.forecasts import plot_forecast

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

# INSERT CALENDAR
today = datetime.date.today()
future_date = today + datetime.timedelta(days=1)
forecast_date = st.sidebar.date_input('Forecast date', future_date)

if forecast_date <= today:
    st.sidebar.error('Error: Forecast date must fall after today\'s date.')

df = database[
    (database['Commodities'] == selected_commodity) & \
    (database['Weight_Kg'] == selected_weight) & \
    (database['Size_Grade'] == selected_grade)
][['Date', 'avg_per_kg']]

price = df.groupby('Date')['avg_per_kg'].mean()
price = pd.DataFrame(price)
price = price.asfreq('B', method='backfill')

result = plot_forecast(price, 'avg_per_kg', selected_commodity, 30)

st.plotly_chart(result)