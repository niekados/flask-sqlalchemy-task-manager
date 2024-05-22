## Installation

- `pip3 install 'Flask-SQLAlchemy<3' psycopg2 sqlalchemy==1.4.46`

- Next, we will be storing some sensitive data, and we need to hide them using environment
variables hidden within a new file called '`env.py`'.
Make sure to have a `.gitignore` file that contains any files and folders which should be ignored by GitHub, such as an `env.py` file.

```python
# env.py
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "any_secret_key")
os.environ.setdefault("DEBUG", "True") # make sure to set it to False for final project
os.environ.setdefault("DEVELOPMENT", "True")
os.environ.setdefault("DB_URL", "postgresql:///taskmanager")
```
- Next, the entire application will need to be its own Python package, so to make this
a package, we need a new folder which we will simply call `taskmanager/`.
Inside of that, a new file called `__init__.py`
This will make sure to initialize our taskmanager application as a package, allowing us to use
our own imports, as well as any standard imports.

- We will start by importing the following:
`import os from flask import Flask`
`from flask_sqlalchemy import SQLAlchemy`
In order to actually use any of our hidden environment variables, we need to import the '`env`' package.
However, since we are not pushing the `env.py` file to GitHub, this file will not be visible
once deployed to Heroku, and will throw an error.
This is why we need to only import '`env`' if the OS can find an existing file path for the `env.py` file itself.
Now we can create an instance of the imported `Flask()` class, and that will be stored in
a variable called '`app`', which takes the default Flask `__name__` module.
Then, we need to specify two app configuration variables, and these will both come from our environment variables.
app.config SECRET_KEY and app.config SQLALCHEMY_DATABASE_URI, both wrapped in square brackets and quotes.
Each of these will be set to get their respective environment variable, which is SECRET_KEY,
and the short and sweet DB_URL for the database location which we'll set up later.
Then, we need to create an instance of the imported SQLAlchemy() class, which will be
assigned to a variable of 'db', and set to the instance of our Flask 'app'.
Finally, from our taskmanager package, we will be importing a file called 'routes' which we'll create momentarily.

--- 
**NOTE**

Once you save the file, you'll notice we have a couple linting issues.
First, it says that we've imported 'env', but it's unused.
It's also complaining about our custom import not being added at the top of the file with the other imports.
The reason this is being imported last, is because the 'routes' file, that we're about
to create, will rely on using both the 'app' and 'db' variables defined above.
If we try to import routes before 'app' and 'db' are defined, then we'll get circular-import
errors, meaning those variables aren't yet available to use, as they're defined after the routes.
These linting warnings are technically not accurate, so to stop the warnings, we can
add a comment at the end of each line, # noqa for 'No Quality Assurance'.

---

```python
# taskmanager/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
if os.path.exists("env.py"):
    import env # noqa


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.comfig["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")

db = SQLAlchemy(app)

from taskmanager import routes # noqa
```

- Now we can create the new '`routes.py`' file within our taskmanager package.
We're going to start using some Flask functionality, so we can `import render_template from flask` to start with.
Then, from our main taskmanager package, let's `import` both '`app`' and '`db`'.
For simplicity to get the app running, we'll create a basic app route using the root-level directory of slash.
This will be used to target a function called 'home', which will just return the rendered_template
of "`base.html`" that we will create shortly.

```python
# taskmanager/routes.py
from flask import render_template
from taskmanager import app, db

@app.route("/")
def home():
    return render_template("base.html")
```

- create the main Python file that will actually run the entire application.
This will be at the root level of our workspace, not part of the taskmanager package itself.
Since it will run the whole application, let's just call it `run.py` in that case.
We need to import os once again, in order to utilize environment variables within this file.
We also need to import the '`app`' variable that we've created within our taskmanager
package, defined in the init file.
The last step to run our application is to tell our app how and where to run the application.
This is the same process we've seen before, checking that the 'name' class is equal to
the default 'main' string, wrapped in double underscores.
If it's a match, then we need to have our app running, which will take three arguments:
'host', 'port', and 'debug'.
Each of these, as you may recall, are stored in the environment variables, so we need to
use os.environ.get().
The host is the IP, the port is obviously PORT, but that needs to be converted into
an integer, and then debug is of course DEBUG.

```python
# run.py
import os
from taskmanager import app


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG")
    )
```
- Finally, we need to render some sort of front-end template to verify that the application is running successfully.
Within our taskmanager package, let's create a new directory called '`templates`', which
is where Flask looks for any HTML templates to be rendered.
- Then, within this templates directory, we will create a new file called `base.html`, which
is what will be rendered from our routes.py file.
