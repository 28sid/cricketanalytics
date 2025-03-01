import requests
from bs4 import BeautifulSoup
import json

# Base URL
TOURNAMENT_URL = "https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament"

def get_match_summary():
    response = requests.get(TOURNAMENT_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    match_summary = []
    all_rows = soup.select("table.engineTable > tbody > tr.data1") 
    for row in all_rows:
        tds = row.find_all("td")  
        
        if len(tds) >= 7:  
            match_summary.append({
                "team1": tds[0].text.strip(),
                "team2": tds[1].text.strip(),
                "winner": tds[2].text.strip(),
                "margin": tds[3].text.strip(),
                "ground": tds[4].text.strip(),
                "matchDate": tds[5].text.strip(),
                "scorecard": tds[6].text.strip()
            })

    return {"matchSummary": match_summary}

if __name__ == "__main__":
    match_data = get_match_summary()
    
    # Print or save data
    print(json.dumps(match_data, indent=4))
