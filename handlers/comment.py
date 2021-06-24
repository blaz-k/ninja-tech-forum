from flask import render_template, request, redirect, url_for

from models.topic import Topic
from models.user import User
from models.comment import Comment
from models.settings import db


#comment
#url za comment
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

