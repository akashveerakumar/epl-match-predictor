import requests
from pathlib import Path

BASE_URL = "https://www.football-data.co.uk/mmz4281/{code}/E0.csv"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

def season_code(start_year):
    first = start_year % 100
    second = (start_year + 1) % 100 
    return f"{first:02d}{second:02d}"

def season_url(start_year):
    return BASE_URL.format(code=season_code(start_year))

def download_season(start_year):
    path = RAW_DIR / f"E0_{season_code(start_year)}.csv"
    if path.exists():
        print(f"cached: {path.name}")
        return path
    
    # 1. fetch this season's URL, with a timeout
    response = requests.get(season_url(start_year), timeout = 30)
    # 2. crash if the status code is an error
    response.raise_for_status()
    # 3. save response.content to path (hint: path.write_bytes(...))
    path.write_bytes(response.content)

    print(f"downloaded: {path.name}")
    return path

if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for year in range(2014, 2026):
        download_season(year)