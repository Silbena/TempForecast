import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
import matplotlib as plt

df = pd.read_csv('data/filtered.csv')
df.drop(columns=['record_id', 'Latitude', 'Longitude', 'month'], inplace= True)
sweden = df[df['Country'] == 'Sweden']
sweden = sweden.groupby('year', as_index = False).mean(numeric_only = True)

