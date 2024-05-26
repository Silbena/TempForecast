import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
import plotly.express as px
import parsing as ps

def load_dataset(country_name: str):
    df = pd.read_csv('data/filtered.csv')
    df = df[df['Country'] == country_name]

    date_str = df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
    df['date'] = pd.to_datetime(date_str, format='%Y-%m-%d')

    df = df.groupby('date')['AverageTemperatureCelsius'].mean()
    df = df.asfreq(freq='MS')
    df.interpolate(inplace=True)

    return df

def hwes(df):
    model = ETSModel(df, trend = 'add', seasonal = 'add', seasonal_periods= 12, freq = 'MS').fit()
    start_date = df.index[-1]
    predictions = model.get_prediction(start = start_date, end = '2261-08-01').summary_frame()
    pred_mean = predictions['mean']
    conf_ints = (predictions['pi_lower'], predictions['pi_upper'])

    return pred_mean, conf_ints

def plot_hwes(df, pred_mean, conf_ints, country_name):
    trace = px.line(x = df.index, y = df.values)

    fig = px.line(x = pred_mean.index, y = pred_mean.values,
                     title = f'Seasonal Temperature Forecast for {country_name} (HWES)',
                     labels = {'x':'Year', 'y':'Temperature [C]'},
                     width = 4000,
                     height = 600,
                     color_discrete_sequence = ['#FF7F0E']
                     ).add_trace(trace.data[0])
    
    fig.add_scatter(x=pred_mean.index, y=conf_ints[0],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Lower CI')
    fig.add_scatter(x=pred_mean.index, y=conf_ints[1],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Upper CI', fill='tonexty')

    fig.update_layout(font = dict(size = 30))
    fig.update_traces(marker = dict(opacity = 0.7))

    fig.show()

def main():
    country_name = 'Japan'
    df = load_dataset(country_name)
    pred_mean, conf_ints = hwes(df)
    plot_hwes(df, pred_mean, conf_ints, country_name)

if __name__ == "__main__":
    main()
