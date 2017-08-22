from __init__ import site,db,lm
from flask import Response, redirect, url_for, request, session, abort,render_template,flash,g
#from forms import LoginForm DEPRECATED
from models import User
from flask_login import login_user, logout_user, current_user, login_required, login_manager
import config
@site.before_request
def before_request():
    g.user=current_user


@site.route('/')
def index():
    return render_template("index.html",user=current_user)
@site.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@site.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')#TODO:Redirect to index


# handle login failed
@site.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

@site.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')#TODO:Create register template
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return 'User successfully registered'
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))