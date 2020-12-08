from bs4 import BeautifulSoup
import pandas as pd
import requests
import tqdm
import time


pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 255)


"""
If you need help with usage, you can message me (mitchy.#6281)
I might not respond because that's just how I am.
I may or may not update this if/when it gets broken by TRN.
I may or may not update this to be of a higher quality.
I may or may nut add instructions to the README.
Licensing is more effort than this is worth. Anyone can use this for whatever.
I think that 'None' rows mean that that account hasn't been played on this season.
"""


def get_players_mmr(df):
    data = []
    errors = []
    for row in tqdm.tqdm(df.values):
        try:
            mmr_data = list(row) + list(parse_page(row))
        except:
            mmr_data = list(row) + [None for e in range(18)]
            errors.append(row)
        data.append(mmr_data)
    df = pd.DataFrame(data)
    df.columns = ['RSC ID', 'Player', 'TRN Link', 'Unranked MMR', 
            'Unranked GP', '1v1 MMR', '1v1 GP', '2v2 MMR', '2v2 GP', 
            '3v3 MMR', '3v3 GP', 'Hoops MMR', 'Hoops GP', 'Rumble MMR',
            'Rumble GP', 'Dropshot MMR', 'Dropshot GP', 'Snowday MMR',
            'Snowday GP', 'Tournament MMR', 'Tournament GP']
    df = df.drop([c for c in df.columns if 'Unranked' in c], axis=1)
    errors_df = pd.DataFrame(errors)
    errors_df.to_csv('errors.csv')
    print('ERRORS BELOW')
    print(errors_df)
    print()
    return df


def get_display_value(string, value_name):
    use_name = '"' + value_name + '"'
    loc = string.find(use_name)
    value_str = string[loc:]
    value_loc = value_str.find('displayValue')
    value = value_str[value_loc:]
    value = value.split('":"')[1].split('","')[0]
    return value


def parse_page(row):
    link = row[2]
    name = row[1]
    page = requests.get(link)
    time.sleep(1)
    soup = BeautifulSoup(page.text, 'lxml')
    lines = [l.parent for l in soup.find_all('script')]
    data_str = [str(l) for l in lines if 'INITIAL_STATE' in str(l)][0]
    data_str = data_str.replace(name, '[player name]')
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
    csv_loc = 'players.csv'
    df = pd.read_csv(csv_loc, header=None)
    cols = df.columns
    if len(cols) == 2:
        df['RSC ID'] = None
        df = df[['RSC ID'] + list(cols)] 
    mmr_df = get_players_mmr(df).dropna().reset_index(drop=True)
    print('MMR Sheet')
    print(mmr_df)
    df.to_csv('mmr.csv')


run()
