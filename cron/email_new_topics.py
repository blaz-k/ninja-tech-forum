import datetime

from models.settings import db
from models.topic import Topic
from models.user import User
from utils import send_email


def new_topics_email():
    today = datetime.datetime.now()
    monday = datetime.date.isoweekday(today)
    print(today)
    print(monday)
    if today == 1:
        yesterday_topics = db.query(Topic).filter(Topic.created > (datetime.datetime.now() - datetime.timedelta(days=1))).all()

        if not yesterday_topics:
            print("No new topics yesterday")
        else:
            message = "Topics created yesterday:\n"

            for topic in yesterday_topics:
                message += "{}\n".format(topic.title)

                print(message)

            users = db.query(User).all()

            for user in users:
                if user.email:
                    send_email(recipient=user.email, subject="New topic(s) to check!", body=message)
    else:
        print("No new topics at his point")


if __name__ == '__main__':
    new_topics_email()