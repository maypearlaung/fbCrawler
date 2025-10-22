from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from fb_crawler.scraper import (
    FacebookScraper,
    MetadataParseError,
    extract_text_from_elements,
    parse_post_metadata,
)


class DummyContainer(SimpleNamespace):
    def get(self, key: str, default=None):  # type: ignore[override]
        return getattr(self, key.replace("-", "_"), default)


def test_parse_post_metadata_valid() -> None:
    payload = json.dumps({"id": 123})
    container = DummyContainer(data_ft=payload)
    metadata = parse_post_metadata(container)
    assert metadata == {"id": 123}


def test_parse_post_metadata_missing() -> None:
    container = DummyContainer()
    assert parse_post_metadata(container) == {}


def test_parse_post_metadata_invalid_json() -> None:
    container = DummyContainer(data_ft="{not:json}")
    with pytest.raises(MetadataParseError):
        parse_post_metadata(container)


def test_extract_text_from_elements() -> None:
    first = MagicMock()
    first.text = "Hello"
    second = MagicMock()
    second.text = "World"
    assert extract_text_from_elements([first, second]) == ["Hello", "World"]


def test_extract_post_content_uses_driver() -> None:
    driver = MagicMock()
    first = MagicMock(text="First")
    second = MagicMock(text="Second")
    driver.find_elements.return_value = [first, second]
    scraper = FacebookScraper(driver)

    result = scraper.extract_post_content()

    driver.find_elements.assert_called_once()
    assert result == ["First", "Second"]
