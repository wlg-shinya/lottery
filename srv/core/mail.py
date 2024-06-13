from smtplib import SMTP
from email.mime.text import MIMEText
from core.config import env

def send_gmail(to_email: str, from_email: str, subject: str, body: str):
    mime = MIMEText(body, "plain")
    mime['Subject'] = subject
    mime['To'] = to_email
    mime['From'] = from_email

    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    server = SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(from_email, env().smtp_password)
    server.send_message(mime)
    server.quit()