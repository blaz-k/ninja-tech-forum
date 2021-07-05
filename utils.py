import os
import logging


def send_email(recipient, subject, body, reply_to=None):
    if "DYNO" in os.environ:
        from tasks import send_email_task
        send_email_task(recipient, subject, body, reply_to)
    else:
        print("Hello localhost!")
        logging.warning("Recipient: " + recipient)
        logging.warning("Subject: " + subject)
        logging.warning("Body: " + body)
