from pmdarima import auto_arima


def arima_forecast(df, col, num_of_periods):
    """
    Returns a trained ARIMA model

    Parameters
    -----------
    df: DataFrame
        A dataframe consisting of a column from which an ARIMA model 
        will be developed
    col: str
        A column name from which an ARIMA model will be developed
    num_of_periods: int
        Number of periods ahead that the model will predict

    Returns
    --------
    pd.Series
        A series of predictions with the number of periods as the index
    """

    model = auto_arima(df[col], error_action='ignore', suppress_warnings=True)
    pred = model.predict(n_periods=num_of_periods)

    return pred  
