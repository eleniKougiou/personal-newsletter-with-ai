# personal-newsletter-with-ai

An AI-powered personal newsletter that explores sources you trust, picks what's worth your attention and sends it to your inbox on a schedule you control.

The project is built for personal use. If you find it useful, feel free to fork and make it your own:)

---

## How it works

1. You define topics you care about in `config/interests.json`, each with a description, keywords, and a list of trusted sources
2. The curator scrapes those sources, selects the most relevant articles, and fetches their full content
3. An LLM writes a newsletter section per topic with inline citations
4. The sections are assembled, editorially polished, and sent as a formatted HTML email

The last-run timestamp is saved to `config/state.json` after each run, so the next run only looks at new content.

---

## Want to set it up?

### 1. Clone and install

    git clone https://github.com/eleniKougiou/personal-newsletter-with-ai.git
    cd personal-newsletter-with-ai
    pip install -r requirements.txt

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

    cp .env.example .env

| Variable | Description                                                                                             |
|---|---------------------------------------------------------------------------------------------------------|
| `LLM_BASE_URL` | Base URL of your LLM provider                                                                           |
| `LLM_API_KEY` | Your API key                                                                                            |
| `LLM_MODEL` | Model name, e.g. `gpt-4o` or `Qwen/Qwen3.5-397B-A17B-FP8`                                               |
| `EMAIL_SENDER` | Gmail address used to send the newsletter                                                               |
| `EMAIL_SENDER_APP_PASSWORD` | [Gmail App Password](https://support.google.com/accounts/answer/185833) - not your regular password     |
| `EMAIL_RECIPIENT` | Where to send the newsletter. Supports multiple: `a@x.com,b@x.com`                                      |
| `EMAIL_SMTP_HOST` | SMTP host (default: `smtp.gmail.com`)                                                                   |
| `EMAIL_SMTP_PORT` | SMTP port (default: `465`)                                                                              |
| `DEV_MODE` | Set to `true` to always fetch articles from the past week, ignoring last run state - useful for testing |

The project uses the OpenAI Python SDK with a configurable `base_url`. An API key for any provider offering an OpenAI-compatible API will work.

---

## Want to customise it?

### Topics and sources

Edit `config/interests.json` to define what you want covered. Each entry is a topic:
```json
    [
      {
        "name": "Science & Technology",
        "description": "Big developments in tech and science worth knowing about.",
        "keywords": ["space", "AI", "physics"],
        "trusted_sources": [
          "https://some_source",
          "https://some_other_source"
        ]
      }
    ]
```

| Field | Description |
|---|---|
| `name` | Becomes the section header in your newsletter |
| `description` | Tells the LLM what to focus on and what to skip |
| `keywords` | Used to prioritize relevant articles — signal boost, not a strict filter |
| `trusted_sources` | Pages the scraper will pull articles from |


### Prompts

All LLM prompts live in `src/prompts.py`. Each one controls a different stage of the pipeline - article selection, section writing, editorial pass, opener, and closing. The tone, focus, and style of the newsletter is largely defined here. Adjust to match your taste.

---

## Want to run it?

### Locally

Make sure your `.env` file is set up first, then run:

    cd src
    python main.py

Set `DEV_MODE=true` in your `.env` to always fetch articles from the past week regardless of when you last ran it (useful for testing).

### Automated with GitHub Actions

The repo includes a workflow defined in `.github/workflows/newsletter.yml` that runs the newsletter daily at **17:00 UTC** and commits the updated run state back to the repo automatically.

**To set it up:**

1. Fork the repo
2. Go to **Settings → Secrets and variables → Actions**
3. Add the following **Secrets**: `LLM_BASE_URL`, `LLM_API_KEY`, `EMAIL_RECIPIENT`, `EMAIL_SENDER`, `EMAIL_SENDER_APP_PASSWORD`
4. Add the following **Variables**: `LLM_MODEL`, `DEV_MODE`
5. Enable Actions on your fork if prompted

The workflow can also be triggered manually from the **Actions** tab at any time.

**To change the schedule**, edit the cron expression in `.github/workflows/newsletter.yml`:

    - cron: '0 17 * * *'  # every day at 17:00 UTC
---

*The newsletter is AI-generated. AI can make mistakes. Verify anything important, and keep an eye on your API costs.*