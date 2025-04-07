import pandas as pd
import plotly.express as px
import parsing as ps

# Loading data and calculating average
df = pd.read_csv('data/filtered.csv')
date_str = df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
df['date'] = pd.to_datetime(date_str, format='%Y-%m-%d')
df.drop(columns=['record_id', 'Latitude', 'Longitude', 'month'], inplace= True)

countries = df['Country'].unique()

# Parsing options
args = ps.parse()

# Creating scatter plot for each country
for country in countries:
    country_df = df[df['Country'] == country]
    means = country_df.groupby('year', as_index = False).mean(numeric_only = True)

    trace = px.line(means, x = 'year', y = 'AverageTemperatureCelsius',
                    color_discrete_sequence = ['#FF7F0E'])

    fig = px.scatter(country_df, x = 'date', y = 'AverageTemperatureCelsius',
                     title = country,
                     width = 1400,
                     height = 700
                     ).add_trace(trace.data[0])
    
    fig.update_layout(font = dict(size = 30))
    fig.update_traces(marker = dict(opacity = 0.7))

    if args.save == 0:
        fig.show()
    if args.save == 1:
        path = f'plots/{country.lower()[:3]}.png'
        fig.write_image(path)
        print(f'Plot saved under: {path}')
