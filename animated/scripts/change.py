import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import line_bar as lb
import time

def bar_data(df):

    years = range(1960, 2023)
    codes = df['Country Code']
    names = df['Country Name']
    populations = df.loc[:, '1960':'2022']
    y_lim = lb.max_pop(df)*1.2

    return  years, codes, names, populations, y_lim

def bar_style(title: str, y_limit: float) -> str:

    plt.title(title, fontsize = 24, pad = 20)
    plt.ylabel('population', fontsize = 18, labelpad = 15)
    year = plt.text(0.85, 0.95, '', transform=plt.gca().transAxes, fontsize = 24, verticalalignment = 'top')
    plt.ticklabel_format(axis = 'y', style = 'sci', useMathText = True)
    plt.gca().tick_params(axis = 'x', labelsize = 18, pad = 15)
    plt.tick_params(axis = 'y', labelsize = 18, pad = 20)
    plt.ylim(0, y_limit)

    return year

def bar_gif(df, title:str, file: str):

    years, codes, names, populations, y_lim = bar_data(df)
    fig = plt.figure(figsize = (10, 7))

    pause_len = 5
    year_index = 0
    line_h = 0

    def animate(i):
        plt.clf()

        nonlocal year_index, pause_len, line_h

        cur_year = years[year_index]

        year = bar_style(title, y_lim)
        year.set_text(str(cur_year))
        single_year = populations.iloc[:, year_index]
        bars = plt.bar(names, single_year, color = sns.color_palette('muted'))
        plt.bar_label(bars, codes, fontsize = 18)
        
        if cur_year == 1979 and pause_len >= 0:
            pause_len -= 1
            line_h = single_year.iloc[0]
        else:
            year_index += 1

        if cur_year >= 1979 and cur_year <= 1989:
            plt.axhline(y = line_h, color = 'black', linestyle = '--', lw = 3)
            plt.text(1.3, 14000000, 'WAR', fontdict={'fontsize': 24})
                    
    anim = FuncAnimation(fig, animate, frames=len(years) + pause_len, interval = 200)
    anim.save(f'plots/change/{file}.gif', dpi = 100)

def prep_data(df):
    incl = ['Afghanistan', 'Iraq', 'Uzbekistan', 'Iran']
    countries = df[df['Country Name'].isin(incl)]

    return countries

def main():

    lb.make_dir('plots/change')
    df = pd.read_csv('data/filtered.csv')
    war = prep_data(df)

    bar_gif(war, 'Soviet–Afghan War impact on Afghanistan', 'soviet_afghan')

if __name__ == "__main__":
    main()