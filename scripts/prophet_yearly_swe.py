from prophet import Prophet
import pandas as pd
import plotly.express as px

def load_dataset(country_name: str):
    df = pd.read_csv('data/filtered.csv')
    df = df[df['Country'] == country_name]

    df = df.groupby('year', as_index = False).mean(numeric_only = True)
    
    df['ds'] = df['year'].astype(str) + '-01-01'

    df = df.loc[:, ['ds','AverageTemperatureCelsius']]
    df.rename(columns={'AverageTemperatureCelsius':'y'}, inplace = True)

    return df

def modelling(df):
    model = Prophet(seasonality_mode='multiplicative')
    model.fit(df)
    future = model.make_future_dataframe(freq = 'YE', periods = 20, include_history = False)
    forecast = model.predict(future)

    return forecast

def plot_prophet(past_df, forecast_df):

    base = px.line(past_df, x = 'ds', y = 'y').data[0]

    fig = px.line(forecast_df, x = 'ds', y = ['yhat', 'yhat_lower','yhat_upper'],
                  color_discrete_sequence = ['#FF7F0E', 'rgba(255, 165, 0, 0.3)', 'rgba(255, 165, 0, 0.3)'],
                  title = 'Seasonal Temperature Forecast for Sweden (Prophet)',
                  labels = {'ds': 'Temperature [C]'},
                  width = 3000,
                  height = 600
                  ).add_trace(base)

    fig.update_layout(font = dict(size = 30), legend_title_text = 'Legend')
    fig.show()

def main():
    df = load_dataset('Sweden')
    print(df.dtypes)
    print(df)
    forecast = modelling(df)
    plot_prophet(df, forecast)

if __name__ == "__main__":
    main()
