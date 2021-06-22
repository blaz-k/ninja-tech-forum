from flask import Flask, render_template, request

from models.topic import Topic
from models.user import User
from models.comment import Comment
from models.settings import db


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

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("contact.html", user=user)
    return render_template("contact.html")

