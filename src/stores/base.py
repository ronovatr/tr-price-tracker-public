"""StoreEngine protocol. Wire your own fixtures or owned sites."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol


@dataclass
class Offer:
    store: str
    title: str
    url: str
    price: float
    currency: str = "TRY"


class StoreEngine(Protocol):
    name: str

    def search(self, query: str, limit: int = 20) -> List[Offer]:
        """Return offers for a category/query from allowed sources only."""
