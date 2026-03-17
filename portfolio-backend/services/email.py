import os
import resend
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configure Resend
resend.api_key = os.getenv("RESEND_API_KEY")

class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, content: str):
        try:
            print(f"DEBUG: Attempting to send email to {to_email} via Resend API")
            
            # Resend requires a verified domain or uses onboarding@resend.dev for testing
            # We'll use the EMAIL_USER if it looks like a custom domain email, 
            # otherwise default to onboarding@resend.dev
            from_email = os.getenv("EMAIL_USER", "onboarding@resend.dev")
            if "gmail.com" in from_email.lower():
                from_email = "onboarding@resend.dev"

            params = {
                "from": f"Portfolio <{from_email}>",
                "to": [to_email],
                "subject": subject,
                "text": content,
            }

            # Resend's library is synchronous for now, but we'll wrap it if needed.
            # Usually it's fast enough for background tasks or immediate await.
            email = resend.Emails.send(params)
            print(f"DEBUG: Successfully sent email to {to_email}. ID: {email['id']}")
            return email
        except Exception as e:
            print(f"ERROR: Resend API failed for {to_email}. Error: {str(e)}")
            raise e

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
        # We wrap this in a try-except because Resend trial accounts 
        # can ONLY send to the account owner. 
        # Attempting to send to the visitor will fail.
        try:
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
        except Exception as e:
            print(f"NOTICE: Auto-reply to visitor ignored (likely Resend trial restriction). Error: {str(e)}")
            # We don't re-raise here so the main notification still succeeds
