import requests
import json

url = 'https://footballapi.pulselive.com/football/competitions/1/awards/20?altIds=true'

response = requests.get(
    f"https://footballapi.pulselive.com/football/stats/ranked/teams/wins?page=0&pageSize=20&compSeasons=362&comps=1&altIds=true",
    headers = {
        "origin": "https://www.premierleague.com"
    }
)

data = json.loads(response.text)
print(response.text)