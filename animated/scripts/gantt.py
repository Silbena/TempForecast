import pandas as pd
import plotly
import plotly.express as px

def main():

    df = pd.read_csv('data/gantt.csv', parse_dates=['start', 'stop'], dayfirst=True)
    fig = px.timeline(df, x_start='start', x_end= 'stop', y='activity')
    fig.update_yaxes(autorange='reversed')
    fig.write_image('gantt.pdf')
    # print('Done.')
    fig.show()

if __name__ == '__main__':
    main()
