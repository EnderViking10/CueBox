from getpass import getpass
from sqlite3 import IntegrityError

import requests
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import User, Movie
from config import ProductionConfig

app = create_app(ProductionConfig)


# CLI command to initialize the database
@app.cli.command('initdb')
def initdb():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")


# CLI command to create an admin user
@app.cli.command('createadmin')
def createadmin():
    """Create an admin user."""
    username = input("Enter admin username: ")
    password = getpass("Enter admin password: ")
    if User.query.filter_by(username=username).first():
        print("Admin with this username already exists!")
        return
    admin = User(username=username, password=generate_password_hash(password), is_admin=True)
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user '{username}' created!")


# CLI command to update the imdb ids
@app.cli.command('get_imdb_id')
def get_imdb_id():
    """Get the imdb ids."""
    movies = Movie.query.filter_by(watched=True).all()

    for movie in movies:
        api_call = f"https://www.omdbapi.com/?t={url_movie_title}&apikey={app.Config.OMDB_API_KEY}"
        response = requests.get(api_call)

        data = None
        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()

        movie.imdb_id = data["imdbID"]



    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Rollback the transaction
        print(IntegrityError)


if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
