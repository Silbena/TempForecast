import pandas as pd

def main():
    df = pd.read_csv('data/temperature.csv')

    # Remove rows with at least one missing value
    df.dropna(inplace = True)

    # Remove day column
    df.drop(columns = 'day', inplace = True)

    # Degrees conversion
    df['AverageTemperatureFahr'] = df['AverageTemperatureFahr'].apply(lambda x: (x - 32)*5/9).round(4)
    df['AverageTemperatureUncertaintyFahr'] = df['AverageTemperatureUncertaintyFahr'].apply(lambda x: (x - 32)*5/9).round(4)

    # Rename temperature columns
    col = {'AverageTemperatureFahr':'AverageTemperatureCelsius', 
        'AverageTemperatureUncertaintyFahr':'AverageTemperatureUncertaintyCelsius'}
    df.rename(columns= col, inplace = True)

    # Save filtered data
    df.to_csv('data/filtered.csv', index = False)

if __name__ == "__main__":
    main()