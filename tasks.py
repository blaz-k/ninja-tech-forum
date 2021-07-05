import os
import random
from huey import RedisHuey
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

huey = RedisHuey(url=os.getenv('REDIS_URL'))


