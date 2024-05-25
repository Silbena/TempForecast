import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
import matplotlib.pyplot as plt

df = pd.read_csv('data/filtered.csv')
df = df[df['Country'] == 'Japan']

date_str = df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
df['date'] = pd.to_datetime(date_str, format='%Y-%m-%d')

df = df.groupby('date')['AverageTemperatureCelsius'].mean()
df = df.asfreq(freq='MS')
df.interpolate(inplace=True)

# Augmented Dickey-Fuller unit root test
result = adfuller(df)

if result[0] < 0.05:
    print('Yey! The time series is stationary. Set: d=0.')
else:
    print('Oh no! The time series ism\'t stationary. Need to adjust differencing operations (d).')

# Auto-correlation plot
plot_acf(df)
plt.show()

# Nr of differences 
nr_differences = ndiffs(df, test = 'adf')
print(f'Number of differeces to set: {nr_differences}')

# Order of autoregresssive term (nr of lags used as predictors)

# Partial auto-corrrelation plot
plot_pacf(df)
plt.show()

# From the plot: p = 1 would be the best
# q - order of Moving Average Term
# Would opt for q = 1
