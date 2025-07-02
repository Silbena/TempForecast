import pandas as pd

import arima_yearly_jap
import arima_yearly_swe

import hwes_seasonal_jap
import hwes_seasonal_swe

import prophet_seasonal_jap
import prophet_seasonal_swe
import prophet_yearly_jap
import prophet_yearly_swe

import sarima_seasonal_jap
import sarima_seasonal_swe
import sarima_yearly_jap
import sarima_yearly_swe


def cross_validate():
    mean_errors = [['' , 'arima_y', 'hwes_s', 'prophet_s', 'prophet_y', 'sarima_s', 'sarima_y'],
                ['jap'],
                ['swe']]

    _, _, _, mean_error = arima_yearly_jap.calculations('Japan')
    mean_errors[1].append(mean_error)

    _, _, _, mean_error = hwes_seasonal_jap.calculations('Japan')
    mean_errors[1].append(mean_error)

    _, _, mean_error = prophet_seasonal_jap.calculations('Japan')
    mean_errors[1].append(mean_error)

    _, _, mean_error = prophet_yearly_jap.calculations('Japan')
    mean_errors[1].append(mean_error)

    _, _, _, mean_error = sarima_seasonal_jap.calculations('Japan')
    mean_errors[1].append(mean_error)

    _, _, _, mean_error = sarima_yearly_jap.calculations('Japan')
    mean_errors[1].append(mean_error)


    _, _, _, mean_error = arima_yearly_swe.calculations('Sweden')
    mean_errors[2].append(mean_error)

    _, _, _, mean_error = hwes_seasonal_swe.calculations('Sweden')
    mean_errors[2].append(mean_error)

    _, _, mean_error = prophet_seasonal_swe.calculations('Sweden')
    mean_errors[2].append(mean_error)

    _, _, mean_error = prophet_yearly_swe.calculations('Sweden')
    mean_errors[2].append(mean_error)

    _, _, _, mean_error = sarima_seasonal_swe.calculations('Sweden')
    mean_errors[2].append(mean_error)

    _, _, _, mean_error = sarima_yearly_swe.calculations('Sweden')
    mean_errors[2].append(mean_error)

    return mean_errors


def make_table(mean_errors):
    df = pd.DataFrame(mean_errors[1:], columns=mean_errors[0])
    html_table = df.to_html(index=False)

    print(df)

    with open('plots/error_table.html', 'w') as f:
        f.write(html_table)


def main():
    mean_errors = cross_validate()
    make_table(mean_errors)


if __name__ == '__main__':
    main()
