"""
Fictional ExampleMart engine.

Parses *local HTML fixtures* that look like a generic product grid.
There is no live ExampleMart website and no third-party retailer mapping.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import List

from .. import fetch
from .base import Offer


class _CardParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.offers: List[Offer] = []
        self._in_card = False
        self._in_title = False
        self._in_price = False
        self._title = ""
        self._price = ""
        self._href = ""

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        classes = attrs_d.get("class", "")
        if tag == "article" and "product-card" in classes.split():
            self._in_card = True
            self._title = ""
            self._price = ""
            self._href = ""
        if not self._in_card:
            return
        if tag == "a" and "product-link" in classes.split():
            self._href = attrs_d.get("href", "")
            self._in_title = True
        if tag == "span" and "price" in classes.split():
            self._in_price = True

    def handle_endtag(self, tag):
        if tag == "a" and self._in_title:
            self._in_title = False
        if tag == "span" and self._in_price:
            self._in_price = False
        if tag == "article" and self._in_card:
            self._in_card = False
            price = _parse_price(self._price)
            if self._title and self._href and price is not None:
                self.offers.append(
                    Offer(
                        store="ExampleMart",
                        title=self._title.strip(),
                        url=self._href.strip(),
                        price=price,
                    )
                )

    def handle_data(self, data):
        if self._in_title:
            self._title += data
        if self._in_price:
            self._price += data


_PRICE_RE = re.compile(r"([\d.,]+)")


def _parse_price(raw: str):
    m = _PRICE_RE.search(raw.replace("\xa0", " "))
    if not m:
        return None
    token = m.group(1)
    # TR-style: 12.345,67 or plain 1234.56
    if "," in token and "." in token:
        token = token.replace(".", "").replace(",", ".")
    elif "," in token:
        token = token.replace(",", ".")
    try:
        return float(token)
    except ValueError:
        return None


class ExampleMartEngine:
    name = "ExampleMart"
    fixture_name = "example_mart_search.html"

    def search(self, query: str, limit: int = 20) -> List[Offer]:
        html = fetch.load_fixture(self.fixture_name)
        parser = _CardParser()
        parser.feed(html)
        q = query.lower().strip()
        offers = [
            o
            for o in parser.offers
            if not q or q in o.title.lower()
        ]
        return offers[:limit]
