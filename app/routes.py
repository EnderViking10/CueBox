import urllib.parse

import requests
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc
from werkzeug.security import check_password_hash

import app
from app.models import db, Movie, User

main = Blueprint('main', __name__)


@main.route('/')
def home():
    movies = Movie.query.filter_by(in_queue=False, watched=False).all()
    return render_template('suggestions.html', movies=movies)


@main.route('/queue')
def queue():
    movies = Movie.query.filter_by(in_queue=True).all()
    return render_template('queue.html', movies=movies)


@main.route('/watched', methods=['GET', 'POST'])
def watched_movies():
    """Page displaying watched movies"""
    movies = Movie.query.filter_by(watched=True).order_by(desc(Movie.id)).all()
    return render_template('watched.html', movies=movies)


@main.route('/add', methods=['POST'])
def add_movie():
    title = request.form.get('title')
    if title:
        if len(title) > 50:
            flash('Movie title must be less than 64 characters', 'danger')
            return redirect(url_for('main.home'))

        url_movie_title = urllib.parse.quote_plus(title)

        api_call = f"https://www.omdbapi.com/?t={url_movie_title}&apikey={app.Config.OMDB_API_KEY}"
        response = requests.get(api_call)

        # Check if the response is successful
        if response.status_code == 200:
            # Parse the JSON data
            data = response.json()
            if data.get("Response") == "False":
                flash('Movie title does not exist.', 'danger')
                return redirect(url_for('main.home'))
        else:
            abort(response.status_code)

        new_movie = Movie(
            title=data.get('Title'),
            year=data.get('Year'),
            runtime=data.get('Runtime'),
            genre=data.get('Genre'),
            imdb_rating=data.get('imdbRating')
        )
        db.session.add(new_movie)
        db.session.commit()
    return redirect(url_for('main.home'))


@main.route('/mark_queue/<int:movie_id>')
@login_required
def mark_queue(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if not current_user.is_admin:
        abort(403)
    movie.in_queue = True
    db.session.commit()
    flash('Movie moved to queue!', 'success')
    return redirect(url_for('main.home'))


@main.route('/mark_watched/<int:movie_id>')
@login_required
def mark_watched(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if not current_user.is_admin:
        abort(403)
    movie.in_queue = False
    movie.watched = True
    db.session.commit()
    flash('Movie marked as watched!', 'success')
    return redirect(url_for('main.queue'))


@main.route('/delete_movie/<int:movie_id>')
@login_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if not current_user.is_admin:
        abort(403)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie has been deleted', 'success')
    return redirect(request.referrer or url_for('main.home'))


@main.route('/delete_all')
@login_required
def delete_all():
    movies = Movie.query.filter_by(in_queue=False, watched=False)
    if not current_user.is_admin:
        abort(403)
    for movie in movies:
        db.session.delete(movie)
    db.session.commit()
    flash('Deleted all movies', 'success')
    return redirect(url_for('main.home'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for user authentication."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('main.home'))
