from django.conf import settings
import smtplib
from email.message import EmailMessage
from celery import shared_task


@shared_task()
def send_email(subject, message, recipient_list):
    message = EmailMessage()
    message.set_content(message)
    message["Subject"] = subject
    message["From"] = settings.SMPT_EMAIL
    message["To"] = recipient_list
    smtp_server = smtplib.SMTP(settings.SMPT_HOST, settings.SMPT_PORT)
    smtp_server.starttls()
    smtp_server.login(settings.SMPT_EMAIL, settings.SMPT_PASSWORD)
    smtp_server.send_message(message)
    smtp_server.quit()
