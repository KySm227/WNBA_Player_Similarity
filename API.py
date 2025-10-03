import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import time
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

def print_every_player_name():
    all_players = []
    player_links = {}  # New dictionary to store name -> href mapping 
    
    base_url = "https://www.basketball-reference.com"
    for letter in string.ascii_lowercase:
        base_link = base_url + "/wnba/players/" + letter + "/"
        page = requests.get(base_link, headers)
        soup = BeautifulSoup(page.text, "html.parser")
        all_player_names = soup.select('div.index[role="main"]#content p a')[:-1]
        
        # Extract names and add to list
        all_players.extend([p.get_text() for p in all_player_names])
        
        # Extract names and hrefs, add to dictionary with full URL
        for p in all_player_names:
            player_name = p.get_text()
            player_href = p.get('href')
            # Construct full URL
            full_url = base_url + player_href if player_href else None
            player_links[player_name] = full_url
        time.sleep(2)  # Be polite and avoid overwhelming the server
    return player_links

def stats(name, age):
    # Get player URL
    url = print_every_player_name().get(name)
    
    if not url:
        return {"error": f"Player '{name}' not found"}

    response = requests.get(url, headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find tables by their IDs
    per_game_table = soup.find('table', {'id': 'per_game0'})
    per_100_table = soup.find('table', {'id': 'per_poss0'})
    advanced_table = soup.find('table', {'id': 'advanced0'})

    # Initialize stats dictionary
    player_stats = {
        "name": name,
        "url": url,
        "age": age,
        "per_game": None,
        "per_100_possessions": None,
        "advanced": None
    }

    # Helper: filter by age if column exists
    def filter_by_age(df, age):
        for col in df.columns:
            if 'Age' in col:
                df = df[df[col] == int(age)]
                break
        return df

    # Extract Per Game Stats
    if per_game_table:
        df_per_game = pd.read_html(str(per_game_table))[0]
        player_stats["per_game"] = filter_by_age(df_per_game, age).to_dict('records')
        del player_stats["per_game"][-1]['Awards']  # Remove awards columns
        keys_to_delete = [k for k in player_stats["per_game"][-1] if 'Unnamed' in k]
        for key in keys_to_delete:
            del player_stats["per_game"][-1][key]
        player_stats["per_game"] = {k: float(v) if k != 'Tm' else v for k, v in player_stats["per_game"][-1].items()}
        
    # Remove awards columns

    # Extract Per 100 Possessions Stats
    if per_100_table:
        df_per_100 = pd.read_html(str(per_100_table))[0]
        player_stats["per_100_possessions"] = filter_by_age(df_per_100, age).to_dict('records')
    
    # Extract Advanced Stats
    if advanced_table:
        df_advanced = pd.read_html(str(advanced_table))[0]
        player_stats["advanced"] = filter_by_age(df_advanced, age).to_dict('records')
        keys_to_delete = [k for k in player_stats["advanced"][-1] if 'Unnamed' in k]
        for key in keys_to_delete:
            del player_stats["advanced"][-1][key]
        player_stats["advanced"] = {k: float(v) if k != 'Tm' else v for k, v in player_stats["advanced"][-1].items()}

    # Remove the last dictionary because its career stats
    print(player_stats)
    return player_stats


def compare(name1, name2, age):
    player1 = stats(name1, age)
    player2 = stats(name2, age)

    if "error" in player1 or "error" in player2:
        return {"error": "One or both players not found"}
    # Convert stats to DataFrames
    keys = ['per_game', 'advanced']

    # 2. Convert dicts to vectors
    vec1 = np.array([player1[k][key] if key != 'Tm' else 0 for k in keys for key in player1[k]]).reshape(1, -1)
    vec2 = np.array([player2[k][key] if key != 'Tm' else 0 for k in keys for key in player2[k]]).reshape(1, -1)

    # 3. Compute cosine similarity
    similarity = cosine_similarity(vec1, vec2)
    similarity = similarity[0][0]  # Extract the scalar value from the 2D array
    return {
        "player1": player1["name"],
        "player2": player2["name"],
        "similarity_score": float(similarity),
    }

# Example usage:
print(compare("A'ja Wilson", "Breanna Stewart", "25"))