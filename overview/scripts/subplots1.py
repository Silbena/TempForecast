import pandas as pd
import plotly.express as px
import parsing as ps


def main():
    df = pd.read_csv('data/filtered.csv')

    df.drop(columns=['record_id', 'month'], inplace=True)

    df = df.groupby(['Country', 'year'], as_index=False).mean(numeric_only=True)

    fig = px.line(df,
                x='year',
                y='AverageTemperatureCelsius',
                color='Country',
                facet_col='Country',
                facet_col_wrap=4,
                width=2000,
                height=1400)

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(font=dict(size=36))

    args = ps.parse()

    if args.save == 0:
        fig.show()

    if args.save == 1:
        path = 'plots/subplots1.png'
        fig.write_image(path)
        print(f'Plot saved under: {path}')


if __name__ == '__main__':
    main()
