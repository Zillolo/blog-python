from flask import Blueprint, session, redirect, url_for, request, render_template, flash

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/login', methods = ['GET', 'POST'])
def login():
    if isAuthorized():
            return redirect(url_for('blog.default'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != "Test" or request.form['password'] != "Password":
            error = "Invalid username or password."
        else:
            session['loggedIn'] = True
            flash('You were logged in.')
            return redirect(url_for('blog.default'))
    return render_template('login.html', error=error)

@user.route('/logout')
def logout():
    session.pop('loggedIn', None)
    flash('You were logged out.')
    return redirect(url_for("blog.default"))

def isAuthorized():
    return session.get('loggedIn')
