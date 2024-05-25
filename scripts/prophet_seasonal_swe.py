from prophet import Prophet
import pandas as pd
import plotly.express as px

def load_dataset(country_name: str):
    df = pd.read_csv('data/filtered.csv')
    df = df[df['Country'] == country_name]

    date_str = df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
    df['ds'] = pd.to_datetime(date_str, format='%Y-%m-%d')

    df = df.loc[:, ['ds','AverageTemperatureCelsius']]
    df = df.groupby('ds', as_index = False).mean()
    df.rename(columns={'AverageTemperatureCelsius' : 'y'}, inplace = True)

    return df

def modelling(df):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(freq = 'MS', periods = 240, include_history = False)
    forecast = model.predict(future)

    return forecast

def plot_prophet(past_df, forecast_df):

    base = px.line(past_df, x = 'ds', y = 'y').data[0]

    fig = px.line(forecast_df, x = 'ds', y = ['yhat', 'yhat_lower','yhat_upper'],
                  color_discrete_sequence = ['#FF7F0E', 'rgba(255, 165, 0, 0.3)', 'rgba(255, 165, 0, 0.3)'],
                  title = 'Seasonal Temperature Forecast for Sweden (Prophet)',
                  labels = {'value': 'Temperature [C]'},
                  width = 2000,
                  height = 600
                  ).add_trace(base)

    fig.update_layout(font = dict(size = 30), legend_title_text = 'Legend')
    fig.show()

def main():
    df = load_dataset('Sweden')
    forecast = modelling(df)
    plot_prophet(df, forecast)

if __name__ == "__main__":
    main()
