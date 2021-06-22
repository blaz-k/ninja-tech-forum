from flask import Flask, render_template, request, redirect, url_for

from models.topic import Topic
from models.user import User
from models.comment import Comment
from models.settings import db


def topic_create():

    if request.method == "GET":
        return render_template("topic-create.html")

    elif request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        session_token = request.cookies.get("session")
        user = db.query(User).filter_by(session_token=session_token).first()

        if not user:
            return redirect(url_for('login'))

        topic = Topic.create(title=title, description=description, author=user)

        return redirect(url_for('dashboard'))

