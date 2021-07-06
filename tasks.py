import os
from huey import RedisHuey
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

huey = RedisHuey(url=os.getenv('REDIS_URL'))


@huey.task(retries=3, retry_delay=3)
def send_email_task(recipient, subject, body, reply_to=None):
    message = Mail(from_email="blazyy@gmail.com",
                   to_emails=recipient,
                   subject=subject,
                   html_content=body)
    if reply_to:
        message.reply_to = reply_to

    sg_key = os.environ.get("SENDGRID_API_KEY")

    sg = SendGridAPIClient(sg_key)
    response = sg.send(message)

    # checking loggings
    logging.warning(response.status_code)
    logging.warning(response.body)
    logging.warning(response.headers)

    if int(response.status_code) != int(200) or int(response.status_code) != int(202):
        raise Exception("Error sending via SendGrid")
