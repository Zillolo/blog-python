from flask import Flask, render_template, redirect, url_for, request, session, \
    flash

import admin
import blog
import user

# Create flask application
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "Gaggn"

app.register_blueprint(admin.admin)
app.register_blueprint(blog.blog)
app.register_blueprint(user.user)

if __name__ == "__main__":
    app.run()
