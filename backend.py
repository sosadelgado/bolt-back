from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

app = FastAPI()

cache_data = None
cache_time = None
CACHE_TTL = timedelta(minutes=30)  # refresh every 30 min

def scrape_board():
    url = "https://www.hltv.org/matches"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "lxml")

    matches = []
    for match in soup.select(".upcomingMatch"):
        team_names = [t.get_text(strip=True) for t in match.select(".team")]
        time_info = match.select_one(".matchTime").get_text(strip=True) if match.select_one(".matchTime") else ""
        matches.append({
            "teams": team_names,
            "time": time_info
        })
    return matches

@app.get("/")
def root():
    return {"status": "Backend is live"}

@app.get("/board")
def get_board():
    global cache_data, cache_time
    if not cache_time or datetime.utcnow() - cache_time > CACHE_TTL:
        cache_data = scrape_board()
        cache_time = datetime.utcnow()
    return {"last_updated": cache_time, "matches": cache_data}
