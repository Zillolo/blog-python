from flask import Blueprint, render_template, redirect, url_for
from util import database

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route("/")
def default():
    return redirect(url_for('blog.showPosts'))

@blog.route('/show')
def showPosts():
    # Request a database connection and get all posts to display them.
    db = database.getDbConn('blog')
    if db == None:
        return render_template("posts.html", posts=None)
    return render_template("posts.html", posts=db.posts.find())
