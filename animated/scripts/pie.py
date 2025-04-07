import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import line_bar as lb

def pie_data(df, biggest: bool):

    if biggest:
            picked = lb.pick_big(df, '2022')
    else: 
            picked = df

    years = range(1960, 2023)
    picked = picked.set_index('Country Code')
    picked = picked.loc[:, '1960':'2022']
    country_data = []
    countries = []

    for country, pops in picked.iterrows():
        countries.append(country)
        country_data.append(pops)

    return picked, years, countries, country_data

def style_pie(title: str):

    plt.title(title, fontsize = 24, pad = 20)
    year = plt.text(1, 0.87, '', transform=plt.gca().transAxes, fontsize = 24, verticalalignment = 'top')

    return year

def pie_gif(df, title:str, file: str, biggest:bool):

    picked, x_data, countries = pie_data(df, biggest)
    fig = plt.figure(figsize=(10,7))
    
    def animate(i):
        plt.clf()
        year = style_pie(title) 
        single_year = picked.iloc[:, i]
        labels = round(single_year/1000000)
        textprops = {'fontsize':14}
        plt.pie(single_year, labels = labels, colors = sns.color_palette('muted'), textprops = textprops)
        year.set_text(str(x_data[i]))
        plt.legend(countries, title = 'Populations [mln]',
                   bbox_to_anchor=(0, 0.9), fontsize=14, title_fontsize = 14)

    anim = FuncAnimation(fig, animate, frames=len(x_data), interval = 200)
    anim.save(f'plots/pie/{file}.gif', dpi = 100)

def prep_data(df):
    ordered = df.sort_values(by = '2022', ascending = False, ignore_index = True)
    poland = ordered[ordered['Country Name'] == 'Poland'].index[0]
    poland_2022 = lb.pick_neighbors(ordered, poland)
    some_countries = lb.pick_neighbors(ordered, 17)

    return poland_2022, some_countries     

def main():

    lb.make_dir('plots/pie')
    df = pd.read_csv('data/filtered.csv')
    poland_2022, some_countries = prep_data(df)

    pie_gif(df, 'Most populated countries', 'most_pop_p', True) 
    pie_gif(some_countries,'Closely populated countries', 'random_p', False)
    pie_gif(poland_2022,'Poland and closely populated countries', 'poland_p', False)

if __name__ == "__main__":
    main()
    