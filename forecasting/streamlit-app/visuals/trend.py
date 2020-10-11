# General libraries
import pandas as pd
import numpy as np
from statsmodels.tsa.filters.hp_filter import hpfilter

# Plotting libraries
import plotly.graph_objects as go

def plot_trend(data, product):
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
    price_cycle, price_trend = hpfilter(data['avg_per_kg'])

    fig = go.Figure(
        data=[
            go.Scatter(
                x=data.index,
                y=data['avg_per_kg'],
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

