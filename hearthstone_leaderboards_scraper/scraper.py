from pathlib import Path
from time import sleep
from typing import Any

import httpx
from loguru import logger
from stdl.fs import json_dump

from hearthstone_leaderboards_scraper.game_mode import GameMode
from hearthstone_leaderboards_scraper.region import Region


class LeaderboardsScraper:
    BASE_URL = "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData"

    def __init__(
        self,
        output_dir: str | None = None,
        delay: float = 1,
        user_agent: str | None = None,
        proxy: str | None = None,
        max_retries: int = 3,
    ) -> None:
        """
        Leaderboards scraper for Hearthstone.

        Args:
            output_dir (str, optional): The directory to save scraped data
            delay (float, optional): The delay between retries in seconds
            user_agent (str, optional): The User-Agent string to use for requests
            proxy (str, optional): The proxy URL to use for requests
            max_retries (int, optional): The maximum number of retries for failed requests
        """
        self.delay = delay
        self.user_agent = (
            user_agent
            or "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
        )
        self.client = httpx.Client(proxy=proxy)
        self.max_retries = max_retries
        self.output_dir = Path(output_dir) if output_dir is not None else Path.cwd() / "data"

    def get_params(
        self,
        game_mode: GameMode,
        region: Region,
        season_id: str,
        page: int,
    ) -> dict[str, str]:
        return {
            "region": region.value,
            "leaderboardId": game_mode.value,
            "seasonId": season_id,
            "page": str(page),
        }

    def scrape_page(
        self,
        game_mode: GameMode,
        region: Region,
        season_id: str,
        page: int,
    ) -> dict[str, Any]:
        params = self.get_params(game_mode, region, season_id, page)
        logger.info(f"[GET] {self.BASE_URL} | params={params}")

        for attempt in range(self.max_retries):
            try:
                response = self.client.get(
                    self.BASE_URL,
                    params=params,
                    headers={"User-Agent": self.user_agent},
                    timeout=30,
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:  # noqa: PERF203
                logger.exception(e)
                if attempt < self.max_retries - 1:
                    logger.info("Retrying ...")
                    sleep(self.delay)
                else:
                    logger.error("Max retries reached.")
                    raise
        raise RuntimeError("Max retries reached")

    def run(
        self,
        region: Region,
        game_mode: GameMode,
        season_id: str,
        num_pages: int | None = None,
        bg_min_rating: int = 0,
    ) -> None:
        """
        Scrape leaderboard data for specified game mode, region and season.

        Args:
            game_mode: Hearthstone game mode
            region: Leaderboards region
            season_id: Season ID
            num_pages: Maximum number of pages to scrape, scrapes all available pages by default
            bg_min_rating: Minimum player rating threshold for Battlegrounds modes. Once a player below this rating is found, scraping stops

        """
        if bg_min_rating and game_mode not in [GameMode.BATTLEGROUNDS, GameMode.BATTLEGROUNDS_DUO]:
            logger.warning("'bg_min_rating' is only applicable to Battlegrounds leaderboards")

        foldername = f"{game_mode.value}.{region.value}.{season_id}"
        output_dir = self.output_dir / foldername
        output_dir.mkdir(parents=True, exist_ok=True)

        data = self.scrape_page(game_mode, region, season_id, page=1)
        leaderboard_data = data["leaderboard"]["rows"]
        json_dump(leaderboard_data, output_dir / "00001.json")
        total_pages = data["leaderboard"]["pagination"]["totalPages"]
        logger.info(f"Total pages: {total_pages}")

        for page_number in range(2, total_pages + 1):
            filepath = output_dir / f"{page_number:05}.json"
            if filepath.exists():
                logger.info(f"'{filepath}' already exists")
                continue

            data = self.scrape_page(game_mode, region, season_id, page=page_number)
            json_dump(data["leaderboard"]["rows"], filepath)

            if num_pages and page_number >= num_pages:
                logger.info(f"Reached the limit of {num_pages} pages")
                return

            if game_mode in [GameMode.BATTLEGROUNDS, GameMode.BATTLEGROUNDS_DUO]:
                for player in data["leaderboard"]["rows"]:
                    if player["rating"] < bg_min_rating:
                        logger.info(f"Found rating below {bg_min_rating}. Stopping ...")
                        return

            sleep(self.delay)
