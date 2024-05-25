import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
import matplotlib.pyplot as plt

df = pd.read_csv('data/filtered.csv')
df = df[df['Country'] == 'Sweden']
df = df.groupby('year', as_index = True)['AverageTemperatureCelsius'].mean()

# Augmented Dickey-Fuller unit root test
result = adfuller(df)

if result[0] < 0.05:
    print('Yey! The time series is stationary. Set: d=0.')
else:
    print('Oh no! The time series ism\'t stationary. Need to adjust differencing operations (d).')

# Auto-correlation plot
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(16,4))
ax1.plot(df)
plot_acf(df, ax = ax2)

# Nr of differences 
nr_differences = ndiffs(df, test = 'adf')
print(f'Number of differeces to set: {nr_differences}')

# Order of autoregresssive term (nr of lags used as predictors)

# Partial auto-corrrelation plot
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(16,4))
ax1.plot(df)
plot_pacf(df, ax = ax2)
plt.show()

# From the plot: p = 2 would be the best

# q - order of Moving Average Term
# Would opt for q = 2
