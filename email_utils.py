import os
import sendgrid
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = ("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")

def send_marketing_email(to_email, subject, html_content):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    message = Mail(
        from_email='your_verified_email@example.com',
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    sg.send(message)

def send_ack_email(to_email, user_name):
    subject = "Appointment Confirmed"
    content = f"Hi {user_name},<br>Your appointment has been successfully booked!"
    send_marketing_email(to_email, subject, content)
