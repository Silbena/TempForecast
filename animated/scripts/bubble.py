import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import line_bar as lb

def density(country_code, populations):
    sizes = {'IND': 3287263, 'CHN': 9596961 , 'USA': 9525067, 'IDN': 1904569, 'PAK': 907132,
              'POL': 312696, 'VNM':331212, 'IRN': 1648195, 'TUR': 783562, 'DEU': 357114, 'THA': 513120,
              'UKR': 603500, 'MAR': 446550, 'SAU': 2149690, 'UZB': 447400}

    size = sizes[country_code]
    dens = populations/size

    return dens 

def bubble_data(df, biggest: bool):

    if biggest:
            picked = lb.pick_big(df, '2022')
    else: 
            picked = df

    years = range(1960, 2023)
    picked = picked.set_index('Country Code')
    picked = picked.loc[:, '1960':'2022']
    country_data = []
    countries = []
    populations = []
    densities = []

    for country, pops in picked.iterrows():
        countries.append(country)
        populations.append(pops)
        dens = density(country, pops)
        densities.append(dens)

    country_data.append(populations)
    country_data.append(densities)

    y_lim = lb.max_pop(picked)*1.3

    return years, countries, country_data, y_lim

def style_bubble(title: str, y_lim: float):

    plt.title(title, fontsize = 24, pad = 15)
    plt.ylabel('population', fontsize = 18, labelpad = 15)
    year = plt.text(0.85, 0.95, '', transform=plt.gca().transAxes, fontsize = 24, verticalalignment = 'top')
    plt.ticklabel_format(axis = 'y', style = 'sci', useMathText = True)
    plt.tick_params(axis = 'x', labelsize = 18, pad = 15)
    plt.tick_params(axis = 'y', labelsize = 18, pad = 15)
    plt.xlim(1960, 2022)
    plt.ylim(0, y_lim)

    return year

def bubble_gif(df, title:str, file: str, biggest:bool):

    x_data, countries, y_data, y_lim = bubble_data(df, biggest)
    fig = plt.figure(figsize=(10,7))
    plt.legend(countries, loc='upper left', title = 'Density', fontsize=14, title_fontsize = 14)
    
    def animate(i):
        plt.clf()
        year = style_bubble(title, y_lim) 
        year.set_text(str(x_data[i]))

        for c, single in enumerate(y_data[0]):
            plt.scatter(x_data[:i], single[:i], s = y_data[1][c][:i], color = sns.color_palette('muted')[c], alpha = 0.6)
         
        plt.legend(countries, loc='upper left', title = 'Density', fontsize=14, title_fontsize = 14)

    anim = FuncAnimation(fig, animate, frames=len(x_data), interval = 100)
    anim.save(f'plots/bubble/{file}.gif', dpi = 100)

def prep_data(df):
    ordered = df.sort_values(by = '2022', ascending = False, ignore_index = True)
    poland = ordered[ordered['Country Name'] == 'Poland'].index[0]
    poland_2022 = lb.pick_neighbors(ordered, poland)
    some_countries = lb.pick_neighbors(ordered, 17)

    return poland_2022, some_countries     

def main():

    lb.make_dir('plots/bubble')
    df = pd.read_csv('data/filtered.csv')
    poland_2022, some_countries = prep_data(df)

    bubble_gif(df, 'Most Populated countries', 'most_pop_b', True) 
    bubble_gif(some_countries,'Closely populated countries', 'random_b', False)
    bubble_gif(poland_2022,'Poland and closely populated countries', 'poland_b', False)

if __name__ == "__main__":
    main()
    