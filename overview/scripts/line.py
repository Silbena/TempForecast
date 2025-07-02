import pandas as pd
import plotly.express as px
import parsing as ps

def main():
    df = pd.read_csv('data/filtered.csv')

    df.drop(columns=['record_id', 'month'], inplace=True)
    
    df = df.groupby(['Country', 'year'], as_index=False).mean()

    fig = px.line(df,
                x='year',
                y='AverageTemperatureCelsius',
                color='Country',
                width = 2000,
                height = 1200)

    fig.update_layout(font=dict(size=36))

    args = ps.parse()

    if args.save == 0:
        fig.show()

    if args.save == 1:
        path = 'plots/line.png'
        fig.write_image(path)
        print(f'Plot saved under: {path}')


if __name__ == '__main__':
    main()
