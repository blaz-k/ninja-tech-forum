
from flask import render_template, request

from models.topic import Topic
from models.user import User
from models.settings import db
from utils import send_email


def home():
    topics =db.query(Topic).all()
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("index.html", user=user, topics=topics)
    return render_template("index.html", topics=topics)


def contact():
    session_cookie = request.cookies.get("session")

    if request.method == "GET":

        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                return render_template("contact.html", user=user)
        return render_template("contact.html")

    elif request.method == "POST":

        name = request.form.get("name")
        sender_email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                return render_template("contact.html", user=user)
            return render_template("contact.html")
        send_email(recipient="blazyy@gmail.com", subject=subject, user_name=name, body=message)

        return render_template("/response/successful-message.html")


