from models.settings import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String, unique=False)
    last_name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    password = db.Column(db.String, unique=False)
    session_token = db.Column(db.String, unique=False)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.now())
    verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String)
