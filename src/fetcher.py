import feedparser
import json
from datetime import datetime, timezone
import trafilatura


def fetch_articles(interest: dict, since: datetime) -> list[dict]:
    articles = []

    for url in interest.get("trusted_sources", []):
        feed = feedparser.parse(url)
        count = 0

        for entry in feed.entries:
            if count >= 20:
                break

            published = entry.get("published_parsed")
            if published:
                published_dt = datetime(*published[:6], tzinfo=timezone.utc)
                if published_dt <= since:
                    continue

            articles.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "source": feed.feed.get("title", url),
                "published": entry.get("published", "")
            })
            count += 1

    return articles


def fetch_full_content(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    return trafilatura.extract(downloaded) or ""


def load_interests() -> list[dict]:
    with open("../config/interests.json", "r") as f:
        return json.load(f)