import pandas as pd


def main():
    df = pd.read_csv('data/temperature.csv')

    df.dropna(inplace=True)
    df.drop(columns='day', inplace=True)

    df['AverageTemperatureFahr'] = df['AverageTemperatureFahr'].apply(lambda x: (x - 32) * 5 / 9).round(4)

    df['AverageTemperatureUncertaintyFahr'] = df['AverageTemperatureUncertaintyFahr'].apply(lambda x: (x - 32) * 5 / 9).round(4)

    col = {'AverageTemperatureFahr':'AverageTemperatureCelsius', 
           'AverageTemperatureUncertaintyFahr':'AverageTemperatureUncertaintyCelsius'}
    df.rename(columns=col, inplace=True)

    df.to_csv('data/filtered.csv', index=False)


if __name__ == "__main__":
    main()
