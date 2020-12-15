from bs4 import BeautifulSoup
import pandas as pd
import requests
import tqdm
import time
import lxml
import re


pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 255)


"""
If you need help with usage, you can message me (mitchy.#6281)
I might not respond because that's just how I am.
I may or may not update this if/when it gets broken by TRN.
I may or may not update this to be of a higher quality.
I may or may not add instructions to the README.
Licensing is more effort than this is worth. Anyone can use this for whatever.
I think that 'None' rows mean that that account hasn't been played on this season.
"""


def get_players_mmr(df):
    data = []
    for row in tqdm.tqdm(df.values):
        mmr_data = list(row) + list(parse_page(row))
        data.append(mmr_data)
    df = pd.DataFrame(data)
    df.columns = ['RSC ID', 'Player', 'TRN Link', '3v3 MMR', '3v3 GP', '2v2 MMR', '2v2 GP']
    df = df.drop([c for c in df.columns if 'Unranked' in c], axis=1)
    return df


def parse_page(row):
    link = row[2]
    name = row[1]
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'lxml')
    data_str = [l for l in [str(l.parent) for l in soup.find_all('script')] if 'INITIAL_STATE' in l][0]
    json_str = data_str.split('INITIAL_STATE')[1].replace('{}', 'null')
    standard_display = json_str.split('Ranked Standard')[1].split('displayValue')
    standard_mmr = standard_display[5].split('"')[2]
    standard_gp = standard_display[3].split('"')[2]
    doubles_display = json_str.split('Ranked Doubles')[1].split('displayValue')
    doubles_mmr = doubles_display[5].split('"')[2]
    doubles_gp = doubles_display[3].split('"')[2]
    return [standard_mmr, standard_gp, doubles_mmr, doubles_gp]


def run():
    start = time.time()
    csv_loc = 'players.csv'
    df = pd.read_csv('players.csv')
    df = df.head(10)
    print('Scraping MMRs')
    mmr_df = get_players_mmr(df).reset_index(drop=True)
    print('MMR Sheet')
    print(mmr_df)
    mmr_df.to_csv('mmr.csv')
    print(time.time() - start)


run()
