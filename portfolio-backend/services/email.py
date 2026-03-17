import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, content: str):
        try:
            print(f"DEBUG: Attempting to send email to {to_email} via SendGrid API")
            
            # SendGrid uses the verified Single Sender email
            from_email = os.getenv("EMAIL_USER", "vnikhilpatil@gmail.com")
            
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=content
            )

            sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
            response = sg.send(message)
            
            print(f"DEBUG: SendGrid Success! Status Code: {response.status_code}")
            return response
        except Exception as e:
            print(f"ERROR: SendGrid API failed for {to_email}. Error: {str(e)}")
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
