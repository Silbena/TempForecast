import pandas as pd
import plotly.express as px
import parsing as ps


def main():
    df = pd.read_csv('data/filtered.csv')

    fig = px.strip(df,
                x='Country',
                y='AverageTemperatureCelsius',
                stripmode='overlay',
                width=2000,
                height=1200)

    trace1 = px.box(df, x='Country', y='AverageTemperatureCelsius').data[0]
    fig.add_trace(trace1)

    fig.update_traces(jitter=1.0,
                      marker=dict(opacity = 0.2),
                      line=dict(color = 'black'),
                      fillcolor='rgba(0,0,0,0)')

    fig.update_layout(font=dict(size = 36))


    args = ps.parse()

    if args.save == 0:
        fig.show()

    if args.save == 1:
        path = 'plots/box2.png'
        fig.write_image(path)
        print(f'Plot saved under: {path}')


if __name__ == '__main__':
    main()
    