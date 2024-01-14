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
    

    # Creates a Login view that will redirect user to home page
    @bp.route('/login', methods=('GET', 'POST'))
    def login():

        # handle POST request
        if request.method == 'POST':

            # get username and password
            username = request.form['username']
            password = request.form['password']

            # get db connection
            db = get_db()
            error = None

            # validate username and password in the form
            if not username:
                error = "Please enter a valid username."
            elif not password:
                error = "Please enter a password."

            # search db for user
            user = db.execute(
                'SELECT * FROM user where username = ?', (username).fetchone()
            )

            # check that user exists in db
            if user is None:
                error = "Incorrect username."
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password'

            # store user id in session dict to be available for multiple requests
            if error is None:
                """
                session is a dict that stores data across requests. When validation succeeds,
                the user id is stored in a new session.
                Difference between g and session: https://stackoverflow.com/questions/32909851/flask-session-vs-g#:~:text=No%2C%20g,g%20is%20cleared.

                The data is stored in a cookie that is sent to the browser and the browser then
                sends it back with subsequent requests. 

                Flask securely signs the data so that it can't be tampered with.
                """
                session.clear()
                session['user_id'] = user['id']
                redirect(url_for('index'))


        # handle GET request
        return render_template('/auth/login.html')
    

    @bp.before_app_request
    def load_logged_in_user():
        """
        This function runs before the view function no matter the URL requested. 
        It checks if a user is logged in by checking if id is stored in session.
        It gets the user's data from the database, and stores it on g.user which will last for 
        the length of the request.

        If a user is not logged in, or the id doesn't exist, g.user will be set to None.
        """
        user_id = session.get('user_id') # get user id stored in session dict

        if user_id is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM user where id = ?', (user_id)
            ).fetchone()


@bp.route('/logout')
def logout():
    """
    To logout, the user id must be removed from session. And load_logged_in_user won't
    load a user on subsequent requests.
    """
    session.clear()
    return redirect(url_for('index'))

# Require authentication in other views
"""
Since creating, editing and deleting blog posts will require a user to be logged in,
a decorator can be used to check this for each view it is applied to.
"""
def login_required(view):
    """
    This decorator returns a new view function that wraps the original view it's applied to.
    The new view function checks if a user is loaded and redirects to the login page otherwise.
    If a user is loaded, the original view is called and continues normally.
    
    This decorator will be used for the blog views.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view