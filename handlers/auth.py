import os
import logging
from flask import render_template, request, redirect, url_for, make_response
from hashlib import sha256
import uuid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from models.user import User
from models.settings import db


def login():
    if request.method == "GET":
        return render_template("/auth/login.html")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        password_hash = sha256(password.encode("utf-8")).hexdigest()

        existing_user = db.query(User).filter_by(username=username, password=password_hash, verified=True).first()

        if existing_user:
            session_token = str(uuid.uuid4())
            existing_user.session_token = session_token
            existing_user.save()

            response = make_response(redirect(url_for("dashboard.dashboard")))
            response.set_cookie("session", session_token)
            return response
        else:
            return render_template("/response/error-login.html")
    return redirect(url_for("dashboard.dashboard"))


def logout():
    session_cookie = request.cookies.get("session")
    user = db.query(User).filter_by(session_token=session_cookie).first()
    user.session_token = ""
    user.save()

    return redirect(url_for("auth.login"))


def registration():
    if request.method == "GET":
        return render_template("/auth/registration.html")

    elif request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        email = request.form.get("user-email")
        phone_number = request.form.get("telephone")
        password = request.form.get("password")
        repeat = request.form.get("repeat")

        existing_user = db.query(User).filter_by(username=username).first()

        if existing_user:
            return "ERROR: This username already exist! You need to choose something else."
        else:
            if password == repeat:
                password_hash = sha256(password.encode("utf-8")).hexdigest()
                verify_email_token = str(uuid.uuid4())

                new_user = User(username=username, first_name=first_name, last_name=last_name,
                                email=email, phone_number=phone_number, password=password_hash,
                                verification_token=verify_email_token)
                new_user.save()

                verification_url = "https://ninja-forum.herokuapp.com/verify-token/" + verify_email_token

                body = """
                    Verify your email for NINJA TECH FORUM: {}.
                """.format(verification_url)

                verification_message = Mail(from_email="blazyy@gmail.com",
                                            to_emails=email,
                                            subject="Verification of your email on NINJA TECH FORUM",
                                            html_content=body)

                sg_key = os.environ.get("SENDGRID_API_KEY")

                sg = SendGridAPIClient(sg_key)
                response = sg.send(verification_message)

                # checking loggings

                logging.warning(response.status_code)
                logging.warning(response.body)
                logging.warning(response.headers)

                return render_template("/response/successful.html")
            else:
                return render_template("/response/passwords-not-match.html")

    return redirect(url_for("public.home"))


def verify_token(token):
    user = db.query(User).filter_by(verification_token=token).first()

    if user:
        user.verified = True
        user.save()

    return redirect(url_for("auth.login"))





