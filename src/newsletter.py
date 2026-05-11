from llm_client import get_llm_client, get_model
from prompts import OPENER_PROMPT, TAKEAWAY_PROMPT, EDITORIAL_PROMPT
from datetime import datetime, timezone


DISCLAIMER = ("\n\n---\n\n*This newsletter is AI-generated based on articles from your selected sources. Content may contain errors, always verify anything important before acting on it."
              "\n\nUntil next time 🤖 *")


def assemble_newsletter(sections: dict[str, str]) -> str:
    client = get_llm_client()
    model = get_model()

    sections_text = "\n\n---\n\n".join([
        f"## {name}\n\n{content}"
        for name, content in sections.items()
    ])

    topic_names = ", ".join(sections.keys())

    print("[Newsletter] Writing opener...")
    opener_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": OPENER_PROMPT.format(
            sections=sections_text,
            topic_names=topic_names
        )}]
    )
    opener = opener_response.choices[0].message.content
    if "<think>" in opener:
        opener = opener.split("</think>")[-1].strip()

    print("[Newsletter] Writing takeaway...")
    takeaway_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": TAKEAWAY_PROMPT.format(sections=sections_text)}]
    )
    takeaway = takeaway_response.choices[0].message.content
    if "<think>" in takeaway:
        takeaway = takeaway.split("</think>")[-1].strip()

    print("[Newsletter] Editorial pass...")
    editorial_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": EDITORIAL_PROMPT.format(
            sections=sections_text,
            topic_names=topic_names
        )}]
    )
    edited_sections = editorial_response.choices[0].message.content
    if "<think>" in edited_sections:
        edited_sections = edited_sections.split("</think>")[-1].strip()

    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    newsletter = f"""# Your Personal Newsletter 🤖 {date_str}

{opener}

---

{edited_sections}

---

{takeaway}
{DISCLAIMER}"""

    return newsletter