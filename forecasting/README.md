# World temperature forcasting with Plotly

The repository contains scripts for forecasting and plotting world temperatures with Plotly in Python.

Models used for forecasting:
- ARIMA - yearly,
- SARIMA - yearly,
- Facebook Prophet - yearly and seasonal,
- HWES - seasonal.

Countries included in prediction:
- Japan,
- Sweden.

## ARIMA
ARIMA is an Autoregressive Integrated Moving Average.

<div align="center">
  <img src="plots/arima_yearly_jap.png" width="50%">
</div>

## HWES
HWES is a Holt-Winters Exponential Smoothing.

<div align="center">
  <img src="plots/hwes_yearly_jap.png" width="100%">
</div>

## Facebook Prophet
### Seasonal

<div align="center">
  <img src="plots/prophet_seasonal_jap.png" width="80%">
</div>

### Yearly

<div align="center">
  <img src="plots/prophet_yearly_jap.png" width="50%">
</div>

## Mean errors
I calculated mean error for each method and each country. _Y_ stands fro a yearly analysis. _S_ stands for a seasonal analysis.

|            | arima_y  | hwes_s   | prophet_s | prophet_y | sarima_s  | sarima_y  |
|------------|----------|----------|-----------|-----------|-----------|-----------|
| jap        | 0.521628 | 0.893788 | 0.873801  | 0.681572  | 0.818446  | 0.567941  |
| swe        | 0.810102 | 2.826763 | 1.559867  | 0.964609  | 1.816844  | 1.174252  |
