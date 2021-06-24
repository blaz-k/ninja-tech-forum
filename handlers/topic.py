from flask import render_template, request, redirect, url_for

from models.topic import Topic
from models.user import User
from models.comment import Comment
from models.settings import db


def topics():
    if request.method == "GET":
        topics = db.query(Topic).all()
        session_cookie = request.cookies.get("session")

        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                return render_template("/topic/topics.html", topics=topics, user=user)
        return render_template("/topic/topics.html", topics=topics)


def topic_create():

    if request.method == "GET":
        return render_template("/topic/topic-create.html")

    elif request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        session_token = request.cookies.get("session")
        user = db.query(User).filter_by(session_token=session_token).first()

        if not user:
            return redirect(url_for('/auth/login'))

        topic = Topic.create(title=title, description=description, author=user)

        return redirect(url_for('dashboard.dashboard'))


def topic_details(topic_id):
    topic = db.query(Topic).get(int(topic_id))
    session_cookie = request.cookies.get("session")
    comments = db.query(Comment).filter_by(topic=topic).all()

    user = None
    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
    topics =db.query(Topic).all()

    if not topic:
        return render_template("/response/not-found.html", user=user)

    return render_template("topic/topic.html", topic=topic, topics=topics, user=user, comments=comments)



