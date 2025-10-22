"""Configuration handling for the Facebook crawler."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping
import json


class ConfigError(ValueError):
    """Raised when the configuration file is missing required values."""


@dataclass(frozen=True)
class CrawlerConfig:
    """Configuration values required to run the crawler."""

    url: str
    chrome_profile_dir: str
    profile_directory: str = "Default"
    headless: bool = False

    def __post_init__(self) -> None:
        if not self.url:
            raise ConfigError("The crawler URL cannot be empty.")
        if not self.chrome_profile_dir:
            raise ConfigError("The chrome_profile_dir setting cannot be empty.")

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "CrawlerConfig":
        """Create a :class:`CrawlerConfig` from a mapping, validating keys."""
        unknown_keys = set(data) - {
            "url",
            "chrome_profile_dir",
            "profile_directory",
            "headless",
        }
        if unknown_keys:
            raise ConfigError(f"Unknown configuration keys: {sorted(unknown_keys)}")

        try:
            url = str(data["url"])
            chrome_profile_dir = str(data["chrome_profile_dir"])
        except KeyError as exc:
            raise ConfigError(f"Missing configuration value: {exc.args[0]}") from exc

        profile_directory = str(data.get("profile_directory", "Default"))
        headless = bool(data.get("headless", False))
        return cls(
            url=url,
            chrome_profile_dir=chrome_profile_dir,
            profile_directory=profile_directory,
            headless=headless,
        )

    @classmethod
    def load(cls, path: str | Path) -> "CrawlerConfig":
        """Load configuration from a JSON file."""
        file_path = Path(path)
        if not file_path.exists():
            raise ConfigError(f"Configuration file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as handle:
            data: Dict[str, Any] = json.load(handle)
        return cls.from_mapping(data)


__all__ = ["ConfigError", "CrawlerConfig"]
