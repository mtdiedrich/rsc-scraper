from bs4 import BeautifulSoup
import pandas as pd
import requests
import tqdm
import time

pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 255)


LINK = 'https://rocketleague.tracker.network/rocket-league/profile/steam/76561198415606823/overview'


def get_players_mmr(df):
    data = []
    for row in tqdm.tqdm(df.values):
        mmr_data = list(row) + list(parse_page(row))
        data.append(mmr_data)
    df = pd.DataFrame(data)
    df.columns = ['Player', 'TRN Link', 'Unranked MMR', 'Unranked GP',
            '1v1 MMR', '1v1 GP', '2v2 MMR', '2v2 GP', '3v3 MMR', '3v3 GP', 
            'Hoops MMR', 'Hoops GP', 'Rumble MMR', 'Rumble GP', 
            'Dropshot MMR', 'Dropshot GP', 'Snowday MMR', 'Snowday GP', 
            'Tournament MMR', 'Tournament GP']
    df = df.drop([c for c in df.columns if 'Unranked' in c], axis=1)
    return df


def get_display_value(string, value_name):
    use_name = '"' + value_name + '"'
    loc = string.find(use_name)
    value_str = string[loc:]
    value_loc = value_str.find('displayValue')
    value = value_str[value_loc:].split('":"')[1].split('","')[0]
    return value


def parse_page(row):
    link = row[1]
    name = row[0]
    page = requests.get(link)
    time.sleep(1)
    soup = BeautifulSoup(page.text, 'lxml')
    lines = [l.parent for l in soup.find_all('script')]
    data_str = [str(l) for l in lines if 'INITIAL_STATE' in str(l)][0]
    data_str = data_str.replace('"name"', '[player name]')
    json_str = data_str.split('INITIAL_STATE')[1].replace('{}', 'null')
    json_list = json_str.split('"type":"playlist"')[1:10]
    data = []
    for j in json_list:
        matches_played = get_display_value(j, 'matchesPlayed')
        rating = get_display_value(j, 'rating')
        data.append(rating)
        data.append(matches_played)
    return data


def run():
    #csv_loc = 'players.csv'
    #df = pd.read_csv(csv_loc)
    data = [['mitchy.' + str(i), LINK] for i in range(10)]
    df = pd.DataFrame(data) 
    mmr_df = get_players_mmr(df)
    print(mmr_df)


run()
