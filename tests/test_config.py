from __future__ import annotations

import json
from pathlib import Path

import pytest

from fb_crawler.config import ConfigError, CrawlerConfig


def test_from_mapping_success() -> None:
    config = CrawlerConfig.from_mapping({
        "url": "https://example.com",
        "chrome_profile_dir": "--user-data-dir=/tmp/profile",
    })
    assert config.url == "https://example.com"
    assert config.chrome_profile_dir == "--user-data-dir=/tmp/profile"
    assert config.profile_directory == "Default"


def test_from_mapping_missing_key() -> None:
    with pytest.raises(ConfigError):
        CrawlerConfig.from_mapping({"url": "https://example.com"})


def test_load_reads_file(tmp_path: Path) -> None:
    config_data = {
        "url": "https://example.com",
        "chrome_profile_dir": "--user-data-dir=/tmp/profile",
        "profile_directory": "Profile 1",
        "headless": True,
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))

    config = CrawlerConfig.load(config_file)

    assert config.profile_directory == "Profile 1"
    assert config.headless is True


def test_load_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    with pytest.raises(ConfigError):
        CrawlerConfig.load(missing)
