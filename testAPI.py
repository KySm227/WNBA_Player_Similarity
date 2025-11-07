import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import random
import math

User_Agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15',
]
headers = {
    'User-Agent': random.choice(User_Agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Conection': 'keep-alive',
}
def fetch_player_stats(player_name, url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    comment_soup = BeautifulSoup(''.join(comments), 'html.parser')

    # Initialize stats dictionary
    player_stats = {
        "name": player_name,
    }

    per_game_table = soup.find('table', {'id': ['per_game0', 'per_game1']})
    per_100_table = comment_soup.find('table', {'id': ['per_poss0', 'per_poss1']})
    advanced_table = soup.find('table', {'id': ['advanced0', 'advanced1']})
    shooting_table = comment_soup.find('table', {'id': ['shooting0', 'shooting1']})
    pbp_table = comment_soup.find('table', {'id': ['pbp0', 'pbp1']})
    # Extract Per Game Stats
    if per_game_table:
        df_per_game = pd.read_html(str(per_game_table))[0]
        for stats in df_per_game.to_dict('records'):
            if (stats['Year'] != 'Career') and ("season" not in str(stats['Year'])) and ("Did Not Play" not in str(stats.values())) and stats is not None:
                if not math.isnan(float(stats["Year"])):
                    del stats['Awards']
                    keys_to_delete = [k for k in stats if 'Unnamed' in k]
                    for key in keys_to_delete:
                        del stats[key]
                    for key, value in stats.items():
                        if ('nan' in key) or (isinstance(value, float) and math.isnan(value)):
                            stats[key] = 0.0
                    player_stats[str(stats["Age"])] = {}
                    player_stats[str(stats["Age"])]["per_game"] = stats
    # Extract Per 100 Possessions Stats
    if per_100_table:
        for comment in comments:
            comment_soup = BeautifulSoup(comment, 'html.parser')
            table = comment_soup.find('table', {'id': ['per_poss0', 'per_poss1']})
            if table:
                df_per_100 = pd.read_html(str(table))[0]
                break
        for stats in df_per_100.to_dict('records'):
            if stats['Year'] != 'Career' and ("season" not in str(stats['Year'])) and ("Did Not Play" not in str(stats.values())) and stats is not None:
                if not math.isnan(float(stats["Year"])):                
                    keys_to_delete = [k for k in stats if 'Unnamed' in k]
                    for key in keys_to_delete:
                        del stats[key]
                    for key, value in stats.items():
                        if ('nan' in key) or (isinstance(value, float) and math.isnan(value)):
                            stats[key] = 0.0
                    player_stats[str(stats["Age"])]["per_100_possessions"] = stats
    # Extract Advanced Stats
    if advanced_table:
        df_advanced = pd.read_html(str(advanced_table))[0]
        for stats in df_advanced.to_dict('records'):
            if stats['Year'] != 'Career' and ("season" not in str(stats['Year'])) and ("Did Not Play" not in str(stats.values())) and stats is not None:
                if not math.isnan(float(stats["Year"])):                
                    keys_to_delete = [k for k in stats if 'Unnamed' in k]
                    for key in keys_to_delete:
                        del stats[key]
                    for key, value in stats.items():
                        if ('nan' in key) or (isinstance(value, float) and math.isnan(value)):
                            stats[key] = 0.0
                    player_stats[str(stats["Age"])]["advanced"] = stats
    if shooting_table:
        for comment in comments:
            comment_soup = BeautifulSoup(comment, 'html.parser')
            table = comment_soup.find('table', {'id': ['shooting0', 'shooting1']})
            if table:
                df_shooting = pd.read_html(str(table))[0]
                break
        for stats in df_shooting.to_dict('records'):
            stats = {k[-1] if isinstance(k, tuple) else k: v for k, v in stats.items()}
            print(stats, "\n")
            if stats['Year'] != 'Career' and ("season" not in str(stats['Year'])) and ("Did Not Play" not in str(stats.values())) and stats is not None:
                if not math.isnan(float(stats["Year"])):                
                    keys_to_delete = [k for k in stats if 'Unnamed' in k]
                    for key in keys_to_delete:
                        del stats[key]
                    for key, value in stats.items():
                        if ('nan' in key) or (isinstance(value, float) and math.isnan(value)):
                            stats[key] = 0.0
                    player_stats[str(stats["Age"])]["shooting"] = stats
        if pbp_table:
            for comment in comments:
                comment_soup = BeautifulSoup(comment, 'html.parser')
                table = comment_soup.find('table', {'id': ['pbp0', 'pbp1']})
                if table:
                    df_pbp = pd.read_html(str(table))[0]
                    print(df_pbp.to_dict('records'))
                    break
            for stats in df_pbp.to_dict('records'):
                stats = {k[-1] if isinstance(k, tuple) else k: v for k, v in stats.items()}
                print(stats, "\n")
                if stats['Year'] != 'Career' and ("season" not in str(stats['Year'])) and ("Did Not Play" not in str(stats.values())) and stats is not None:
                    if not math.isnan(float(stats["Year"])):                
                        keys_to_delete = [k for k in stats if 'Unnamed' in k]
                        for key in keys_to_delete:
                            del stats[key]
                        for key, value in stats.items():
                            if ('nan' in key) or (isinstance(value, float) and math.isnan(value)):
                                stats[key] = 0.0
                        player_stats[str(stats["Age"])]["pbp"] = stats
    return player_stats

print(fetch_player_stats("A'ja Wilson", 'https://www.basketball-reference.com/wnba/players/w/wilsoa01w.html'))