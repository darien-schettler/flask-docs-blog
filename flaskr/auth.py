import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

#  	-- Blueprint() --
#       -->	    This creates a Blueprint named 'auth'.
#       -->     Like the application object, the blueprint needs to know where it’s defined,
#               so __name__ is passed as the second argument.
#       -->     The url_prefix will be prepended to all the URLs associated with the blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')


#   -- THE FIRST VIEW : REGISTER
#       -->     When the user visits /auth/register, the view will return HTML with a form for them to fill out. [GET]
#       -->     When they submit the form, it will validate their input and either show the form
#               again with an error message or create the new user and go to the login page. [PUT]
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # Step 1 : Retrieve submitted username & password
        username = request.form['username']
        password = request.form['password']

        # Step 2 : Access the database connection (for the future) and define the error status as None (to start)
        db = get_db()
        error = None

        # Step 3 : Perform validation on username and password fields (verify something was passed & user is unique)
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        # Step 4a : If no validation errors than create an entry in the user table with username and password (hashed)
        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                       (username, generate_password_hash(password)))
            db.commit()

            # Step 5 : redirect to the login screen on successful validation and db update
            return redirect(url_for('auth.login'))

        # Step 4b : If there WAS validation errors pass them through to the user (if there are none they won't appear)
        flash(error)

    # If it was a GET request (i.e. going to the page via a link) than we will simply return the register html page
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        # Step 1 : Get user input for username and password and setup connection to db and init error array to None
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # Step 2 : Verify that the user exists
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # Step 3a : If the user does not exist or the user's password is wrong add those errors to the error array
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # Step 3b : If the user DOES exist AND the user's password is correct we set the session and redirect to home
        if error is None:
            #   -- session --
            #       -->     A dict that stores data across requests.
            #       -->     When validation succeeds, the user’s id is stored in a new session.
            #       -->     The data is stored in a cookie that is sent to the browser, and the browser then sends it
            #               back with subsequent requests.
            #       -->     Flask securely signs the data so that it can’t be tampered with.
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested.
#
# load_logged_in_user checks if a user id is stored in the session and gets that user’s data from the database,
# storing it on g.user, which lasts for the length of the request.
#
# If there is no user id, or if the id doesn’t exist, g.user will be None.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()


# To log out, you need to remove the user id from the session.
# Then load_logged_in_user won’t load a user on subsequent requests.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# This decorator returns a new view function that wraps the original view it’s applied to
# The new function checks if a user is loaded and redirects to the login page otherwise.
# If a user is loaded the original view is called and continues normally.
def login_required(view):
    @functools.wraps(view)
    def decorated_view(*args, **kwargs):

        if g.user is None:
            return redirect(url_for('auth.login'))
        else:
            return view(*args, **kwargs)

    return decorated_view