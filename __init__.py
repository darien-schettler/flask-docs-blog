# Import the os package so we can interact better with the ecosystem of files/folders on host computer
import os

# First we imported the Flask class
# An instance of this class will be our WSGI (Web Server Gateway Interface )application 
from flask import Flask

# --------------------------------------- FILE OVERVIEW ------------------------------------------------
#
#   The __init__.py serves double duty: 
#
#           1. It will contain the application factory
#                   - Instead of creating a Flask instance globally, you will create it inside a function. 
#                   - This function is known as the application factory
#                   - Any config/registration/other-setup the app needs will happen inside the function
#                   - THEN the application will be returned.
#
#           2. It tells Python that the flaskr directory should be treated as a package.
#
# ------------------------------------------------------------------------------------------------------


def create_app(test_config=None):
    #  We create an instance of the Flask class -- Lets look at the passed arguments
    #
    #       1.  __name__ 
    #               - Is the name of the current Python module. 
    #               - The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.
    #
    #       2.  instance_relative_config=True 
    #               - Tells the app that configuration files are relative to the instance folder
    #               - The instance folder is located outside the hello-world-flask package
    #               - The instance folder can hold local data that shouldn’t be committed to version control (db/config/secrets)
    app = Flask(__name__, instance_relative_config=True)

    #  Next we set some default configuration that the app will use -- Let's look at the passed arguments
    #
    #       1.  SECRET_KEY='dev'
    #               - Is used by Flask and extensions to keep data safe
    #               - It’s set to 'dev' to provide a convenient value during development
    #               - This value should be overridden with a random value when deploying
    #
    #       2.  DATABASE=os.path.join(app.instance_path, 'hello-world-flask.sqlite'),
    #               - Is the path where the SQLite database file will be saved
    #               - It’s under app.instance_path, which is the path that Flask has chosen for the instance folder.
    #               - You’ll learn more about the database in the next section.
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'hello-world-flask.sqlite'),
    )

    if test_config is None:
        #  Next we allow for overriding of the default configuration
        #  We take values from the config.py file in the instance folder if it exists
        #  For example, when deploying, this can be used to set a real SECRET_KEY
        app.config.from_pyfile('config.py', silent=True)
    else:
        # test_config can also be passed to the factory, and will be used instead of the instance configuration
        #       -   This is so the tests you’ll write later in the tutorial can be configured independently of any development 
        #           values you have configured.
        app.config.from_mapping(test_config)

    # Next we ensure that app.instance_path exists
    #   -   Flask doesn’t create the instance folder automatically, but it needs to be 
    #       created because your project will create the SQLite database file there.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app