from flask import Flask, redirect, flash, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "so-secret"
 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def homepage():
    """Register user: produce form and handle form submission."""
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    """register a user: show form and handle form submission"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        return redirect('/secret')
    else:
        return render_template('register.html', form=form)
        
@app.route('/login',methods=["GET", "POST"])
def login():
    """login a use: show the and handle form submission"""
    form = LoginForm

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.anthenticate(username, password)
        if user:
            session["username"]=user.username
            return redirect('/secret')
        else:
            form.username.errors = ["incorrect username/password"]
    return render_template("login.html",form=form)
