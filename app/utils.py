# Utility functions to use throughout the app.

from flask_mail import Message
from flask_login import current_user
from app import app, mail, db
from app.models import User
from threading import Thread
from app.decorators import threader
from app import encryptor

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

# Updates user details.
def update_user(form_data):
    current_user.username = form_data["username"]
    current_user.email = form_data["email"]
    current_user.contact = form_data["contact"]
    db.session.commit()

# updates user password
def change_password(new_password):
    current_user.password = encryptor.generate_password_hash(new_password).decode("utf-8")
    db.session.commit()