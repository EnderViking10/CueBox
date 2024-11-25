from app import create_app, db
from app.models import User
from getpass import getpass
from werkzeug.security import generate_password_hash
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


if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
