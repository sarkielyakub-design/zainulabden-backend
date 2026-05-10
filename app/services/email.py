import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os


# =========================
# SMTP CONFIG
# =========================
SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 587

EMAIL = os.getenv(
    "EMAIL_ADDRESS"
)

PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)


# =========================
# GENERIC EMAIL
# =========================
def send_email(
    to_email: str,
    subject: str,
    body: str,
):

    try:

        msg = MIMEMultipart()

        msg["From"] = EMAIL

        msg["To"] = to_email

        msg["Subject"] = subject

        msg.attach(
            MIMEText(body, "plain")
        )

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        server.login(
            EMAIL,
            PASSWORD
        )

        server.send_message(msg)

        server.quit()

        print("✅ Email sent")

    except Exception as e:

        print(
            "❌ Email error:",
            str(e)
        )


# =========================
# BOOKING EMAIL
# =========================
def send_booking_email(
    email: str,
    first_name: str,
    booking_name: str,
):

    subject = (
        "Booking Confirmation"
    )

    body = f"""
Hello {first_name},

Your booking for:

{booking_name}

has been successfully confirmed.

Thank you for choosing
ZAINULABIDEEN TRAVEL AGENCY.

We will contact you shortly
with more details.

Best regards,
ZAINULABIDEEN TRAVEL
"""

    send_email(
        to_email=email,
        subject=subject,
        body=body,
    )