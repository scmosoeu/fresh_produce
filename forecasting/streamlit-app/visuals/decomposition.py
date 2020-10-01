# General libraries
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

# Plotting libraries
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_seasonality(data, product):
    """
    Returns ....

    Parameters
    -----------
    data: DataFrame
    title: str

    Returns
    --------
    A plotly graph object
    """ 
    seasoned_data = seasonal_decompose(data['ave_per_kg'])

    fig = make_subplots(
        rows=4, 
        cols=1,
        shared_xaxes=True, 
        vertical_spacing=0.02
    )

    fig.append_trace(
        go.Scatter(
            x=data.index,
            y=seasoned_data.observed.values
        ),
        row=1,
        col=1
    )
    fig.append_trace(
        go.Scatter(
            x=data.index,
            y=seasoned_data.trend.values
        ),
        row=2,
        col=1
    )
    fig.append_trace(
        go.Scatter(
            x=data.index,
            y=seasoned_data.seasonal.values
        ),
        row=3,
        col=1
    )
    fig.append_trace(
        go.Scatter(
            x=data.index,
            y=seasoned_data.resid.values
        ),
        row=4,
        col=1
    )
    fig.update_layout(
        title_text=f'Price of {product}',
        title_x=0.5,
        template='none'
    )

    return fig

