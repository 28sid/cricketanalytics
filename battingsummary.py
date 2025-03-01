import requests
from bs4 import BeautifulSoup

# Step 1: Get match summary links
BASE_URL = "https://stats.espncricinfo.com"
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

# Step 2: Scrape match details & batting summary
def get_match_data(match_url):
    response = requests.get(match_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extracting team names
    team_elements = soup.select("span > span > span")
    team1 = team_elements[0].text.replace(" Innings", "") if len(team_elements) > 1 else "Unknown Team"
    team2 = team_elements[1].text.replace(" Innings", "") if len(team_elements) > 2 else "Unknown Team"
    match_info = f"{team1} Vs {team2}"
    
    tables = soup.select("div > table.ci-scorecard-table")
    
    batting_summary = []
    
    # Extract First Innings Batting Data
    if tables:
        first_inning_rows = tables[0].select("tbody > tr")
        for index, row in enumerate(first_inning_rows):
            cols = row.find_all("td")
            if len(cols) >= 8:
                batting_summary.append({
                    "match": match_info,
                    "teamInnings": team1,
                    "battingPos": index + 1,
                    "batsmanName": cols[0].text.strip(),
                    "dismissal": cols[1].text.strip(),
                    "runs": cols[2].text.strip(),
                    "balls": cols[3].text.strip(),
                    "4s": cols[5].text.strip(),
                    "6s": cols[6].text.strip(),
                    "SR": cols[7].text.strip(),
                })
    
    # Extract Second Innings Batting Data
    if len(tables) > 1:
        second_inning_rows = tables[1].select("tbody > tr")
        for index, row in enumerate(second_inning_rows):
            cols = row.find_all("td")
            if len(cols) >= 8:
                batting_summary.append({
                    "match": match_info,
                    "teamInnings": team2,
                    "battingPos": index + 1,
                    "batsmanName": cols[0].text.strip(),
                    "dismissal": cols[1].text.strip(),
                    "runs": cols[2].text.strip(),
                    "balls": cols[3].text.strip(),
                    "4s": cols[5].text.strip(),
                    "6s": cols[6].text.strip(),
                    "SR": cols[7].text.strip(),
                })
    
    return {"battingSummary": batting_summary}

# Run the scraper
match_links = get_match_links()

all_match_data = []
for link in match_links[:5]:  # Limiting to 5 matches for testing
    print(f"Scraping: {link}")
    match_data = get_match_data(link)
    all_match_data.append(match_data)

# Print or save data
import json
print(json.dumps(all_match_data, indent=4))
