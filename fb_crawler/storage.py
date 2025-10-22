"""Simple persistence layer for scraped posts."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Iterable
import json

from .scraper import Post


class StorageError(RuntimeError):
    """Raised when persisting scraped results fails."""


class JSONStorage:
    """Persist posts to a JSON file."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save_posts(self, posts: Iterable[Post]) -> None:
        data = [asdict(post) for post in posts]
        try:
            with self.path.open("w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, ensure_ascii=False)
        except OSError as exc:
            raise StorageError(f"Unable to write to {self.path}") from exc


__all__ = ["JSONStorage", "StorageError"]
