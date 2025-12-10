import os
import requests


def send_email(to_email, subject, html_content):
    api_key = os.getenv("SENDGRID_API_KEY")

    data = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": "vasanijeet5@gmail.com"},
        "subject": subject,
        "content": [
            {
                "type": "text/html",
                "value": html_content
            }
        ]
    }

    r = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        json=data,
        headers={"Authorization": f"Bearer {api_key}"}
    )

    print("SendGrid:", r.status_code, r.text)