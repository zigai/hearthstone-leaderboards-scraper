from hearthstone_leaderboards_scraper.scraper import LeaderboardsScraper

def cli():
    from interfacy_cli import Argparser
    Argparser(full_error_traceback=True).run(LeaderboardsScraper.run)

if __name__ == "__main__":
    cli()
