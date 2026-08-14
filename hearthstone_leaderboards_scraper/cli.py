from hearthstone_leaderboards_scraper.game_mode import GameMode
from hearthstone_leaderboards_scraper.region import Region
from hearthstone_leaderboards_scraper.scraper import LeaderboardsScraper


def scrape(
    region: Region,
    game_mode: GameMode,
    season_id: str,
    num_pages: int | None = None,
    bg_min_rating: int = 0,
    *,
    output_dir: str | None = None,
    delay: float = 1,
    user_agent: str | None = None,
    proxy: str | None = None,
    max_retries: int = 3,
) -> None:
    """Scrape Hearthstone leaderboard data."""
    scraper = LeaderboardsScraper(
        output_dir=output_dir,
        delay=delay,
        user_agent=user_agent,
        proxy=proxy,
        max_retries=max_retries,
    )
    scraper.run(
        region=region,
        game_mode=game_mode,
        season_id=season_id,
        num_pages=num_pages,
        bg_min_rating=bg_min_rating,
    )


def cli() -> None:
    from interfacy import Interfacy

    Interfacy(full_error_traceback=True).run(scrape)


if __name__ == "__main__":
    cli()
