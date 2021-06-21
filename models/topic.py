from models.settings import db
from datetime import datetime




class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    description = db.Column(db.String, unique=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship("User")
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.now())

    @classmethod
    def create(cls, title, description, author):
        topic = cls(title=title, description=description, author=author)
        db.add(topic)
        db.commit()

        return topic
