"""
robots.txt helper. Fail closed if unread. For hosts you are allowed to hit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


@dataclass
class RobotsCache:
    parsers: dict[str, RobotFileParser] = field(default_factory=dict)

    def allowed(self, user_agent: str, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            return False
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if origin not in self.parsers:
            rp = RobotFileParser()
            rp.set_url(f"{origin}/robots.txt")
            try:
                rp.read()
            except Exception:  # noqa: BLE001
                # Fail closed for the demo skeleton: if robots cannot be read,
                # do not claim the path is allowed.
                return False
            self.parsers[origin] = rp
        return bool(self.parsers[origin].can_fetch(user_agent, url))


def path_allowed(url: str, user_agent: str = "EducationalDemoFetcher/1.0") -> bool:
    return RobotsCache().allowed(user_agent, url)
