from flask import Flask, render_template, redirect, url_for, request, session, \
    flash

import controller.admin
import controller.blog
import controller.user

# Create flask application
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "Secret"

app.register_blueprint(controller.admin.admin)
app.register_blueprint(controller.blog.blog)
app.register_blueprint(controller.user.user)

if __name__ == "__main__":
    app.run()
