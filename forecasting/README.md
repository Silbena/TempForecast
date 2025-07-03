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

![ARIMA Yearly Japan](plots/arima_yearly_jap.png)
![ARIMA Yearly Sweden](plots/arima_yearly_swe.png)

## HWES
HWES is a Holt-Winters Exponential Smoothing.

![HWES Yearly Japan](plots/hwes_yearly_jap.png)
![HWES Yearly Sweden](plots/hwes_yearly_swe.png)

## Facebook Prophet
![Prophet Seasonal Japan](plots/prophet_seasonal_jap.png)
![Prophet Seasonal Sweden](plots/prophet_seasonal_swe.png)

![Prophet Yearly Japan](plots/prophet_yearly_jap.png)
![Prophet Yearly Sweden](plots/prophet_yearly_swe.png)

## Comparison
|            | arima_y  | hwes_s   | prophet_s | prophet_y | sarima_s  | sarima_y  |
|------------|----------|----------|-----------|-----------|-----------|-----------|
| jap        | 0.521628 | 0.893788 | 0.873801  | 0.681572  | 0.818446  | 0.567941  |
| swe        | 0.810102 | 2.826763 | 1.559867  | 0.964609  | 1.816844  | 1.174252  |
