from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    
    db.app = app
    db.init_app(app)

class User(db.Model):
    """user model"""
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
@classmethod
def register(cls, username, password, email, first_name, last_name):
    """Reigster user w/hashed password and return user."""
    hashed = bcrypt.generate_password_hash(password)
    hashed_utf8 = hashed.decode("utf8")
    user = cls(
        username=username,
        password=hashed_utf8,
        email=email,
        first_name=first_name,
        last_name=last_name
        
    )
    db.session.add(user)
    return user


@classmethod
def authenticate(cls,username,password):
    """validate that user exisits and password is correct"""

    user= User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password,password):
        return user
    else:
        return False
