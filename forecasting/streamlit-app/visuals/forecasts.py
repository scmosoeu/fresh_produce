# General libraries
import pandas as pd
import numpy as np
from statsmodels.tsa.filters.hp_filter import hpfilter

# Plotting libraries
import plotly.graph_objects as go

# Import custom functions
from models.arima_model import arima_forecast

def plot_forecast(data, col, product, periods):
    """
    Returns ....

    Parameters
    -----------
    data: DataFrame
        A dataframe containing a series of which a trend is to be determined
    col: str
        A column name from which the trend is to be determined
    product: str
        A column name of series from which a trend is to be determined
    periods: int
        Forecast horizon in units of the series

    Returns
    --------
    A plotly graph object
    """ 
    price_cycle, price_trend = hpfilter(data[col])

    predictions = arima_forecast(data, 'avg_per_kg', periods)

    fig = go.Figure(
        data=[
            go.Scatter(
                x=data.index,
                y=data[col],
                name='Average'
            ),
            go.Scatter(
                x=data.index,
                y=price_trend,
                name='Trend'
            )
        ],

        layout=go.Layout(
            title_text=f'Price of {product}',
            title_x=0.5,
            xaxis={'title': 'Date'},
            yaxis={'title': 'R/kg'},
            template='none'
        )
    )
    return fig


