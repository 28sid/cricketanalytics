import requests
from bs4 import BeautifulSoup
import json

# Base URL
BASE_URL = "https://www.espncricinfo.com"
TOURNAMENT_URL = "https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament"

### ---- STEP 1: GET MATCH LINKS ---- ###
def get_match_links():
    response = requests.get(TOURNAMENT_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    match_links = []
    rows = soup.select("table.engineTable > tbody > tr.data1")
    
    for row in rows:
        match_link = row.select_one("td:nth-child(7) a")  # 7th column has the match link
        if match_link:
            match_links.append(BASE_URL + match_link["href"])
    
    return match_links

def get_players_from_match(match_url):
    response = requests.get(match_url)
    soup = BeautifulSoup(response.text, "html.parser")

    team_elements = soup.select("span > span > span")
    team1 = team_elements[0].text.replace(" Innings", "") if len(team_elements) > 1 else "Unknown Team"
    team2 = team_elements[1].text.replace(" Innings", "") if len(team_elements) > 2 else "Unknown Team"

    players_links = []

    tables = soup.select("div > table.ci-scorecard-table")

    if tables:
        first_inning_rows = tables[0].select("tbody > tr")
        for row in first_inning_rows:
            cols = row.find_all("td")
            if len(cols) >= 8:
                player_link = cols[0].find("a")
                if player_link:
                    players_links.append({
                        "name": cols[0].text.strip(),
                        "team": team1,
                        "link": BASE_URL + player_link["href"]
                    })

        second_inning_rows = tables[1].select("tbody > tr")
        for row in second_inning_rows:
            cols = row.find_all("td")
            if len(cols) >= 8:
                player_link = cols[0].find("a")
                if player_link:
                    players_links.append({
                        "name": cols[0].text.strip(),
                        "team": team2,
                        "link": BASE_URL + player_link["href"]
                    })

    tables = soup.select("div > table.ds-table")

    if len(tables) > 1:
        first_inning_rows = tables[1].select("tbody > tr")
        for row in first_inning_rows:
            cols = row.find_all("td")
            if len(cols) >= 11:
                player_link = cols[0].find("a")
                if player_link:
                    players_links.append({
                        "name": cols[0].text.strip(),
                        "team": team2,
                        "link": BASE_URL + player_link["href"]
                    })

    if len(tables) > 3:
        second_inning_rows = tables[3].select("tbody > tr")
        for row in second_inning_rows:
            cols = row.find_all("td")
            if len(cols) >= 11:
                player_link = cols[0].find("a")
                if player_link:
                    players_links.append({
                        "name": cols[0].text.strip(),
                        "team": team1,
                        "link": BASE_URL + player_link["href"]
                    })

    return players_links


def get_player_details(player):
    response = requests.get(player["link"])
    soup = BeautifulSoup(response.text, "html.parser")

    def extract_info(label):
        section = soup.select_one(f"div.ds-grid > div:has(p:contains('{label}'))")
        return section.select_one("span").text.strip() if section else "Not Available"

    player_info = {
        "name": player["name"],
        "team": player["team"],
        "battingStyle": extract_info("Batting Style"),
        "bowlingStyle": extract_info("Bowling Style"),
        "playingRole": extract_info("Playing Role"),
        "description": soup.select_one("div.ci-player-bio-content p").text.strip() if soup.select_one("div.ci-player-bio-content p") else "No description available"
    }
    
    return player_info


if __name__ == "__main__":
    match_links = get_match_links()
    
    all_players = []
    for match in match_links[:3]:  # Limit to first 3 matches 
        print(f"Scraping match: {match}")
        players = get_players_from_match(match)
        all_players.extend(players)

    final_data = []
    for player in all_players[:5]:  # Limit to first 5 
        print(f"Scraping player: {player['name']}")
        player_details = get_player_details(player)
        final_data.append(player_details)


    print(json.dumps(final_data, indent=4))
