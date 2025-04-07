import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib.animation import PillowWriter
import seaborn as sns
from matplotlib.animation import FuncAnimation

# make plots dir
def make_dir(name):
    if os.path.exists(f'./{name}'):
        shutil.rmtree(f'./{name}')

    os.mkdir(f'./{name}')

# pick 5 most populated countries
def pick_big(dataframe, year: str):
    ordered = dataframe.sort_values(by = year, ascending = False)
    biggest = ordered.head(5)

    return biggest

# pick 4 neighbors
def pick_neighbors(dataframe, country) -> list:

    countries = dataframe.loc[country - 2 : country + 2]

    return countries

# pick random country and 4 neighbors from random year
def pick_random(dataframe) -> list:

    year = str(random.randrange(1960, 2023))
    ordered = dataframe.sort_values(by = year, ascending = False, ignore_index = True)

    country = ordered.sample(n = 1).index[0]
    names = pick_neighbors(ordered, country)

    return names

# pick Poland and 4 neighbors from random year
def pick_poland(dataframe) -> list:

    year = str(random.randrange(1960, 2023))
    ordered = dataframe.sort_values(by = year, ascending = False, ignore_index = True)

    poland = ordered[ordered['Country Name'] == 'Poland'].index[0]
    names = pick_neighbors(ordered, poland)

    return names

# maximum populatio in dataframe
def max_pop(dataframe) -> int:
   
   year_cols = dataframe.loc[:, '1960':'2022']
   country_max = year_cols.max(axis = 1)
   overall_max = country_max.max()

   return overall_max

def bar_data(dataframe, year: str):

    codes = dataframe['Country Code']
    names = dataframe['Country Name']
    populations = dataframe[year]

    return codes, names, populations


def assign_colors(dataframe) -> dict:
    
    color_map = sns.color_palette('muted')
    colors = {}
    ordered = dataframe.sort_values(by = '2022', ascending = False)

    for i, country in enumerate(ordered['Country Name'].tolist()):
        colors[country] = color_map[i % 10]

    return colors

def assign_hatches(dataframe) -> dict:

    hatch_types = ['x', 'o', '/', '*', '\\', '.', '|', 'O', '-',  '+']
    hatches = {}
    ordered = dataframe.sort_values(by = '2022', ascending = False)

    for i, country in enumerate(ordered['Country Name'].tolist()):
        hatches[country] = hatch_types[i % 10]

    return hatches

def bar_plot(x, y, code, year: str, title: str, patterns: dict, y_limit: float) -> str:

        if type(list(patterns.values())[0]) == tuple:
            cols = [patterns[key] for key in x]
            bars = plt.bar(x, y, color = cols)

        else:
            shapes = [patterns[key] for key in x]
            bars = plt.bar(x, y, color = 'white', edgecolor = 'black' , hatch = shapes)

        plt.title(title, fontsize = 24, pad = 20)
        plt.ylabel('population', fontsize = 18, labelpad = 15)
        plt.ylim(0, y_limit)
        plt.bar_label(bars, code, fontsize = 18)
        plt.text(0.85, 0.95, year, transform=plt.gca().transAxes, fontsize = 24, verticalalignment = 'top')

        multiline = [label.replace(' ', '\n') for label in x]
        plt.xticks(x, multiline, va = 'center')
        plt.ticklabel_format(axis = 'y', style = 'sci', useMathText = True)
        plt.tick_params(axis = 'x', labelsize = 18, pad = 40)
        plt.tick_params(axis = 'y', labelsize = 18, pad = 20)

        plt.tight_layout()

def bar_gif(dataframe, title:str, file: str, biggest:bool, color: bool):

    if color:
        patterns = assign_colors(dataframe)
    else:
        patterns = assign_hatches(dataframe)

    y_limit = max_pop(dataframe)*1.2
    writer = PillowWriter(fps = 10)
    fig = plt.figure(figsize = (10, 7))

    with writer.saving(fig, f'plots/bar/{file}.gif', 100):

        for year in range(1960, 2023):
            year = str(year)

            if biggest:
                countries = pick_big(dataframe, year)
            else: 
                countries = dataframe

            codes, names, populations = bar_data(countries, year)
            bar_plot(names, populations, codes, year, title, patterns, y_limit)
            writer.grab_frame()
            plt.clf()

    plt.close()

def line_data(df, biggest: bool):

    if biggest:
            picked = pick_big(df, '2022')
    else: 
            picked = df

    years = range(1960, 2023)
    picked = picked.set_index('Country Code')
    picked = picked.loc[:, '1960':'2022']
    countries = []
    country_data = []

    for country, populations in picked.iterrows():
         countries.append(country)
         country_data.append(populations)

    y_lim = max_pop(picked)*1.2
    
    return years, countries, country_data, y_lim

def style_line(title: str, y_lim: float):

    plt.title(title, fontsize = 24, pad = 15)
    plt.ylabel('population', fontsize = 18, labelpad = 15)
    year = plt.text(0.85, 0.95, '', transform=plt.gca().transAxes, fontsize = 24, verticalalignment = 'top')
    plt.ticklabel_format(axis = 'y', style = 'sci', useMathText = True)
    plt.tick_params(axis = 'x', labelsize = 18, pad = 15)
    plt.tick_params(axis = 'y', labelsize = 18, pad = 15)
    plt.xlim(1960, 2022)
    plt.ylim(0, y_lim)

    return year

def line_gif(df, title:str, file: str, biggest:bool):

    x_data, countries, y_data, y_lim = line_data(df, biggest)
    fig = plt.figure(figsize=(10,7))
    
    def animate(i):
        plt.clf()
        year = style_line(title, y_lim) 

        for s, single in enumerate(y_data):
            plt.plot(x_data[:i], single[:i], color = sns.color_palette('muted')[s])
         
        year.set_text(str(x_data[i]))
        plt.legend(countries, loc='upper left', fontsize=14)

    anim = FuncAnimation(fig, animate, frames=len(x_data), interval = 100)
    anim.save(f'plots/line/{file}.gif', dpi = 100)

def main():

    make_dir('plots/bar')
    make_dir('plots/line')
    df = pd.read_csv('data/filtered.csv')
    random_countries = pick_random(df)
    poland_plus = pick_poland(df)

    bar_gif(df, 'Most populated countries', 'most_pop_c', True, True)
    bar_gif(df, 'Most populated countries', 'most_pop_bw', True, False)
    bar_gif(random_countries, 'Closely populated countries', 'random_c', False, True)
    bar_gif(random_countries, 'Closely populated countries', 'random_bw', False, False)
    bar_gif(poland_plus, 'Poland and closely populated countries','poland_c', False, True)
    bar_gif(poland_plus, 'Poland and closely populated countries', 'poland_bw', False, False)

    line_gif(df, 'Most Populated countries', 'most_pop_l', True) 
    line_gif(random_countries,'Closely populated countries', 'random_l', False)
    line_gif(poland_plus,'Poland and closely populated countries', 'poland_l', False)  

if __name__ == "__main__":
    main()
