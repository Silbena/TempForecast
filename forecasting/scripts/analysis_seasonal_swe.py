import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv('data/filtered.csv')
    df = df[df['Country'] == 'Sweden']

    date_str = df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'

    df['date'] = pd.to_datetime(date_str,
                                format='%Y-%m-%d')

    df = df.groupby('date')['AverageTemperatureCelsius'].mean()
    df = df.asfreq(freq='MS')
    df.interpolate(inplace=True)

    result = adfuller(df)

    if result[0] < 0.05:
        print('The time series is stationary. Set: d=0.')
    else:
        print('The time series ism\'t stationary. Need to adjust differencing operations (d).')

    plot_acf(df)
    plt.show()

    nr_differences = ndiffs(df,
                            test='adf')
    
    print(f'Number of differeces to set: {nr_differences}')

    plot_pacf(df)
    plt.show()


if __name__ == '__main__':
    main()
