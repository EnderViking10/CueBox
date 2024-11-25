from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Movie, User
from werkzeug.security import check_password_hash

main = Blueprint('main', __name__)


@main.route('/')
def home():
    movies = Movie.query.filter_by(in_queue=True).all()
    return render_template('queue.html', movies=movies)


@main.route('/add', methods=['POST'])
def add_movie():
    title = request.form.get('title')
    if title:
        if len(title) > 50:
            flash('Movie title must be less than 64 characters', 'danger')
            return redirect(url_for('main.home'))
        new_movie = Movie(title=title)
        db.session.add(new_movie)
        db.session.commit()
        flash('Movie added to the queue!', 'success')
    return redirect(url_for('main.home'))


@main.route('/watched', methods=['GET', 'POST'])
def watched_movies():
    """Page displaying watched movies and allowing manual additions for admins."""
    if request.method == 'POST':
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to add movies to the watched list.', 'danger')
            return redirect(url_for('main.watched_movies'))

        title = request.form.get('title')
        if title:
            new_movie = Movie(title=title, in_queue=False, watched=True)
            db.session.add(new_movie)
            db.session.commit()
            flash('Movie added to the watched list!', 'success')
        else:
            flash('Please enter a movie title.', 'danger')
        return redirect(url_for('main.watched_movies'))

    movies = Movie.query.filter_by(watched=True).all()
    return render_template('watched.html', movies=movies)


@main.route('/mark_watched/<int:movie_id>')
@login_required
def mark_watched(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if current_user.is_admin:
        movie.in_queue = False
        movie.watched = True
        db.session.commit()
        flash('Movie marked as watched!', 'success')
    return redirect(url_for('main.home'))


@main.route('/delete_movie/<int:movie_id>')
@login_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if current_user.is_admin:
        db.session.delete(movie)
        db.session.commit()
        flash('Movie has been deleted', 'success')
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
