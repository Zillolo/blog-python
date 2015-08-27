from flask import Blueprint, session, redirect, url_for, request, render_template, flash

from model import form
from model import user

from util import database

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/user')
def default():
    pass

@user.route('/user/register', methods = ['GET', 'POST'])
def register():
    # Check if the user is already logged in. In that case redirect him to the
    # default page for the user module.
    if isLoggedIn():
        flash('You are already logged in.')
        return redirect(url_for('user.default'))

    form = forms.RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = User(form.firstName.data, form.lastName.data, form.username.data,
             form.email.data, form.password.data)

            db = database.getDbConn('blog')
            user.addTo(db.users)

            flash('You have been successfully registered.')
            return redirect(url_for('user.login'))

    # If the form was not yet submitted or was not valid, show the form to the user.
    return render_template('user/registration.html')

@user.route('/user/login', methods = ['GET', 'POST'])
def login():
    if isLoggedIn():
            return redirect(url_for('blog.default'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != "Test" or request.form['password'] != "Password":
            error = "Invalid username or password."
        else:
            session['loggedIn'] = True
            session['username'] = "Anna"
            session['profilePicPath'] = url_for('static', filename='userimg/anna.jpg')
            flash('You were logged in.')
            return redirect(url_for('blog.default'))
    return render_template('login.html', error=error)

@user.route('/user/logout')
def logout():
    session.pop('loggedIn', None)
    session.pop('username', None)
    session.pop('profilePicPath', None)
    flash('You were logged out.')
    return redirect(url_for("blog.default"))

def isLoggedIn():
    return session.get('loggedIn')
