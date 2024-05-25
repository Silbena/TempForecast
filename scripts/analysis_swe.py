import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
import matplotlib.pyplot as plt

df = pd.read_csv('data/filtered.csv')
df.drop(columns=['record_id', 'Latitude', 'Longitude', 'month', 'AverageTemperatureUncertaintyCelsius'], inplace= True)
sweden = df[df['Country'] == 'Sweden']
sweden = sweden.groupby('year', as_index = True).mean(numeric_only = True)

# Augmented Dickey-Fuller unit root test
result = adfuller(sweden['AverageTemperatureCelsius'])

if result[0] < 0.05:
    print('Yey! The time series is stationary. Set: d=0.')
else:
    print('Oh no! The time series ism\'t stationary. Need to adjust differencing operations (d).')

# Auto-correlation plot
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(16,4))
ax1.plot(sweden['AverageTemperatureCelsius'])
plot_acf(sweden['AverageTemperatureCelsius'], ax = ax2)

# Nr of differences 
nr_differences = ndiffs(sweden['AverageTemperatureCelsius'], test = 'adf')
print(f'Number of differeces to set: {nr_differences}')

# Order of autoregresssive term (nr of lags used as predictors)

# Partial auto-corrrelation plot
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(16,4))
ax1.plot(sweden['AverageTemperatureCelsius'])
plot_pacf(sweden['AverageTemperatureCelsius'], ax = ax2)
plt.show()

# From the plot: p = 2 would be the best

# q - order of Moving Average Term
# Would opt for q = 2
