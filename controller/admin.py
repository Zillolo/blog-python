from bson.objectid import ObjectId
from flask import Blueprint, session, flash, redirect, url_for, render_template, request

import pymongo
from util import database

import controller.user

admin = Blueprint('admin', __name__, template_folder='templates')

"""
The default action for the admin module.
"""
@admin.route('/admin')
def default():
    return redirect(url_for('admin.showPosts'))

"""
TODO: Add documentation
"""
@admin.route("/admin/posts/view")
def showPosts():
    # If the user is not logged in show a message and redirect him to a non-admin site.
    if not controller.user.isLoggedIn():
        flash('You are not authorized to access this site.')
        return redirect(url_for('blog.default'))

    # Render the admin page and display all posts.
    return render_template("admin.html", posts=database.getDbConn('blog').posts.find())

"""
Adds a post.
"""
@admin.route('/admin/posts/add', methods = ['GET', 'POST'])
def addPost():
    # If the user is not logged in show a message and redirect him to a non-admin site.
    if not controller.user.isLoggedIn():
        flash('You are not authorized to access this site.')
        return redirect(url_for('blog.default'))

    # If the form was already submitted, validate it and, if valid, submit it.
    if request.method == "POST":
        # Validate the form. If there happens to be an error, the string 'error' will not be empty.
        #TODO: Validate this further.
        error = ""
        if not request.form['title']:
            error = "The title field may not be empty.\n"
        if not request.form['author']:
            error += "The author field may not be empty.\n"
        if not request.form['content']:
            error += "The content field may not be empty.\n"

        # If the validation fails we display the same template with the generated errors.
        if error:
            return render_template('posts/new.html', error=error)

        # Request a database connection and insert the validated post into the collection.
        db = database.getDbConn('blog')
        if db == None:
            flash('A connection to the database could not be established.')
            return render_template(url_for('admin.default'))

        collection = db.posts
        post = {'title' : request.form['title'], 'author' : request.form['author'], 'content' : request.form['content']}
        collection.insert_one(post)
        #TODO: Check if this never fails?

        flash('The post was added successfully.')
        return redirect(url_for('admin.default'))
    else:
        # If the form is not yet submitted, show the form and show no errors.
        return render_template('posts/new.html', error=None)

"""
Modifies a post.
"""
@admin.route('/admin/posts/modify', methods = ['GET', 'POST'])
def modifyPost():
    # If the user is not logged in show a message and redirect him to a non-admin site.
    if not controller.user.isLoggedIn():
        flash('You are not authorized to access this site.')
        return redirect(url_for('blog.default'))

    # Request a database connection.
    db = database.getDbConn('blog')
    if db == None:
        flash('A connection to the database could not be established.')
        return redirect(url_for('admin.default'))
    collection = db.posts

    # If the form was already submitted, validate it and then insert it.
    if request.method == 'POST':
        error = ""
        if not request.form['title']:
            error += "The title field may not be empty."
        if not request.form['author']:
            error += "The author field may not be empty."
        if not request.form['content']:
            error += "The content field may not be empty."

        if error:
            post = {'title' : request.form['title'], 'author' : request.form['author'], 'content' : request.form['content']}
            return render_template('posts/modify.html', post=post, error=error)

        # Insert the modified post into the collection.
        post = {'title' : request.form['title'], 'author' : request.form['author'], 'content' : request.form['content']}
        collection.update_one({'_id' : ObjectId(request.form['id'])}, { '$set' : post}, upsert = False)

        flash('The post was successfully changed.')
        return redirect(url_for('admin.default'))
    else:
        # If the form was not yet submitted, retrieve the original post and fill the form with it.
        post = collection.find_one({'_id' : ObjectId(request.args.get('id', ''))})
        if post == None:
            flash('No post with the specified id found.')
            return redirect(url_for('admin.default'))
        return render_template('posts/modify.html', post=post, error=None)

"""
Deletes a post.
"""
@admin.route('/admin/posts/delete')
def deletePost():
    # If the user is not logged in show a message and redirect him to a non-admin site.
    if not controller.user.isLoggedIn():
        flash('You are not authorized to access this site.')
        return redirect(url_for('showPosts'))

    # Get a db connection.
    db = database.getDbConn('blog')
    collection = db.posts

    # Remove the post with the id given as parameter from the collection.
    collection.remove({'_id' : ObjectId(request.args.get('id', ''))})

    # Flash a message of success and redirect to the admin panel.
    flash('The post was successfully removed.')
    return redirect(url_for('admin.default'))
