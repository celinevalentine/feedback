from app import app
from models import db, connect_db, User

db.drop_all()
db.create_all()

u1 = User(
    username="christopher",
    password="123456",
    email="123@gmail.com",
    first_name="christopher",
    last_name="tutorking"
)

u2 = User(
    username="william",
    password="123456",
    email="234@gmail.com",
    first_name="william",
    last_name="throneholder"
)

db.session.add_all([u1,u2])
db.session.commit()