from llm_client import get_llm_client, get_model
from fetcher import fetch_articles, fetch_full_content
from state import get_last_run
from prompts import ARTICLE_SELECTION_PROMPT, INTEREST_SECTION_WRITER_PROMPT
from typing import Optional
import json
import re


def parse_urls(raw: str) -> list[str]:
    # Strip <think> blocks
    if "<think>" in raw:
        raw = raw.split("</think>")[-1].strip()
    # Strip markdown code blocks
    raw = re.sub(r"```[a-z]*\n?", "", raw).strip()
    raw = raw.replace("```", "").strip()
    # Parse JSON
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("urls", [])
    except json.JSONDecodeError:
        return []
    return []


def curate_interest(interest: dict) -> Optional[str]:
    client = get_llm_client()
    model = get_model()
    since = get_last_run()

    print(f"[{interest['name']}] Fetching articles since {since}...")
    articles = fetch_articles(interest, since)
    print(f"[{interest['name']}] Found {len(articles)} articles")

    if not articles:
        print(f"[{interest['name']}] No articles found, skipping")
        return None

    articles_text = "\n\n".join([
        f"URL: {a['link']}\nTitle: {a['title']}\nSummary: {a['summary']}"
        for a in articles
    ])

    print(f"[{interest['name']}] Pass 1: selecting best articles...")
    pass1_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": ARTICLE_SELECTION_PROMPT.format(
            interest_name=interest["name"],
            interest_description=interest.get("description", ""),
            keywords=", ".join(interest.get("keywords", [])),
            articles=articles_text
        )}]
    )

    raw = pass1_response.choices[0].message.content
    selected_urls = parse_urls(raw)
    print(f"[{interest['name']}] Selected URLs: {selected_urls}")

    if not selected_urls:
        print(f"[{interest['name']}] No URLs selected, skipping")
        return None

    print(f"[{interest['name']}] Fetching full content for {len(selected_urls)} articles...")
    full_articles = []
    for url in selected_urls:
        content = fetch_full_content(url)
        if content:
            full_articles.append(f"URL: {url}\n\n{content}")
            print(f"[{interest['name']}] Fetched content for {url}")
        else:
            print(f"[{interest['name']}] Could not fetch content for {url}")

    if not full_articles:
        print(f"[{interest['name']}] No full content fetched, skipping")
        return None

    print(f"[{interest['name']}] Pass 2: writing section...")
    full_articles_text = "\n\n---\n\n".join(full_articles)

    pass2_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": INTEREST_SECTION_WRITER_PROMPT.format(
            interest_name=interest["name"],
            interest_description=interest.get("description", ""),
            articles=full_articles_text
        )}]
    )

    raw2 = pass2_response.choices[0].message.content
    if "<think>" in raw2:
        raw2 = raw2.split("</think>")[-1].strip()

    print(f"[{interest['name']}] Done!")
    return raw2