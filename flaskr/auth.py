"""
VIEWS
A view function is the code that responds to an incoming request to your application.
Flask uses patterns to match the incoming request URL to the view that should handle it.

The view returns data that Flask turns into an outgoing response. Flask can also go the
other direction and generate a URL to a view based on its name and arguments.

--------------------------------------------------------------------------------------

BLUEPRINTS
A blueprint is a way to organize a group of related views and other code. Instead of registering
these views and other code directly with the app, they are registered to the Blueprint.

The blueprint is then registered with the application when it is available in the factory func.
"""

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# BLUEPRINT
# this creates a Blueprint named auth that preprends /auth to all URLs associated
bp = Blueprint('auth', __name__, url_prefix='/auth')

# VIEWS

# Creates the Register view that will return a HTML form for them to fill out.
@bp.route('/register', methods=('GET','POST')) # associates the register URL with the register view func
def register():

    # validate user input if the user submits the form via POST request
    if request.method == 'POST':
        # Get username and password from request.form (a special type of dict containing form data)
        username = request.form['username']
        password = request.form['password']

        # get db connection if available
        db = get_db()
        error = None

        # Input validation for username and password
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # Insert new user in USER table for the db if no error and redirect to login page
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username password) VALUES (? ?)", (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError: # raises error if user exists already
                error = f"User {username} is already registered. Please login instead."
            else:
                return redirect(url_for("auth.login")) # redirects to login page if no error
            
        flash(error) # Flashes the error across the screen

        # return register template if GET request
        return render_template('auth/register.html')