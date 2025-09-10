import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import unicodedata
import string

def clean_name(name1):
    name1 = unicodedata.normalize('NFKD', name1).encode('ASCII', 'ignore').decode()
    name1 = name1.lower().strip()

    parts = name1.split()
    if len(parts) == 2:
        first, last = parts 
        print(first + " " + last)
        return first, last

def get_url(name2):
    first, last = clean_name(name2)
    base = "https://www.basketball-reference.com/wnba/players/"
    for i in range(1, 3):
        suffix = f"{i:02d}w"
        player_link = f"{base}{last[0]}/{last[:5]}{first[:2]}{suffix}.html"  
        player_link = re.sub(r"[']", "", player_link)
        r = requests.get(player_link)
        if r.status_code == 200:
            print(player_link)
            return player_link 

def print_every_player_name(name, year):
    all_players = []
    all_p_stats = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    }  
    for letter in string.ascii_lowercase:
        base_link = "https://www.basketball-reference.com/wnba/players/" + letter + "/"
        page = requests.get(base_link, headers)
        soup = BeautifulSoup(page.text, "html.parser")
        all_player_names = soup.select('div.index[role="main"]#content p a')[:-1]
        all_players.extend([p.get_text() for p in all_player_names])
    url = get_url(name)
    page2 = requests.get(url, headers)

    soup2 = BeautifulSoup(page2.text, "html.parser")

    all_players_stats = soup2.find_all(id=f'per_game0.{year}', class_='full_table')
    all_advanced_stats = soup2.find('div', id='div_advanced0')
    all_advanced = all_advanced_stats.find('tr', id=f'advanced0.{year}')
    ts = all_advanced.find('td', attrs={'data-stat' : 'ts_pct'}, class_= 'right')
    
    for player in all_players_stats:
        labels = ["Team", "Age", "Games Played", "Games Started", "Minutes", "Field Goals Made", "Field Goals Attempted" , "Field Goal Percentage", "3 Points Made" , "3 Points Attempted", "3 Point Percentage", "2 Points Made", "2 Points Attempted", "2 Points Percentage", "Effective Field Goal", "Free Throws Made", "Free Throws Attempted", "Free Throw Percentage", "Offensive Rebounds", "Defensive Rebounds", "Total Rebounds", "Assists", "Steals", "Blocks", "Turnovers", "Personal Fouls", "Points"]
        numbers = []
        

        stats = player.find_all(class_='right')

        for stat in stats:
            numbers.append(stat.text)
        player_stats = dict(zip(labels,numbers))
    all_p_stats[name] = player_stats
    print(all_p_stats[name])
    print(ts.text)
name_input = input("Enter a WNBA player: ")
year_input = input("Enter a year: ")
print_every_player_name(name_input, year_input)


"""
Similarity Score: eFG%, TS%, 3PAr, FTr, ORB%, DRB%, AST%, STL%, BLK%, TOV%, USG, 2P%, 3P%, 2PA, DRtg, ORtg, OWS, DWS, WS, PER

BPM = RawBPM + Tm Adj.
Tm. Adj =
RawBPM = 
VORP = (BPM - (-2.0)) x (MP/TeMP) 



"""