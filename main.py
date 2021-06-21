from flask import Flask, render_template, request, redirect, url_for, make_response
from hashlib import sha256
import uuid

from models.topic import Topic
from models.user import User
from models.comment import Comment
from models.settings import db


app = Flask(__name__)

db.create_all()


@app.route("/blog")
def blog():
    topics = db.query(Topic).all()

    return render_template("blog.html", topics=topics)


@app.route("/")
def home():
    topics =db.query(Topic).all()
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("index.html", user=user, topics=topics)
    return render_template("index.html", topics=topics)


@app.route("/contact")
def contact():
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("contact.html", user=user)
    return render_template("contact.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("dashboard.html", user=user)

    return render_template("error.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        password_hash = sha256(password.encode("utf-8")).hexdigest()

        existing_user = db.query(User).filter_by(username=username, password=password_hash).first()

        if existing_user:
            session_token = str(uuid.uuid4())
            existing_user.session_token = session_token
            existing_user.save()

            response = make_response(redirect(url_for("dashboard")))
            response.set_cookie("session", session_token)
            return response
        else:
            return render_template("error-login.html")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session_cookie = request.cookies.get("session")
    user = db.query(User).filter_by(session_token=session_cookie).first()
    user.session_token = ""
    user.save()

    return redirect(url_for("login"))


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("registration.html")

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
                new_user = User(username=username, first_name=first_name, last_name=last_name,
                                email=email,
                                phone_number=phone_number, password=password_hash)
                new_user.save()

                return render_template("successful.html")
            else:
                return "ERROR: This username already exist! You need to choose something else."

    return redirect(url_for("home"))


@app.route("/dashboard/topic", methods=["GET", "POST"])
def topic():

    if request.method == "GET":
        return render_template("topic.html")

    elif request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        session_token = request.cookies.get("session")
        user = db.query(User).filter_by(session_token=session_token).first()

        if not user:
            return redirect(url_for('login'))

        topic = Topic.create(title=title, description=description, author=user)

        return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(use_reloader=True)