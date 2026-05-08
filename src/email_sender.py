import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone


def send_newsletter(content: str):
    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_SENDER_APP_PASSWORD")
    smtp_host = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "465"))

    if not all([sender, recipient, password]):
        raise ValueError("EMAIL_SENDER, EMAIL_RECIPIENT and EMAIL_SENDER_APP_PASSWORD must be set in .env")

    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your Daily Newsletter — {date_str}"
    msg["From"] = sender
    msg["To"] = recipient

    msg.attach(MIMEText(content, "plain"))

    print(f"[Email] Sending newsletter to {recipient}...")
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
    print("[Email] Sent!")