from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    in_queue = db.Column(db.Boolean, default=False)
    watched = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    imdb_rating = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(200), nullable=False)

    __table_args__ = (
        UniqueConstraint('title', name='uq_movie_title'),
    )
