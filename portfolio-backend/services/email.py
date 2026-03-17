import os
import aiosmtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, content: str):
        message = EmailMessage()
        message["From"] = os.getenv("EMAIL_USER")
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(content)

        await aiosmtplib.send(
            message,
            hostname=os.getenv("EMAIL_HOST"),
            port=int(os.getenv("EMAIL_PORT", 587)),
            username=os.getenv("EMAIL_USER"),
            password=os.getenv("EMAIL_PASS"),
            start_tls=True,
        )

    @classmethod
    async def send_contact_notification(cls, data: dict):
        subject = f"New Portfolio Inquiry — {data['service']} from {data['name']}"
        content = f"""
New contact form submission:

Name:    {data['name']}
Email:   {data['email']}
Service: {data['service']}
Budget:  {data['budget']}

Message:
{data['message']}

---
Submitted at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Reply to: {data['email']}
"""
        await cls.send_email(os.getenv("NOTIFY_EMAIL"), subject, content)

    @classmethod
    async def send_auto_reply(cls, data: dict):
        subject = f"Got your message — Nikhil V"
        content = f"""
Hi {data['name']},

Thanks for reaching out! I've received your message 
about {data['service']} and will get back to you within 24 hours.

In the meantime, feel free to check my GitHub:
https://github.com/nikhilv

Talk soon,
Nikhil V
AI & Full-Stack Developer
"""
        await cls.send_email(data["email"], subject, content)
