from db import db
from sqlalchemy import ForeignKey

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    next_feed = db.Column(db.DateTime, nullable=False)
    subscribe = db.Column(db.Boolean, nullable=False)
    tag = db.Column(db.String(30), nullable=False)
    history = db.relationship('History', backref='user')


class Feed(db.Model):
    feed_no = db.Column(db.Integer, primary_key=True)
    feed_links = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(30), nullable=False)
    titles = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    history = db.relationship('History', backref='feed')


class History(db.Model):
    hid = db.Column(db.Integer, primary_key=True)
    feed_no = db.Column(db.Integer, ForeignKey('feed.feed_no'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    date_and_time = db.Column(db.DateTime, nullable=False)
