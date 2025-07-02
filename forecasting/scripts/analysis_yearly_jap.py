import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv('data/filtered.csv')
    df = df[df['Country'] == 'Japan']

    df = df.groupby('year',
                    as_index=True)['AverageTemperatureCelsius'].mean()

    result = adfuller(df)

    if result[0] < 0.05:
        print('The time series is stationary. Set: d=0.')
    else:
        print('The time series ism\'t stationary. Need to adjust differencing operations (d).')

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
    ax1.plot(df)
    plot_acf(df,
             ax=ax2)

    nr_differences = ndiffs(df, test='adf')
    print(f'Number of differeces to set: {nr_differences}')

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,4))
    ax1.plot(df)
    plot_pacf(df,
              ax=ax2)
    
    plt.show()


if __name__ == '__main__':
    main()
