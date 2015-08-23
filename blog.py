from flask import Flask, render_template, redirect, url_for, request, session, \
    flash

import pymongo

# Create flask application
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "Gaggn"

@app.route("/")
def showPosts():
    # Render template with posts.
    return render_template("posts.html", posts=getAllPosts())

@app.route("/admin")
def showAdmin():
    if session.get('loggedIn') == True:
        return render_template("admin.html", posts=getAllPosts())
    flash('You are not authorized to access this site.')
    return redirect(url_for('showPosts'))

@app.route("/admin/posts/add", methods=["POST", "GET"])
def addPost():
    if session.get('loggedIn') == True:
        if request.method == "POST":
            error = None
            if not request.form['title']:
                error = "The title field must be filled."
            elif not request.form['author']:
                error = "The author field must be filled."
            else:
                # Initialize a connection to the MongoDB.
                try:
                    conn = pymongo.MongoClient('localhost', 27017)
                    print("Connection to MongoDB was successful.")
                except pymongo.errors.ConnectionFailure as e:
                    print("Could not connect to MongoDB: %s" % e)
                    return # Well fuck.
                db = conn.blog
                collection = db.posts

                post = {'title' : request.form['title'], 'author' : request.form['author'], 'content' : request.form['content']}
                collection.insert(post)
                flash('Post was added successfully.')
                return redirect(url_for('showPosts'))
            return render_template('posts/new.html', error=error)
        else:
            return render_template('posts/new.html', error=None)
    flash('You are not authorized to access this site.')
    return redirect(url_for('showPosts'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('loggedIn') == True:
            return redirect(url_for('showPosts'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != "Test" or request.form['password'] != "Password":
            error = "Invalid username or password."
        else:
            session['loggedIn'] = True
            flash('You were logged in.')
            return redirect(url_for('showPosts'))
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session.pop('loggedIn', None)
    flash('You were logged out.')
    return redirect(url_for("showPosts"))

def getAllPosts():
    # Initialize a connection to the MongoDB.
    try:
        conn = pymongo.MongoClient('localhost', 27017)
        print("Connection to MongoDB was successful.")
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)
        return # Well fuck.
    db = conn.blog
    collection = db.posts

    # Read all posts from the database.
    posts = collection.find()
    return posts

if __name__ == "__main__":
    app.run()
