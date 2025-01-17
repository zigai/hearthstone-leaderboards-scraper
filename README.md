# Hearthstone leaderboards scraper

# Installation
```
pip install git+https://github.com/zigai/hearthstone-leaderboards-scraper.git
```

# Usage
```
usage: hs-leaderboards-scraper [-h] [-d] [-u] [-p] [-m] [-o] [-n] [-b] GAME-MODE REGION SEASON-ID

Scrapes leaderboard data for specified game mode, region and season.

positional arguments:
  GAME-MODE                             Hearthstone game mode [choices: BATTLEGROUNDS, BATTLEGROUNDS_DUO, STANDARD, WILD, ClASSIC, MERCEANARY, ARENA, TWIST] (*)
  REGION                                Leaderboards region [choices: EUROPE, AMERICAS, ASIA_PACIFIC] (*)
  SEASON-ID                             Season ID [type: str] (*)

options:
  -h, --help                            show this help message and exit
  -d, --delay                           The delay between retries in seconds [type: float, default=1]
  -u, --user-agent                      The User-Agent string to use for requests [type: str?]
  -p, --proxy                           The proxy URL to use for requests [type: str?]
  -m, --max-retries                     The maximum number of retries for failed requests [type: int, default=3]
  -o, --output-dir                      The directory to save scraped data [type: str?]
  -n, --num-pages                       Maximum number of pages to scrape, scrapes all available pages by default [type: int?]
  -b, --bg-min-rating                   Minimum player rating threshold for Battlegrounds modes. Once a player below this rating is found, scraping stops [type: int, default=0]
```
