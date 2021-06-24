from flask import render_template, request

from models.user import User

from models.settings import db


def dashboard():

    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("dashboard.html", user=user)

    return render_template("/response/error.html")
