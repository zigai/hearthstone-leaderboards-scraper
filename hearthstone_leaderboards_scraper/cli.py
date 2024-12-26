from hearthstone_leaderboards_scraper.scraper import LeaderboardsScraper


def cli():
    from interfacy_cli import Argparser

    Argparser().run(LeaderboardsScraper.run)
