import os
import resend
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, content: str, is_notification: bool = False):
        try:
            print(f"DEBUG: Attempting to send email to {to_email} via Resend API")
            
            resend.api_key = os.getenv("RESEND_API_KEY")
            
            # Resend uses this sandbox email until you verify a custom domain
            from_email = "onboarding@resend.dev"
            
            params = {
                "from": f"Nikhil Portfolio <{from_email}>",
                "to": to_email,
                "subject": subject,
                "text": content,
                "html": f"<pre style='font-family: inherit;'>{content}</pre>"
            }

            response = resend.Emails.send(params)
            
            print(f"DEBUG: Resend Response for {to_email}:")
            print(response)
            
            return response
        except Exception as e:
            print(f"ERROR: Resend API failed for {to_email}. Error: {str(e)}")
            # If this is an auto-reply, it's expected to fail on the free tier 
            # (you can only send TO your registered email).
            if not is_notification:
                print("NOTE: Auto-replies to external emails require a verified domain on Resend.")
            else:
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
        # is_notification=True ensures we surface the error if this fails
        await cls.send_email(os.getenv("NOTIFY_EMAIL"), subject, content, is_notification=True)

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
        # is_notification=False because this WILL fail if sending to a generic user 
        # (until a custom domain is verified in Resend)
        await cls.send_email(data["email"], subject, content, is_notification=False)
