import pandas as pd
from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests

def crawler(url, id_div, cnt):
    print(url, id_div)
    r1 = requests.get(url)
    soup1 = bs(r1.content, 'html.parser')
    table1 = soup1.find('div', {'id': id_div})
    comment1 = table1.find_all(string=lambda text: isinstance(text, Comment))
    data1 = bs(comment1[0], 'html.parser').find_all('tr')

    ans1 = dict()
    for i, g in enumerate(data1[1].find_all('th')):
        if i != 0:
            ans1[g.get('data-stat')] = []

    for i in range(2, len(data1)):
        tmp1 = data1[i].find_all('td')
        for j, x in enumerate(tmp1):
            if x.get('data-stat') in ans1.keys():
                if x.get('data-stat') == 'nationality':
                    s = x.getText().split(" ")
                    ans1[x.get('data-stat')].append(s[0])
                else:
                    ans1[x.get('data-stat')].append(x.getText())

    df1 = pd.DataFrame(ans1)
    if cnt == 2:
        df1.drop(['gk_games', 'gk_games_starts', 'gk_minutes', 'minutes_90s'], axis=1, inplace=True)
    df1.to_csv(f'table{cnt}.csv')

def clean_data():
    result = pd.read_csv('table1.csv')
    for x in range(3, 11):
        table = pd.read_csv(f"table{x}.csv")
        for x in table.columns:
            if x in result.columns:
                if x != 'Unnamed: 0':
                    table.drop(x, axis=1, inplace=True)
        result = pd.merge(result, table, on=['Unnamed: 0'], how='inner')

    merge = []
    table2 = pd.read_csv("table2.csv")
    for x in table2.columns:
        if x in result.columns:
            merge.append(x)
    merge.pop(0)

    result = pd.merge(result, table2, on=merge, how='left')
    result.drop(['Unnamed: 0_x', 'Unnamed: 0_y', 'minutes_90s', 'birth_year', 'matches'], axis=1, inplace=True)
    result['minutes'] = result['minutes'].apply(lambda x: int(''.join(x.split(','))))
    result = result[result['minutes'] > 90]
    result.sort_values(by=["player", 'age'], ascending=[True, False])
    result.to_csv('results.csv')

if _name_ == '_main_':
    url = 'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats'
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    table = soup.find('div', {'id': 'all_stats_standard'})
    comment = table.find_all(string=lambda text: isinstance(text, Comment))
    data = bs(comment[0], 'html.parser').find_all('tr')

    idx = [0, 6, 10, 11, 13, 16, 22, 36]
    ans = dict()
    for i, g in enumerate(data[1].find_all('th')):
        if i not in idx:
            ans[g.get('data-stat')] = []

    for i in range(2, len(data)):
        tmp = data[i].find_all('td')
        for j, x in enumerate(tmp):
            if x.get('data-stat') in ans.keys():
                if x.get('data-stat') == 'nationality':
                    s = x.getText().split(" ")
                    ans[x.get('data-stat')].append(s[0])
                else:
                    ans[x.get('data-stat')].append(x.getText())

    df = pd.DataFrame(ans)
    df.rename(columns={'goals_pens': 'non-Penalty Goals', 'pens_made': 'Penalty Goals'}, inplace=True)
    df.to_csv('table1.csv')

    urls = [
        'https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats'
    ]
    ids = ['all_stats_keeper', 'all_stats_shooting', 'all_stats_passing', 'all_stats_passing_types', 'all_stats_gca',
           'all_stats_defense', 'all_stats_possession', 'all_stats_playing_time',
           'all_stats_misc']

    for _, x in enumerate(zip(urls, ids)):
        crawler(x[0], x[1], _ + 2)
    clean_data()