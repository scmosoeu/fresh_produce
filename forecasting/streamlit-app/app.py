# General libraries
import pandas as pd
import numpy as np

# App libraries 
import streamlit as st

# import sql DATABASE
from database.sql_tables import database    

############################### STREAMLIT APP #########################################################

sales = database['sales']

commodity = sales['commodity'].unique()

selected_commodity = st.sidebar.selectbox(
    label="Commodity",
    options=commodity
)

st.write("You selected", selected_commodity)