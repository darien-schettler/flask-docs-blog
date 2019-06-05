<h2>Flask Docs Blog Tutorial</h2>
<h4>With Bootstrap and Extensive Commenting</h4>
<hr>
<h3>What Is It?</h3>
<p> A basic blog application called Flaskr. Users will be able to register, log in, create posts, and edit or delete their own posts. You will be able to package and install the application on other computers.</p>
<hr>
<h3>Things to Add in the Future</h3>
<ol>
<li>A detail view to show a single post. Click a post’s title to go to its page</li>
<li>Like / unlike a post.</li>
<li>Comments.</li>
<li>Tags</li>
<li>Clicking a tag shows all the posts with that tag</li>
<li>A search box that filters the index page by name</li>
<li>Paged display. Only show 5 posts per page</li>
<li>Upload an image to go along with a post</li>
<li>Format posts using Markdown</li>
<li>An RSS feed of new posts</li>
</ol>
<hr>
<h3>Command To Run Using Wheel For Deployment</h3>
<p>pip install flaskr-1.0.0-py3-none-any.whl</p>
<hr>
<h3>Final Notes On Deployment From Flask Docs</h3>
<p>
<strong>Configure the Secret Key</strong><br>
Your secret key should be a string of random bytes and not an easily guessable string

You can use the following command to output a random secret key:

- python -c 'import os; print(os.urandom(16))'

b'_5#y2L"F4Q8z\n\xec]/'<br><br>
Create the config.py file in the instance folder, which the factory will read from if it exists. Copy the generated value into it.

- venv/var/flaskr-instance/config.py<br>
- SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'<br><br>
You can also set any other necessary configuration here, although SECRET_KEY is the only one needed for Flaskr.

<strong>Run with a Production Server</strong><br>
When running publicly rather than in development, you should not use the built-in development server (flask run).<br>
The development server is provided by Werkzeug for convenience, but is not designed to be particularly efficient, stable, or secure.

<strong>Instead, use a production WSGI server.</strong><br><br>
For example, to use Waitress, first install it in the virtual environment:

- pip install waitress<br><br>
You need to tell Waitress about your application, but it doesn’t use FLASK_APP like flask run does. You need to tell it to import and call the application factory to get an application object.

- waitress-serve --call 'flaskr:create_app'

Serving on http://0.0.0.0:8080</p>