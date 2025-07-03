# World Temperature Analysis

## Data
The data come from the [Climate Change: Earth Surface Temperature Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data/data?select=GlobalLandTemperaturesByCity.csv) dataset.

Data were filtered with **overview**&rarr; **scripts** &rarr; **filtering.py**.

## Overview
8 countries on different continents were chosen, although for some there were no temperature records from the middle XVIII to middle XIX centure do not exist.
The temperatures in most of the chosen countries were steadily increasing in the course of last century.

<div align="center"/>
  <img src="overview/plots/line.png" alt=overview width=70%/>
</div>

## Forecasting
Here, I forecasted the temperatures for the years to come in Japan with Faceboook Prophet. To see more forecasts with ARIMA, SARIMA, Facebook Prophet, and HWES go to &rarr; **forecasting**.

<div align="center"/>
  <img src="forecasting/plots/prophet_yearly_jap.png", alt=forecasting width=50%>
</div>
