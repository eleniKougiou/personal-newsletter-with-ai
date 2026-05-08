from llm_client import get_llm_client, get_model
from prompts import TLDR_PROMPT, TAKEAWAY_PROMPT
from datetime import datetime, timezone


def assemble_newsletter(sections: dict[str, str]) -> str:
    client = get_llm_client()
    model = get_model()

    sections_text = "\n\n---\n\n".join([
        f"## {name}\n\n{content}"
        for name, content in sections.items()
    ])

    print("[Newsletter] Writing TL;DR...")
    tldr_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": TLDR_PROMPT.format(sections=sections_text)}]
    )
    tldr = tldr_response.choices[0].message.content
    if "<think>" in tldr:
        tldr = tldr.split("</think>")[-1].strip()

    print("[Newsletter] Writing takeaway...")
    takeaway_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": TAKEAWAY_PROMPT.format(sections=sections_text)}]
    )
    takeaway = takeaway_response.choices[0].message.content
    if "<think>" in takeaway:
        takeaway = takeaway.split("</think>")[-1].strip()

    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    newsletter = f"""# Your Daily Newsletter — {date_str}

## TL;DR
{tldr}

---

{sections_text}

---

## Today's Takeaway
{takeaway}"""

    return newsletter
