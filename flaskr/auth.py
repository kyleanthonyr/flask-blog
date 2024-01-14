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

# this creates a Blueprint named auth that preprends /auth to all URLs associated
bp = Blueprint('auth', __name__, url_prefix='/auth')