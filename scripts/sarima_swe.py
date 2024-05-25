import pandas as pd
import statsmodels.api as sm
import plotly.express as px
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

def sarima(dataset):
    model = sm.tsa.SARIMAX(dataset, order=(2, 0, 2), seasonal_order=(0,1,1,12)).fit()
    steps = 248*12
    predictions = model.get_forecast(steps = steps)

    return predictions

def plot_arima(df, predictions):
    trace = px.line(x = df.index, y = df.values)
    
    pred_mean = predictions.predicted_mean
    conf_ints = predictions.conf_int()

    fig = px.line(x = pred_mean.index, y = pred_mean.values,
                     title = 'Seasonal Temperature Forecast for Sweden (SARIMA)',
                     width = 4000,
                     height = 600,
                     color_discrete_sequence = ['#FF7F0E']
                     ).add_trace(trace.data[0])
    
    fig.add_scatter(x=pred_mean.index, y=conf_ints['lower AverageTemperatureCelsius'],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Lower CI')
    fig.add_scatter(x=pred_mean.index, y=conf_ints['upper AverageTemperatureCelsius'],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Upper CI', fill='tonexty')


    fig.update_layout(font = dict(size = 30))
    fig.update_traces(marker = dict(opacity = 0.7))

    fig.show()

def main():
    sweden = load_dataset('Sweden')
    model = sarima(sweden)
    plot_arima(sweden, model)

if __name__ == "__main__":
    main()
