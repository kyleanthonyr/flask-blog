"""
Instead of creating a Flask instance globally, it will be created
inside of a function known as the application factory.

Any confiuguration, registration, and other setup the application
needs will be done inside the function. 

Finally, the function will return the Flask application instance.

"""

import os
from flask import Flask

def create_app(test_config=None):
    """
    This function creates and configures a Flask app and returns
    an instance of it.
    """
    app = Flask(__name__, instance_relative_config=True) # creates the Flask instance
    
    # sets some default configuration the app will use
    app.config.from_mapping(
        SECRET_KEY="freemason-slinky-basin-grill",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        """
        The following line overrides the default config from above with
        values taken from the config.py file in the instance folder, if
        it exists.

        test_config can also be passed directly to the factory and will
        be used instead of the instance configuration. (useful for tests)
        """
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # return a simple page that says hello to test
    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    return app
