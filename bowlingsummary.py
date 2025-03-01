import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.espncricinfo.com"
TOURNAMENT_URL = "https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament"

def get_match_links():
    response = requests.get(TOURNAMENT_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    links = []
    rows = soup.select("table.engineTable > tbody > tr.data1")
    
    for row in rows:
        match_link = row.select_one("td:nth-child(7) a")  # 7th column has the match link
        if match_link:
            links.append(BASE_URL + match_link["href"])
    
    return links

def get_match_data(match_url):
    response = requests.get(match_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    team_elements = soup.select("span > span > span")
    team1 = team_elements[0].text.replace(" Innings", "") if len(team_elements) > 1 else "Unknown Team"
    team2 = team_elements[1].text.replace(" Innings", "") if len(team_elements) > 2 else "Unknown Team"
    match_info = f"{team1} Vs {team2}"
    
    tables = soup.select("div > table.ds-table")

    bowling_summary = []
    
    if len(tables) > 1:
        first_inning_rows = tables[1].select("tbody > tr")
        for index, row in enumerate(first_inning_rows):
            cols = row.find_all("td")
            if len(cols) >= 11:
                bowling_summary.append({
                    "match": match_info,
                    "bowlingTeam": team2,
                    "bowlerName": cols[0].text.strip(),
                    "overs": cols[1].text.strip(),
                    "maiden": cols[2].text.strip(),
                    "runs": cols[3].text.strip(),
                    "wickets": cols[4].text.strip(),
                    "economy": cols[5].text.strip(),
                    "0s": cols[6].text.strip(),
                    "4s": cols[7].text.strip(),
                    "6s": cols[8].text.strip(),
                    "wides": cols[9].text.strip(),
                    "noBalls": cols[10].text.strip(),
                })
    
    if len(tables) > 3:
        second_inning_rows = tables[3].select("tbody > tr")
        for index, row in enumerate(second_inning_rows):
            cols = row.find_all("td")
            if len(cols) >= 11:
                bowling_summary.append({
                    "match": match_info,
                    "bowlingTeam": team1,
                    "bowlerName": cols[0].text.strip(),
                    "overs": cols[1].text.strip(),
                    "maiden": cols[2].text.strip(),
                    "runs": cols[3].text.strip(),
                    "wickets": cols[4].text.strip(),
                    "economy": cols[5].text.strip(),
                    "0s": cols[6].text.strip(),
                    "4s": cols[7].text.strip(),
                    "6s": cols[8].text.strip(),
                    "wides": cols[9].text.strip(),
                    "noBalls": cols[10].text.strip(),
                })
    
    return {"bowlingSummary": bowling_summary}

match_links = get_match_links()

all_match_data = []
for link in match_links[:5]:  # Limiting to 5 matches for testing
    print(f"Scraping: {link}")
    match_data = get_match_data(link)
    all_match_data.append(match_data)

import json
print(json.dumps(all_match_data, indent=4))
