import uuid

from flask import request, redirect, url_for, render_template

from models.subscribe import Subscribe
from models.topic import Topic
from models.user import User
from models.comment import Comment
from models.settings import db, redis
from utils import send_email, is_localhost


def create_comment(topic_id):
    topic = db.query(Topic).get(int(topic_id))
    session_cookie = request.cookies.get("session")

    user = None
    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()

        comment_content = request.form.get("content")

        new_comment_content = Comment(content=comment_content, topic=topic, author=user)
        new_comment_content.save()

        subscriptions = db.query(Subscribe).filter_by(topic=topic).all()

        for item in subscriptions:
            subscriber = db.query(User).filter_by(id=item.user_id).first()

            topic_url = "http://127.0.0.1:5000/topic/{}".format(topic.id)

            if not is_localhost():
                topic_url = "https://ninja-forum.herokuapp.com/topic/{}".format(topic.id)

            body = """
                There is a new comment in topic {0}\n
                Link for this topic: {1}\n
                Comment: {2}
            """.format(topic.title, topic_url, comment_content)
            send_email(recipient=subscriber.email,
                       subject="new comment in topic: "+topic.title,
                       body=body)

        return redirect(url_for("topic.topic_details", topic_id=topic_id))


def edit_comment(comment_id):
    session_cookie = request.cookies.get("session")
    user = db.query(User).filter_by(session_token=session_cookie).first()

    if not user:
        return render_template("response/error.html")

    comment = db.query(Comment).filter_by(id=int(comment_id)).first()

    if comment.author != user:
        return render_template("/response/error-comment.html")

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
        return render_template("/response/error-comment.html")

    if request.method == "GET":
        csrf_token = str(uuid.uuid4())
        redis.set(name=csrf_token, value=user.username)
        return render_template("comment/delete.html", comment=comment, csrf_token=csrf_token)

    elif request.method == "POST":

        content = request.form.get("content")
        csrf = request.form.get("csrf")

        existing_csrf = redis.get(csrf).decode()

        if existing_csrf and existing_csrf == user.username:
            comment.content = content
            comment.delete()

        return redirect(url_for("topic.topic_details", topic_id=comment.topic_id))







