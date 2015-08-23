from flask import Flask, render_template

import pymongo

# Create flask application
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def showPosts():
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

    # Render template with posts.
    print("Will render posts now.")
    return render_template("posts.html", posts=posts)

if __name__ == "__main__":
    app.run()
