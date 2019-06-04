import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

# --------------------------------------- FILE OVERVIEW ------------------------------------------------
#
#   The application will use a SQLite database to store users and posts. 
#		--> 	Python comes with built-in support for SQLite in the sqlite3 module.
#		--> 	SQLite is convenient as it doesn’t require setting up a separate db server
#		--> 	However, if concurrent requests try to write to the database at the same time... 
#				they will slow down as each write happens sequentially. 
#		-->		Small applications won’t notice this type of slowdown but... be warned
#
#	The tutorial doesn’t go into detail about SQL. If you are not familiar with it, the SQLite docs describe the language.
#
#						------------ Connect to the Database ------------
#	The first thing to do when working with a database is to create a connection to it
#		-->		Any queries and operations are performed using the connection, which is closed after the work is finished.
#		--> 	In web applications this connection is typically tied to the request
#		-->		It is created at some point when handling a request, and closed before the response is sent.
#
#	SIDENOTE ABOUT *g*
#		--> 	g is a special object that is unique for each request
#		-->		It is used to store data that might be accessed by multiple functions during the request. 
#		-->		The connection is stored and reused instead of creating a new connection
#		--> 	i.e. Fn get_db() is called a 2nd time in the same request.)
#
# ------------------------------------------------------------------------------------------------------

def get_db():
    if 'db' not in g:
    	# 	-- sqlite3.connect() --
    	#			-->		Establishes a connection to the file pointed at by the DATABASE config key
    	#			--> 	This file doesn’t have to exist yet, and won’t until we initialize the db later.
        g.db = sqlite3.connect(
        	# 	-- current_app -- 
        	#		--> 	A special object that points to the Flask application handling the request
        	# 		--> 	Since we used an app factory, there is no app object for the rest of the code 
        	# 		-->		get_db() will be called when the application has been created and is handling a request
        	#				so current_app can be used
            current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES
        )
        #  	-- sqlite3.Row -- 
        #		-->		Tells the connection to return rows that behave like dicts
        #		-->		This creates the ability to access the columns by name
        g.db.row_factory = sqlite3.Row

    return g.db

# 	-- close_db --
#		-->		Checks if a connection was created by checking if g.db was set
#		-->		If the connection exists, it is closed
#		-->		Further down you will tell your application about the close_db function in the 
#				application factory so that it is called after each request
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# ------------------- FUNCTIONS TO RUN SQL COMMANDS FROM schema.sql ---------------------------
def init_db():
    
    #	-- get_db() --
    #		-->		Returns a db connection, which is used to execute the commands read from the file
    db = get_db()

    # 	-- open_resource() --
    #		-->		Opens a file relative to the app package
    #		-->		This is useful since we may not know where that location is when deploying the app later
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#  	-- click.command() --
#		-->		Defines a cmd-line command called init-db that calls 
#				the init_db fn and shows a success message to the user
@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database.')


# ---------------------------------------------- NOTE --------------------------------------------
#		The close_db and init_db_command functions need to be registered with the app instance
#		otherwise they won’t be used by the application. However, since you’re using a factory fn, 
#		that instance isn’t available when writing the functions. Instead, we write a fn that takes 
#		an application and does the registration.
# ----------------------------------------------------------------------------------------------------------

def init_app(app):
	#	-- app.teardown_appcontext() --
	#		-->		Tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
	
	#	-- app.cli.add_command() --
	#		-->		Adds a new command that can be called with the flask command   
    app.cli.add_command(init_db_command)



init_db_command()
