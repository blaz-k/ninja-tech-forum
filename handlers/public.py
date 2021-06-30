import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from flask import render_template, request, redirect, url_for

from models.topic import Topic
from models.user import User
from models.settings import db


def home():
    topics =db.query(Topic).all()
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("index.html", user=user, topics=topics)
    return render_template("index.html", topics=topics)


def contact():
    if request.method == "GET":
        session_cookie = request.cookies.get("session")

        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                return render_template("contact.html", user=user)
        return render_template("contact.html")

    elif request.method == "POST":

        name = request.form.get("name")
        sender_email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        body = """
            name: {0}, 
            sender_email: {1},
            message: {2}.
        """.format(name, sender_email, message)

        email = Mail(from_email="blazyy@gmail.com",
                       to_emails=sender_email,
                       subject=subject,
                       html_content=body)

        # DELETE API KEY BEFORE UPLOADING TO GITHUB!!!!!!!
        sg_key = os.environ.get("SENDGRID_API_KEY")

        sg = SendGridAPIClient(sg_key)
        response = sg.send(email)

        # checking loggings

        logging.warning(response.status_code)
        logging.warning(response.body)
        logging.warning(response.headers)

        return redirect(url_for("public.contact"))


