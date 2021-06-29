import uuid

from flask import request, redirect, url_for, render_template

from models.topic import Topic
from models.user import User
from models.comment import Comment
from models.settings import db, redis


def user_comment(topic_id):
    topic = db.query(Topic).get(int(topic_id))
    session_cookie = request.cookies.get("session")

    user = None
    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()

        comment_content = request.form.get("content")

        new_comment_content = Comment(content=comment_content, topic=topic, author=user)
        new_comment_content.save()

        return redirect(url_for("topic.topic_details", topic_id=topic_id))


def edit_comment(comment_id):
    session_cookie = request.cookies.get("session")
    user = db.query(User).filter_by(session_token=session_cookie).first()

    if not user:
        return render_template("response/error.html")

    comment = db.query(Comment).filter_by(id=int(comment_id)).first()

    if comment.author != user:
        return "ERROR: You are not comment author!!"

    if request.method == "GET":
        csrf_token = str(uuid.uuid4())
        redis.set(name=csrf_token, value=user.username)
        return render_template("/comment/edit.html", comment=comment, csrf_token=csrf_token)

    elif request.method == "POST":

        content = request.form.get("content")
        csrf = request.form.get("csrf")

        existing_csrf = redis.get(csrf).decode()

        if existing_csrf and existing_csrf == user.username:
            comment.content = content
            comment.save()

        return redirect(url_for("topic.topic_details", topic_id=comment.topic_id))


def delete_comment(comment_id):
    session_cookie = request.cookies.get("session")
    user = db.query(User).filter_by(session_token=session_cookie).first()
    if not user:
        return render_template("response/error.html")

    comment = db.query(Comment).filter_by(id=int(comment_id)).first()

    if comment.author != user:
        return "ERROR: You are not comment author!!"

    if request.method == "GET":
        return render_template("comment/delete.html", comment=comment)

    elif request.method == "POST":

        content = request.form.get("content")

        comment.content = content
        comment.delete()

        return redirect(url_for("topic.topic_details", topic_id=comment.topic_id))







