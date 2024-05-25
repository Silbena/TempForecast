import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_predict

df = pd.read_csv('data/filtered.csv')
df.drop(columns=['record_id', 'Latitude', 'Longitude', 'month', 'AverageTemperatureUncertaintyCelsius'], inplace= True)
sweden = df[df['Country'] == 'Sweden']
sweden = sweden.groupby('year', as_index = True).mean(numeric_only = True)

def arima(dataframe):
    model = ARIMA(dataframe['AverageTemperatureCelsius'], order=(2, 0, 2)).fit()
    return model

def plot_arima(dataframe, arima_model):
    _, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dataframe.index, dataframe['AverageTemperatureCelsius'], label='Observed')
    plot_predict(arima_model, start = 2013, end = 2013 + 250, dynamic = True, ax = ax)
    ax.set_title('Average Temperature Forecast for Sweden (ARIMA)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature (Celsius)')
    ax.legend()
    plt.show()

def main():
    model = arima(sweden)
    print(model.summary())
    plot_arima(sweden, model)

if __name__ == "__main__":
    main()
