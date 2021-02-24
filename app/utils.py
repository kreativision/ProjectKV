# Utility functions to use throughout the app.

from flask_mail import Message
from app import app, mail
from threading import Thread
from app.decorators import threader

# Redacts the email ID to show on the email-sent page.
def redact_email(mail_id):
    m_id = mail_id[0 : mail_id.index("@")]
    m_domain = mail_id[mail_id.index("@") :]
    redact = m_id[0:3] + ("*" * len(m_id[3:])) + m_domain
    return redact

# Send the mail
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_mail_async(app, msg)

# creates additional thread to actually send the email
@threader
def send_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)
