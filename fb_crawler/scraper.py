"""Scraping logic for Facebook posts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence
import json
import sys
from html.parser import HTMLParser

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:  # pragma: no cover - fallback used when bs4 is missing
    BeautifulSoup = None  # type: ignore[assignment]
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class MetadataParseError(RuntimeError):
    """Raised when post metadata cannot be parsed from the page."""


@dataclass
class Post:
    """Representation of a scraped Facebook post."""

    metadata: Dict[str, Any]
    content: List[str]


def parse_post_metadata(container: Any) -> Dict[str, Any]:
    """Extract JSON metadata from a BeautifulSoup container."""
    data_ft = getattr(container, "get", lambda *_: None)("data-ft")
    if not data_ft:
        return {}

    try:
        return json.loads(data_ft)
    except json.JSONDecodeError as exc:
        raise MetadataParseError("Unable to parse post metadata") from exc


def extract_text_from_elements(elements: Iterable[WebElement]) -> List[str]:
    """Return the text content for each element in *elements*."""
    return [element.text for element in elements]


@dataclass
class _PostContainer:
    attrs: Dict[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        return self.attrs.get(key, default)


class _FallbackParser(HTMLParser):
    """Fallback HTML parser for environments without BeautifulSoup."""

    def __init__(self) -> None:
        super().__init__()
        self.containers: List[_PostContainer] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:  # type: ignore[override]
        if tag.lower() != "div":
            return

        attributes: Dict[str, str] = {key: value or "" for key, value in attrs}
        classes = attributes.get("class", "").split()
        if {"by", "di", "ds"}.issubset(set(classes)):
            self.containers.append(_PostContainer(attributes))


class FacebookScraper:
    """Encapsulates logic for scraping posts using a Selenium driver."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def load_feed(self, url: str) -> None:
        """Navigate the driver to the provided URL."""
        self.driver.get(url)

    def find_post_containers(self) -> Sequence[Any]:
        """Return BeautifulSoup containers for each post on the page."""
        html = self.driver.page_source
        if BeautifulSoup is not None:
            soup = BeautifulSoup(html, "html.parser")
            return soup.find_all("div", {"class": "by di ds"})

        parser = _FallbackParser()
        parser.feed(html)
        return parser.containers

    def open_post_links(self) -> Sequence[WebElement]:
        """Return WebElements representing "Full Story" links."""
        return self.driver.find_elements(By.LINK_TEXT, "Full Story")

    def open_post_in_new_tab(self, link_element: WebElement) -> None:
        """Open a link element in a new tab using keyboard shortcuts."""
        modifier = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
        link_element.send_keys(modifier + Keys.RETURN)

    def extract_post_content(self) -> List[str]:
        """Grab the text content from the currently active post page."""
        elements = self.driver.find_elements(By.XPATH, "//*[@class='bx' or @class='bv']")
        return extract_text_from_elements(elements)

    def scrape_posts(self) -> List[Post]:
        """Scrape post metadata and content for the current feed."""
        posts: List[Post] = []
        containers = self.find_post_containers()
        post_links = self.open_post_links()
        for index, container in enumerate(containers):
            metadata = parse_post_metadata(container)
            if index >= len(post_links):
                break

            link_element = post_links[index]
            self.open_post_in_new_tab(link_element)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            content = self.extract_post_content()
            posts.append(Post(metadata=metadata, content=content))

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        return posts


__all__ = [
    "FacebookScraper",
    "MetadataParseError",
    "Post",
    "extract_text_from_elements",
    "parse_post_metadata",
]
