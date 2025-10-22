"""Command line entry point for the Facebook crawler."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from fb_crawler.browser import managed_browser
from fb_crawler.config import CrawlerConfig, ConfigError
from fb_crawler.scraper import FacebookScraper
from fb_crawler.storage import JSONStorage


DEFAULT_CONFIG = Path("mvars")
DEFAULT_OUTPUT = Path("scraped_posts.json")


def run_crawler(config_path: Path = DEFAULT_CONFIG, output_path: Path = DEFAULT_OUTPUT) -> Sequence[dict]:
    """Execute the scraping pipeline and return the collected posts."""
    config = CrawlerConfig.load(config_path)
    with managed_browser(config) as driver:
        scraper = FacebookScraper(driver)
        scraper.load_feed(config.url)
        posts = scraper.scrape_posts()

    storage = JSONStorage(output_path)
    storage.save_posts(posts)
    return [asdict(post) for post in posts]


def main() -> None:
    try:
        run_crawler()
    except ConfigError as exc:
        raise SystemExit(f"Configuration error: {exc}") from exc


if __name__ == "__main__":
    main()
