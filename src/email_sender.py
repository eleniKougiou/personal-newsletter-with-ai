import os
import markdown
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone


def send_newsletter(content: str):
    sender = os.getenv("EMAIL_SENDER")
    recipients = [r.strip() for r in os.getenv("EMAIL_RECIPIENT", "").split(",") if r.strip()]
    password = os.getenv("EMAIL_SENDER_APP_PASSWORD")
    smtp_host = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "465"))

    if not all([sender, recipients, password]):
        raise ValueError("EMAIL_SENDER, EMAIL_RECIPIENT and EMAIL_SENDER_APP_PASSWORD must be set in .env")

    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your Personal Newsletter 🤖 {date_str}"
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    html_body = markdown.markdown(content, extensions=["extra", "nl2br"])
    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      body {{ font-family: Georgia, serif; max-width: 680px; margin: 40px auto; color: #222; line-height: 1.7; }}
      h1 {{ font-size: 1.8em; border-bottom: 2px solid #333; padding-bottom: 8px; }}
      h2 {{ font-size: 1.3em; margin-top: 2em; color: #111; }}
      hr {{ border: none; border-top: 1px solid #ddd; margin: 2em 0; }}
      a {{ color: #1a73e8; }}
      p {{ margin: 0.8em 0; }}
    </style>
    </head>
    <body>
    {html_body}
    </body>
    </html>"""

    msg.attach(MIMEText(content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    print(f"[Email] Sending newsletter to {', '.join(recipients)}...")
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())
    print("[Email] Sent!")