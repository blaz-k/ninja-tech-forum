from models.settings import db
from datetime import datetime


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, unique=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.now())
