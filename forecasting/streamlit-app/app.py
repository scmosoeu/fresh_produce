# General libraries
import pandas as pd
import numpy as np

# App libraries 
import streamlit as st

# import sql DATABASE
from database.sql_tables import database

# Custom libraries
from visuals.decomposition import plot_seasonality

############################### STREAMLIT APP #########################################################

sales = database['sales']
inventory = database['inventory']

commodity = sales['commodity'].unique()

selected_commodity = st.sidebar.selectbox(
    label="Commodity",
    options=commodity
)

df_sales = sales[sales['commodity'] == selected_commodity][['date', 'ave_per_kg']]

price = df_sales.groupby('date')['ave_per_kg'].mean()
price = pd.DataFrame(price)
price = price.asfreq('B', method='backfill')

result = plot_seasonality(price['ave_per_kg'], selected_commodity)

st.plotly_chart(result)