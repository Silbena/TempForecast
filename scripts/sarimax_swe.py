import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Loading data and calculating average
df = pd.read_csv('data/filtered.csv')
date_str = df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
df['date'] = pd.to_datetime(date_str, format='%Y-%m-%d')
df.drop(columns=['record_id', 'Latitude', 'Longitude', 'month'], inplace= True)

# Assuming your data is in a pandas DataFrame `df` with a datetime index and a column 'temperature'
plot_acf(df['AverageTemperatureCelsius'])
plot_pacf(df['AverageTemperatureCelsius'])
plt.show()