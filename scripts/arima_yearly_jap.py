import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px

def load_dataset(country_name: str):
    df = pd.read_csv('data/filtered.csv')
    df = df[df['Country'] == country_name]
    df = df.groupby('year', as_index = True)['AverageTemperatureCelsius'].mean()
    
    return df

def arima(df):
    model = ARIMA(df, order=(1, 0, 24)).fit()
    predictions = model.get_forecast(steps = 250)

    pred_mean = predictions.predicted_mean
    conf_ints = predictions.conf_int()

    year_range = np.arange(2014, 2014+250)
    pred_mean.index = year_range
    conf_ints.index = year_range

    return pred_mean, conf_ints

def plot_arima(past_df, pred_mean, conf_ints):

    base = px.line(past_df, x = past_df.index, y = 'AverageTemperatureCelsius').data[0]

    fig = px.line(x = pred_mean.index, y = pred_mean.values,
                     title = 'Yearly Temperature Forecast for Sweden (ARIMA)',
                     labels = {'x':'Year', 'y':'Temperature [C]'},
                     width = 1400,
                     height = 600,
                     color_discrete_sequence = ['#FF7F0E']
                     ).add_trace(base)
    
    fig.add_scatter(x=pred_mean.index, y=conf_ints['lower AverageTemperatureCelsius'],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Lower CI')
    fig.add_scatter(x=pred_mean.index, y=conf_ints['upper AverageTemperatureCelsius'],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Upper CI', fill='tonexty')

    fig.update_layout(font = dict(size = 30), legend_title_text = 'Legend')
    fig.show()

def main():
    df = load_dataset('Japan')
    pred_mean, conf_ints = arima(df)
    print(pred_mean.head())
    plot_arima(df, pred_mean, conf_ints)

if __name__ == "__main__":
    main()
