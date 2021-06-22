from flask import Flask, render_template, request, redirect, url_for, make_response
from hashlib import sha256
import uuid

from models.topic import Topic
from models.user import User
from models.comment import Comment
from models.settings import db

from handlers import public
from handlers import auth
from handlers import topic
from handlers import user


app = Flask(__name__)

db.create_all()


# PUBLIC
app.add_url_rule(rule="/", endpoint="public.home", view_func=public.home, methods=["GET"])
app.add_url_rule(rule="/contact", endpoint="public.contact", view_func=public.contact, methods=["GET"])


# AUTHENTICATION
app.add_url_rule(rule="/login", endpoint="auth.login", view_func=auth.login, methods=["GET", "POST"])
app.add_url_rule(rule="/logout", endpoint="auth.logout", view_func=auth.logout, methods=["GET"])
app.add_url_rule(rule="/registration", endpoint="auth.registration", view_func=auth.registration, methods=["GET", "POST"])


# TOPIC
app.add_url_rule(rule="/dashboard/topic-create", endpoint="topic.topic_create", view_func=topic.topic_create, methods=["GET", "POST"])
app.add_url_rule(rule="/topics", endpoint="topic.topics", view_func=topic.topics, methods=["GET"])
app.add_url_rule(rule="/topic/<topic_id>", endpoint="topic.topic_details", view_func=topic.topic_details, methods=["GET", "POST"])


# USER
app.add_url_rule(rule="/dashboard/edit-profile", endpoint="user.edit_profile", view_func=user.edit_profile, methods=["GET", "POST"])




@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("dashboard.html", user=user)

    return render_template("error.html")


if __name__ == '__main__':
    app.run(use_reloader=True)