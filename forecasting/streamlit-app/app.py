# General libraries
import pandas as pd
import numpy as np

# Plotting libraries
import plotly.graph_objects as go

# App libraries 
import streamlit as st

# DATABASE
from database.sql_tables import database    

############################### STREAMLIT APP #########################################################

commodity = sales['commodity'].unique()

selected_commodity = st.sidebar.selectbox(
    label="Commodity",
    options=commodity
)

st.write("You selected", selected_commodity)