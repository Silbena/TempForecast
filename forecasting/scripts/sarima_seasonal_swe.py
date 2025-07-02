import pandas as pd
import statsmodels.api as sm
import plotly.express as px
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
import parsing as ps


def load_dataset(country_name: str):
    df = pd.read_csv('data/filtered.csv')
    df = df[df['Country'] == country_name]

    date_str = df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
    df['date'] = pd.to_datetime(date_str, format='%Y-%m-%d')

    dataset = df.groupby('date')['AverageTemperatureCelsius'].mean()
    dataset = dataset.asfreq(freq='MS')
    dataset.interpolate(inplace=True)

    return dataset


def sarima(train, test):
    model = sm.tsa.SARIMAX(train, order=(2, 0, 2), seasonal_order=(1, 0, 2, 12)).fit()

    prediction = model.get_prediction(start=test.index[0],
                                      end=test.index[-1])
    
    pred_mean = prediction.predicted_mean

    forecast = model.get_forecast(steps=2976)
    fore_mean = forecast.predicted_mean
    fore_conf_ints = forecast.conf_int()

    return pred_mean, fore_mean, fore_conf_ints


def plot_arima(df, fore_mean, fore_conf_ints, country_name):
    trace = px.line(x=df.index, 
                    y=df.values)

    fig = px.line(x=fore_mean.index,
                  y=fore_mean.values,
                  title = f'Seasonal Temperature Forecast for {country_name} (SARIMA)',
                  labels = {'x':'Year', 'y':'Temperature [C]'},
                  width = 3000,
                  height = 600,
                  color_discrete_sequence = ['#FF7F0E']
                  ).add_trace(trace.data[0])
    
    fig.add_scatter(x=fore_mean.index,
                    y=fore_conf_ints['lower AverageTemperatureCelsius'],
                    mode='lines',
                    line=dict(color='rgba(255, 165, 0, 0.3)'),
                    name='Lower CI')
    
    fig.add_scatter(x=fore_mean.index,
                    y=fore_conf_ints['upper AverageTemperatureCelsius'],
                    mode='lines',
                    line=dict(color='rgba(255, 165, 0, 0.3)'),
                    name='Upper CI',
                    fill='tonexty')

    fig.update_layout(font=dict(size=30))
    fig.update_traces(marker=dict(opacity=0.7))

    args = ps.parse()
    if args.save == 0:
        fig.show()

    if args.save == 1:
        path = f'plots/sarima_seasonal_{country_name.lower()[:3]}.png'
        fig.write_image(path)
        print(f'Plot saved under: {path}')


def sarima_error(df):
    mean_error = 0
    splits = 5
    tscv = TimeSeriesSplit(n_splits=splits)

    for train_index, test_index in tscv.split(df):
        train, test = df.iloc[train_index], df.iloc[test_index]
        pred_mean, _, _ = sarima(train, test)
        mean_error += mean_absolute_error(test, pred_mean)
    
    mean_error /= 5

    print(f'The mean error: {mean_error}')

    return mean_error


def calculations(country_name):
    df = load_dataset(country_name)
    _, fore_mean, fore_conf_ints = sarima(df, df)
    mean_error = sarima_error(df)

    return df, fore_mean, fore_conf_ints, mean_error


def main():
    country_name = 'Sweden'
    df, fore_mean, fore_conf_ints, _ = calculations(country_name)
    plot_arima(df, fore_mean, fore_conf_ints, country_name)


if __name__ == "__main__":
    main()
