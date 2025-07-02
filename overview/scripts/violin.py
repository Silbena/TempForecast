import pandas as pd
import plotly.express as px
import parsing as ps


def main():
    df = pd.read_csv('data/filtered.csv')

    fig = px.violin(df,
                    x='Country',
                    y='AverageTemperatureCelsius',
                    width=2000,
                    height=1200)

    fig.update_layout(font = dict(size = 36))

    args = ps.parse()

    if args.save == 0:
        fig.show()

    if args.save == 1:
        path = 'plots/violin.png'
        fig.write_image(path)
        print(f'Plot saved under: {path}')


if __name__ == '__main__':
    main()
