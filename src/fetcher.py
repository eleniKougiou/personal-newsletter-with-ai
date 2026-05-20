import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from llm_client import get_llm_client, get_model
from prompts import ARTICLE_EXTRACTION_PROMPT
import trafilatura


def fetch_articles(interest: dict) -> list[dict]:
    client = get_llm_client()
    model = get_model()
    articles = []

    for url in interest.get("trusted_sources", []):
        try:
            print(f"[Fetcher] Fetching {url}...")
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})

            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "meta", "link", "svg", "img"]):
                tag.decompose()
            content = str(soup)[:40000]

            print(f"[Fetcher] Content length for {url}: {len(content)} chars")
            print(f"[Fetcher] Extracting articles from {url}...")

            extraction_response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": ARTICLE_EXTRACTION_PROMPT.format(html=content)}]
            )

            raw = extraction_response.choices[0].message.content
            print(f"[Fetcher] Raw extraction response for {url}: {raw[:500]}")
            if "<think>" in raw:
                raw = raw.split("</think>")[-1].strip()

            raw = re.sub(r"```[a-z]*\n?", "", raw).strip()
            raw = raw.replace("```", "").strip()

            try:
                data = json.loads(raw)
                extracted = data.get("articles", [])
                print(f"[Fetcher] Raw extracted articles: {extracted[:3]}")
                for item in extracted:
                    articles.append({
                        "title": item.get("title", ""),
                        "link": urljoin(url, item.get("url", "")),
                        "source": url
                    })
                print(f"[Fetcher] Extracted {len(extracted)} articles from {url}")
            except json.JSONDecodeError:
                print(f"[Fetcher] Failed to parse articles from {url}")

        except Exception as e:
            print(f"[Fetcher] Failed to fetch {url}: {e}")

    return articles


def fetch_full_content(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    return trafilatura.extract(downloaded) or ""


def load_interests() -> list[dict]:
    with open("../config/interests.json", "r") as f:
        return json.load(f)