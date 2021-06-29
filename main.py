from flask import Flask
from models.settings import db

from handlers import public
from handlers import auth
from handlers import topic
from handlers import user
from handlers import dashboard
from handlers import comment


app = Flask(__name__)

db.create_all()

# AUTHENTICATION
app.add_url_rule(rule="/login", endpoint="auth.login", view_func=auth.login, methods=["GET", "POST"])
app.add_url_rule(rule="/logout", endpoint="auth.logout", view_func=auth.logout, methods=["GET"])
app.add_url_rule(rule="/registration", endpoint="auth.registration", view_func=auth.registration, methods=["GET", "POST"])


# COMMENT
app.add_url_rule(rule="/topic/<topic_id>/add-comment", endpoint="comment.user_comment", view_func=comment.user_comment, methods=["POST"])
app.add_url_rule(rule="/comment/<comment_id>/edit", endpoint="comment.edit_comment", view_func=comment.edit_comment, methods=["GET", "POST"])
app.add_url_rule(rule="/comment/<comment_id>/delete", endpoint="comment.delete_comment", view_func=comment.delete_comment, methods=["GET", "POST"])


# DASHBOARD
app.add_url_rule(rule="/dashboard", endpoint="dashboard.dashboard", view_func=dashboard.dashboard, methods=["GET", "POST"])


# USER
app.add_url_rule(rule="/dashboard/edit-profile", endpoint="user.edit_profile", view_func=user.edit_profile, methods=["GET", "POST"])


# PUBLIC
app.add_url_rule(rule="/", endpoint="public.home", view_func=public.home, methods=["GET"])
app.add_url_rule(rule="/contact", endpoint="public.contact", view_func=public.contact, methods=["GET"])


# TOPIC
app.add_url_rule(rule="/dashboard/topic-create", endpoint="topic.topic_create", view_func=topic.topic_create, methods=["GET", "POST"])
app.add_url_rule(rule="/topics", endpoint="topic.topics", view_func=topic.topics, methods=["GET"])
app.add_url_rule(rule="/topic/<topic_id>", endpoint="topic.topic_details", view_func=topic.topic_details, methods=["GET", "POST"])


if __name__ == '__main__':
    app.run(use_reloader=True)