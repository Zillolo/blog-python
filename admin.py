from bson.objectid import ObjectId
from flask import Blueprint, session, flash, redirect, url_for, render_template, request

import pymongo
import database

admin = Blueprint('admin', __name__, template_folder='templates')

"""
Shows the admin panel if the user is logged in.
"""
@admin.route('/admin')
def showAdmin():
    if session.get('loggedIn') == True:
        return render_template("admin.html", posts=database.getDbConn().posts.find())
    flash('You are not authorized to access this site.')
    return redirect(url_for('blog.showPosts'))

"""
Adds a post.
"""
@admin.route('/admin/posts/add', methods = ['GET', 'POST'])
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
                return redirect(url_for('blog.showPosts'))
            return render_template('posts/new.html', error=error)
        else:
            return render_template('posts/new.html', error=None)
    flash('You are not authorized to access this site.')
    return redirect(url_for('blog.showPosts'))

"""
Modifies a post.
"""
@admin.route('/admin/posts/modify', methods = ['GET', 'POST'])
def modifyPost():
    if session.get('loggedIn') != True:
        flash('You are not authorized to access this site.')
        return redirect(url_for('blog.showPosts'))

    # Initialize a connection to the MongoDB.
    try:
        conn = pymongo.MongoClient('localhost', 27017)
        print("Connection to MongoDB was successful.")
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)
        return # Well fuck.
    db = conn.blog
    collection = db.posts

    if request.method == 'GET':
        print('GET called.')
        print(request.args.get('id'))
        post = collection.find_one({'_id' : ObjectId(request.args.get('id', ''))})
        if post == None:
            print('No post with id.')
            flash('No post with the specified id found.')
            return redirect(url_for('admin.showAdmin'))
        print('Show dat template.')
        return render_template('posts/modify.html', post=post, error=None)
    else:
        print('POST called.')
        error = None
        if not request.form['title']:
            error = "The title field must be filled."
        elif not request.form['author']:
            error = "The author field must be filled."
        else:
            print("Success.")
            post = {'title' : request.form['title'], 'author' : request.form['author'], 'content' : request.form['content']}
            collection.update_one({'_id' : ObjectId(request.form['id'])}, { '$set' : post}, upsert = False)
            flash('The post was successfully changed.')
            print("Redirecting now.")
            return redirect(url_for('blog.showPosts'))
        print("Something went wrong :/")
        post = {'title' : request.form['title'], 'author' : request.form['author'], 'content' : request.form['content']}
        return render_template('posts/modify.html', post=post, error=error)

"""
Deletes a post.
"""
@admin.route('/admin/posts/delete')
def deletePost():
    if session.get('loggedIn') != True:
        flash('You are not authorized to access this site.')
        return redirect(url_for('showPosts'))

    # Initialize a connection to the MongoDB.
    try:
        conn = pymongo.MongoClient('localhost', 27017)
        print("Connection to MongoDB was successful.")
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)
        return # Well fuck.
    db = conn.blog
    collection = db.posts

    collection.remove({'_id' : ObjectId(request.args.get('id', ''))})
    flash('The post was successfully removed.')
    return redirect(url_for('admin.showAdmin'))
