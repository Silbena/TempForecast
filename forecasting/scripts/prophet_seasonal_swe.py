from prophet import Prophet
import pandas as pd
import plotly.express as px
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
import parsing as ps


def load_dataset(country_name: str):
    df = pd.read_csv('data/filtered.csv')
    df = df[df['Country'] == country_name]

    date_str = df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
    df['ds'] = pd.to_datetime(date_str, format='%Y-%m-%d')

    df = df.loc[:, ['ds','AverageTemperatureCelsius']]
    
    df = df.groupby('ds', as_index = False).mean()

    df.rename(columns={'AverageTemperatureCelsius' : 'y'},
              inplace=True)

    return df


def modelling(train, test):
    model = Prophet()
    model.fit(train)

    predictions = model.predict(test)

    time_frame = model.make_future_dataframe(freq='MS',
                                             periods=240,
                                             include_history=False)
    forecast = model.predict(time_frame)

    return predictions, forecast


def plot_prophet(past_df, forecast_df, country_name):

    base = px.line(past_df,
                   x='ds',
                   y='y'
                   ).data[0]

    fig = px.line(forecast_df,
                  x='ds',
                  y='yhat',
                  title = f'Seasonal Temperature Forecast for {country_name} (Prophet)',
                  labels = {'ds':'Year', 'yhat':'Temperature [C]'},
                  width = 2000,
                  height = 600,
                  color_discrete_sequence = ['#FF7F0E']
                  ).add_trace(base)
    
    fig.add_scatter(x=forecast_df['ds'],
                    y=forecast_df['yhat_lower'],
                    mode='lines',
                    line=dict(color='rgba(255, 165, 0, 0.3)'),
                    name='Lower CI')
    
    fig.add_scatter(x=forecast_df['ds'],
                    y=forecast_df['yhat_upper'],
                    mode='lines',
                    line=dict(color='rgba(255, 165, 0, 0.3)'),
                    name='Upper CI',
                    fill='tonexty')

    fig.update_layout(font=dict(size=30),
                      legend_title_text='Legend')

    args = ps.parse()
    if args.save == 0:
        fig.show()
        
    if args.save == 1:
        path = f'plots/prophet_seasonal_{country_name.lower()[:3]}.png'
        fig.write_image(path)
        print(f'Plot saved under: {path}')


def prophet_error(df):
    mean_error = 0
    splits = 5
    tscv = TimeSeriesSplit(n_splits=splits)

    for train_index, test_index in tscv.split(df):
        train, test = df.iloc[train_index], df.iloc[test_index]
        predictions, _ = modelling(train, test)
        mean_error += mean_absolute_error(test['y'], predictions['yhat'])

    mean_error /= splits
    print(f'The mean error: {mean_error}')

    return mean_error


def calculations(country_name):
    df = load_dataset(country_name)
    _, forecast = modelling(df, df)
    mean_error = prophet_error(df)

    return df, forecast, mean_error


def main():
    country_name = 'Sweden'
    df, forecast, _ = calculations(country_name)
    plot_prophet(df, forecast, country_name)


if __name__ == "__main__":
    main()
