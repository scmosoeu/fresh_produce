# General libraries
import pandas as pd
import numpy as np
from statsmodels.tsa.filters.hp_filter import hpfilter
import datetime

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
    start = data.index[-1] + datetime.timedelta(days=1) # Prediction start date
    prediction_index = pd.date_range(start, periods=periods, freq='B')

    fig = go.Figure(
        data=[
            go.Scatter(
                x=data.index,
                y=data[col],
                name='Average',
                mode='lines'
            ),
            go.Scatter(
                x=data.index,
                y=round(price_trend,2),
                name='Trend',
                mode='lines'
            ),
            go.Scatter(
                x=prediction_index,
                y=predictions,
                name='Forecast',
                mode='lines'
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


