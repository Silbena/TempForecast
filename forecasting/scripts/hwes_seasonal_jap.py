import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
import plotly.express as px
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
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

def hwes(train, test):
    model = ETSModel(train, error='add', trend='add', seasonal='add', seasonal_periods=12).fit()

    predictions = model.get_prediction(start=test.index[0], end=test.index[-1]).summary_frame()
    pred_mean = predictions['mean']

    forecast = model.get_prediction(start = test.index[-1], end = '2261-08-01').summary_frame()
    fore_mean = forecast['mean']
    fore_conf_ints = (forecast['pi_lower'], forecast['pi_upper'])

    return pred_mean, fore_mean, fore_conf_ints

def plot_hwes(past_df, fore_mean, fore_conf_ints, country_name):
    base = px.line(past_df, x=past_df.index, y='AverageTemperatureCelsius').data[0]

    fig = px.line(x=fore_mean.index, y=fore_mean.values,
                  title=f'Seasonal Temperature Forecast for {country_name} (HWES)',
                  labels={'x': 'Year', 'y': 'Temperature [C]'},
                  width=3000,
                  height=600,
                  color_discrete_sequence=['#FF7F0E']).add_trace(base)

    fig.add_scatter(x=fore_mean.index, y=fore_conf_ints[0],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Lower CI')
    fig.add_scatter(x=fore_mean.index, y=fore_conf_ints[1],
                    mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)'), name='Upper CI', fill='tonexty')

    fig.update_layout(font=dict(size=30))
    fig.update_traces(marker=dict(opacity=0.7))

    args = ps.parse()
    if args.save == 0:
        fig.show()
    if args.save == 1:
        path = f'plots/hwes_yearly_{country_name.lower()[:3]}.png'
        fig.write_image(path)
        print(f'Plot saved under: {path}')

def hwes_error(df):
    mean_error = 0
    splits = 5
    tscv = TimeSeriesSplit(n_splits=splits)

    for train_index, test_index in tscv.split(df):
        train, test = df.iloc[train_index], df.iloc[test_index]
        pred_mean, _, _ = hwes(train, test)
        mean_error += mean_absolute_error(test, pred_mean)

    mean_error /= splits
    print(f'The mean error: {mean_error}')

    return mean_error

def calculations(country_name):
    df = load_dataset(country_name)
    _, fore_mean, fore_conf_ints = hwes(df, df)
    mean_error = hwes_error(df)

    return df, fore_mean, fore_conf_ints, mean_error

def main():
    country_name = 'Japan'
    df, fore_mean, fore_conf_ints, mean_error = calculations(country_name)
    plot_hwes(df, fore_mean, fore_conf_ints, country_name)

if __name__ == "__main__":
    main()
