"""Browser management for Selenium WebDriver."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from .config import CrawlerConfig


def build_chrome_options(config: CrawlerConfig) -> Options:
    """Create Chrome options based on crawler configuration."""
    options = Options()
    options.add_argument(config.chrome_profile_dir)
    options.add_argument(f"--profile-directory={config.profile_directory}")
    if config.headless:
        # The "new" headless mode is available on recent Chrome versions. Fallback
        # to the legacy flag if necessary.
        options.add_argument("--headless=new")
    return options


@contextmanager
def managed_browser(config: CrawlerConfig) -> Iterator[Chrome]:
    """Context manager yielding a configured Chrome WebDriver instance."""
    options = build_chrome_options(config)
    driver = Chrome(options=options)
    try:
        yield driver
    finally:
        driver.quit()


__all__ = ["build_chrome_options", "managed_browser"]
