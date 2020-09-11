from flask import Flask, redirect, flash, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized

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

@app.errorhandler(404)
def page_not_found(e):
    """show 404 NOT found page"""
    return render_template('404.html'), 404


@app.route('/register', methods=["GET", "POST"])
def register():
    """register a user: show form and handle form submission"""
    if "username" in session:
        return redirect(f'/users/{session["username"]}')

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

       
        db.session.commit()

        session['username']=user.username
        return redirect(f'/users/{user.username}')
    else:
        return render_template('users/register.html', form=form)
        
@app.route('/login',methods=["GET", "POST"])
def login():
    """login a use: show the and handle form submission"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session["username"]=user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["incorrect username/password"]
            return render_template("users/login.html",form=form)
    return render_template("users/login.html",form=form)

@app.route('/users/<username>')
def show_user(username):
    """show user info"""
    
    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()
    
    return render_template('/users/show.html', user=user, form=form)

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect('/login')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """delete a user"""
    
    if "username" not in session or username != session["username"]:
        raise Unauthorized() 
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
   

    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """add feedback to a user"""
    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        feedback = Feedback(
            title=title,
            content=content,
            username=username
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect (f'/users/{feedback.username}')
    else:
        return render_template('feedback/new.html', form=form)




@app.route('/feedback/<int:id>/update', methods=["GET", "POST"])
def update_feedback(id):
    """update feedback to a user"""
    feedback = Feedback.query.get(id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()
    
    form = FeedbackForm(obj=feedback)
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        db.session.commit()
        
        return redirect (f'/users/{feedback.username}')
    else:
        return render_template('feedback/edit.html', feedback=feedback, form=form)


@app.route('/feedback/<int:id>/delete', methods=["POST"])
def delete_feedback(id):
    """delete feedback to a user"""
    feedback = Feedback.query.get(id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()
    
    form = DeleteForm()
    
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
        
    return redirect (f'/users/{feedback.username}')
 