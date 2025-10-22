"""fb_crawler package exposing browser, configuration, scraper, and storage utilities."""

from .browser import managed_browser, build_chrome_options
from .config import CrawlerConfig, ConfigError
from .scraper import FacebookScraper, Post, MetadataParseError
from .storage import JSONStorage, StorageError

__all__ = [
    "build_chrome_options",
    "managed_browser",
    "CrawlerConfig",
    "ConfigError",
    "FacebookScraper",
    "Post",
    "MetadataParseError",
    "JSONStorage",
    "StorageError",
]
