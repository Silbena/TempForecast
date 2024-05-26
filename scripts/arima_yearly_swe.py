import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
import parsing as ps

def load_dataset(country_name: str):
    df = pd.read_csv('data/filtered.csv')
    df = df[df['Country'] == country_name]
    df = df.groupby('year', as_index = True)['AverageTemperatureCelsius'].mean()
    df.interpolate(inplace = True)
    
    return df

def arima(train, test):
    model = ARIMA(train, order=(1, 0, 1)).fit()

    prediction = model.get_prediction(start = test.index[0], end = test.index[-1])
    pred_mean = prediction.predicted_mean

    forecast = model.get_forecast(250)
    fore_mean = forecast.predicted_mean
    fore_conf_ints = forecast.conf_int()
    year_range = np.arange(2014, 2014+250)

    fore_mean.index = year_range
    fore_conf_ints.index = year_range

    return pred_mean, fore_mean, fore_conf_ints

def plot_arima(past_df, fore_mean, fore_conf_ints, country_name):

    base = px.line(past_df, x = past_df.index, y = 'AverageTemperatureCelsius').data[0]

    fig = px.line(x = fore_mean.index, y = fore_mean.values,
                     title = f'Yearly Temperature Forecast for {country_name} (ARIMA)',
                     labels = {'x':'Year', 'y':'Temperature [C]'},
                     width = 1400,
                     height = 600,
                     color_discrete_sequence = ['#FF7F0E']
                     ).add_trace(base)
    
    fig.add_scatter(x=fore_mean.index, y=fore_conf_ints['lower AverageTemperatureCelsius'],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Lower CI')
    fig.add_scatter(x=fore_mean.index, y=fore_conf_ints['upper AverageTemperatureCelsius'],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Upper CI', fill='tonexty')

    fig.update_layout(font = dict(size = 30), legend_title_text = 'Legend')

    args = ps.parse()
    if args.save == 0:
        fig.show()
    if args.save == 1:
        path = f'plots/arima_yearly_{country_name.lower()[:3]}.png'
        fig.write_image(path)
        print(f'Plot saved under: {path}')

def arima_error(df):
    mean_error = 0
    splits = 5
    tscv = TimeSeriesSplit(n_splits= splits)

    for train_index, test_index in tscv.split(df):
        train, test = df.iloc[train_index], df.iloc[test_index]
        pred_mean, _, _ = arima(train, test)
        mean_error += mean_absolute_error(test, pred_mean)
    
    mean_error = mean_error/5

    print(f'The mean error: {mean_error}')

    return mean_error

def calculations(country_name):
    df = load_dataset(country_name)
    _, fore_mean, fore_conf_ints = arima(df, df)
    mean_error = arima_error(df)

    return df, fore_mean, fore_conf_ints, mean_error

def main():
    country_name = 'Sweden'
    df, fore_mean, fore_conf_ints, mean_error = calculations(country_name)
    plot_arima(df, fore_mean, fore_conf_ints, country_name)

if __name__ == "__main__":
    main()
