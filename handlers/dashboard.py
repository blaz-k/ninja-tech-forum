from flask import Flask, render_template, request, redirect, url_for, make_response
from hashlib import sha256

from models.topic import Topic
from models.user import User
from models.comment import Comment

from models.settings import db
from datetime import datetime


def dashboard():

    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("dashboard.html", user=user)

    return render_template("error.html")
