from flask import Blueprint, render_template
import database

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route('/')
def showPosts():
    return render_template("posts.html", posts=database.getDbConn().posts.find())
