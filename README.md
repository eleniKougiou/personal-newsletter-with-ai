# personal-newsletter-with-ai

A self-hosted AI-powered newsletter that scrapes sources you trust, picks the most relevant articles, and writes them up like a smart friend would. Then sends everything to your inbox on a schedule.

The project is built for personal use. If you find it useful, feel free to fork and make it your own:)

---

## How it works

You choose topics you care about and sources you trust. You set a schedule. 

The rest is automatic: articles get scraped, filtered, and written up in a conversational tone with inline sources, assembled into a formatted HTML email, and sent to your inbox.

---

## Want to try it?

You'll need:
- An API key for any OpenAI-compatible LLM provider (OpenAI, Groq, Together, Ollama, etc.)
- A Gmail account to send from (App Password required)

Then:
1. Fork the repo and copy `.env.example` to `.env` with your values
2. Edit `config/interests.json` to define your topics, sources, and keywords
3. Set up your secrets in GitHub Actions and let it run — or test locally with `python src/main.py`

The prompts in `src/prompts.py` control the tone and style of every section. Tweak to match your taste.

---

*AI makes mistakes and so do hobby projects. Verify anything important, and watch your API usage.*