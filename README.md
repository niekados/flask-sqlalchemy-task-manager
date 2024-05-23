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

## Creating Database

- We'll start by creating a new file called `models.py` within our taskmanager package.
- Since we will be defining the database, we obviously need to `import db` from the main taskmanager package.
For the purposes of these videos, we will be creating two separate tables, which will
be represented by class-based models using SQLAlchemy's ORM.
    - The first table will be for various categories, so let's call this class 'Category', which
will use the declarative base from SQLAlchemy's model.
    - The second table will be for each task created, so we'll call this class 'Task', also using the default db.Model.
-We want each of these tables to have a unique ID, acting as our primary key, so let's create
a new column variable of 'id' for both of these tables.
These will be columns on our tables, and each will be Integers, with primary_key set to
True, which will auto-increment each new record added to the database.
```python
# models.py
from taskmanager import db

class Category(db.Model):
    # schema for the Category model
    id = db.Column(db.Integer, primary_key=True)



class Task(db.Model):
    # schema for the Task model
    id = db.Column(db.Integer, primary_key=True)
```
---
**NOTE**

If you recall from the last few lessons, we had to specifically import each column type at the top of the file.
However, with `Flask-SQLAlchemy`, the '`db`' variable contains each of those already, and we can
simply use dot-notation to specify the data-type for our columns.

--- 

- For each model, we also need to create a function called `__repr__` that takes itself as the argument,
similar to the '`this`' keyword in JavaScript.
This is a standard Python function meaning '`represent`’, which means to represent the class objects as a string.
Another function that you might see out there, is the `__str__` function that behaves quite
similar, and either should be suitable to use.
```python
    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        # there is another function that behaves simillar - def __str__(self):
        return self
```
For now, let's just return self for those, but we'll come back to these momentarily.
- Within our Category table, let's add a new column of 'category_name', which will be set to a standard db.Column().
This will be the type of 'string', with a maximum character count of 25, but you can
make these larger or smaller if needed.
We also want to make sure each new Category being added to the database is unique, so we'll set that to True.
Then, we also need to make sure it's not empty or blank, so by setting nullable=False this
enforces that it's a required field.
` category_name = db.Column(db.String(25), unique=True, nullable=False)`
Now that we have a category_name, we can simply return self.category_name in our function.
- For our Task table, we'll add a new column of 'task_name', which will also be a standard db.Column().
This will also be the type of 'string', with a maximum character count of 50, which should
also be unique for each record, and required, so nullable=False.
- Then, we'll create a new column for 'task_description', and this time we'll use db.Text instead of
string, which allows longer strings to be used, similar to textareas versus inputs.
- Next, we'll create a new column for 'is_urgent', but this will be a Boolean field, with a default
set to False, and nullable=False.
- Then, the next column will be 'due_date', and this data-type will be db.Date with nullable=False,
but if you need to include time on your database, then db.DateTime or db.Time are suitable.
*By the way, you can see a full list of column and data types from the SQLAlchemy docs, which
include Integer, Float, Text, String, Date, Boolean, etc.*
- The final column we need for our tasks is a foreign key pointing to the specific category, which will be our category_id.
This will use db.Integer of course, and for the data-type we need to use db.ForeignKey
so our database recognizes the relationship between our tables, which will also be nullable=False.
**The value of this foreign key will point to the ID from our Category class, and therefore
we need to use lowercase '`category.id`' in quotes.**
In addition to this, we are going to apply something `called ondelete="CASCADE"` for this foreign key.
Since each of our tasks need a category selected, this is what's known as a one-to-many relationship.

---
**NOTE**

One category can be applied to many different tasks, but one task cannot have many categories.
If we were to apply many categories to a single task, this would be known as a many-to-many relationship.
Let's assume that we have 10 tasks on our database, and 2 categories, with these two
categories being assigned to 5 tasks each.
Later, we decide to delete 1 of those categories, so any of the 5 tasks that have this specific
category linked as a foreign key, will throw an error, since this ID is no longer available.
This is where the ondelete="CASCADE" comes into play, and essentially means that once
a category is deleted, it will perform a cascading effect and also delete any task linked to it.
If these aren't deleted, and a task contains an invalid foreign key, then you will get errors.

---

- In order to properly link our foreign key and cascade deletion, we need to add one more field to the Category table.
We'll call this variable 'tasks' plural, not to be confused with the main Task class, and
for this one, we need to use db.relationship instead of db.Column.
Since we aren't using db.Column, this will not be visible on the database itself like
the other columns, as it's just to reference the one-to-many relationship.
To link them, we need to specify which table is being targeted, which is "Task" in quotes.
Then, we need to use something called 'backref' which establishes a bidirectional relationship
in this one-to-many connection, meaning it sort of reverses and becomes many-to-one.
It needs to back-reference itself, but in quotes and lowercase, so backref="category".
Also, it needs to have the 'cascade' parameter set to 'all, delete' which means it will find
all related tasks and delete them.
The last parameter here is lazy=True, which means that when we query the database for
categories, it can simultaneously identify any task linked to the categories.
```python
class Category(db.Model):
    # schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)
```
- The final thing that we need to do with our class-based models, is to return some sort of string for the Task class.
We could simply return self.task_name, but instead, let's utilize some of Python's formatting to include different columns.
We'll use placeholders of {0}, {1}, and {2}, and then the Python .format() method to specify
that these equate to self.id, self.task_name, and self.is_urgent.
Alternatively, you could use `f"{strings}"`. -> `return f"#{self.id} - Task:{self.task_name} | Urgent: {self.is_urgent}"`
- Let's return back to our routes.py file now.
At the top of the routes, we need to import these classes in order to generate our database next.
```python
from taskmanager.models import Category, Task
```

---
**NOTE** 

If you recall from our environment variables, we've specified that our database will be
called 'taskmanager', not to be confused with our 'taskmanager' Python package.
This would be similar to the 'chinook' database we created in the previous lessons, so we
will need to also create this 'taskmanager' database.

---

- Let's navigate to the Terminal, and login to the Postgres CLI by typing 'psql' and hitting enter.
- To create the database, we can simply type:
`CREATE DATABASE taskmanager;`
- Once that's created, we'll switch over to that connection by typing:
`\c taskmanager;`
- We don't need to do anything else within the Postgres CLI now that we have the database
created, so let's come out of the CLI by typing `\q`.
- Next, we need to use Python to generate and migrate our models into this new database.
This will take the models that we've created for Category and Task, and build the database
schema using the details we've provided.

---
**NOTE**

It's important to note, that if you were to modify your models later, then you'll need
to migrate these changes each time the file is updated with new context.
For example, if you added a new column on the Task table for 'task_owner', once the
file is saved, you'll need to make your migrations once again, so the database knows about these changes.

---

---
**IMPORTANT**

- Let's go ahead and access the Python interpreter by typing "`python3`" and enter.
- From here, we need to import our '`db`' variable found within the taskmanager package, so type:
`from taskmanager import db`
- Now, using db, we need to perform the `.create_all()` method -> `db.create_all()`
- That's it, pretty simple enough, our Postgres database should be populated with these two
tables and their respective columns and relationships.
- Let's exit the Python interpreter by typing exit().
```terminal
<!-- In terminal python3 interpreter type these: -->

<!-- # 1 -->
from taskmanager import db

<!-- # 2 -->
db.create_all()

<!-- # 3 -->
exit()
```

---

Congratulations, you now have your database models and schema migrated into the database.
You should go ahead and push your changes to GitHub now for version control.
However, if you'd like to confirm that these tables exist within your database, then follow
these instructions listed on the screen.

```terminal

psql -d taskmanager

\dt
```

## Template Inheritance

When using a templating language such as Flask, any assets that we use such as images, CSS,
and JavaScript, need to be stored in a directory called '`static`' and we'll also want to add the css/
and js/ folders within this static directory.

Now, in order to link to any static file that we have, it's important to note that we must use the correct syntax.
`<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">`

---
**NOTE**

Also, quite often when working with a templating language, if you make changes to your CSS
or JavaScript files, and then reload the page, it might not show your changes.
This is very likely an issue to do with caching, so here are three steps to always remember to check.
- First, try a hard-reload, which is generally CTRL+SHIFT+R in most cases, but depending
on your computer and which browser you use, it could be one of these combinations on screen.
- Second, if that doesn't work, open a new Incognito window with your project URL, and if you do
see the changes, it's certainly a caching issue, since Incognito doesn't store cache.
- Finally, if neither of those options work, stop the application in your terminal from
running, and just restart it.
This may sound asinine, but quite often with Flask and Django, a fresh restart of the app
is required to take effect of any new additions to your code.

---

### Materilize

we need to initialise materialise sidenav.
just get the snippet code from materialize website under the Initialization section and paste it in script.js
```js
  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, options);
  });
  ```
  and we customize it like this for our project 
  ```js
  document.addEventListener('DOMContentLoaded', function() {
    // sidenav initialization
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
  });
  ```
  
  ## Adding Categories

  ### routes.py

  Let's return to the `route.py` file, and now we can add the `POST` method functionality for
users to add a new category to the database.
If the requested method is equal to POST, then we will create a new variable called
'`category`', which will be set to a new instance of the `Category()` model imported at the top of the file.
By using the '`request`' method, we need to also import that from Flask at the top here.
We need to make sure that this Category model uses the same exact keys that the model is
expecting, so when in doubt, copy from the model directly.
For this category_name field, we can then use the `request` form being posted to retrieve the name-attribute.
This is why it's important to keep the naming convention consistent, which means our name-attribute
matches that of our database model.
Once we've grabbed the form data, we can then '`add`' and '`commit`' this information to the
SQLAlchemy database variable of '`db`' imported at the top of the file.
This will use the database `sessionmaker` instance that we learned about in some of the previous videos.
After the form gets submitted, and we're adding and committing the new data to our database,
we could redirect the user back to the '`categories`' page.
We'll need to import the '`redirect`' and '`url_for`' classes at the top of the file from our flask import.
That completes our function, so let's quickly recap what's happening here.
When a user clicks the "Add Category" button, this will use the "GET" method and render the 'add_category' template.
Once they submit the form, this will call the same function, but will check if the request
being made is a “POST“ method, which posts data somewhere, such as a database.
Anything that needs to be handled by the POST method, should be indented properly within this condition.
By default, the normal method is GET, so it will behave as the 'else' condition since
it's not part of the indented POST block.
If you wanted to, technically you could separate this into two separate functions, which would
handle the GET and POST methods completely apart.
Also, in a real-world scenario in a production environment, you'd probably want to consider
adding defensive programming to handle brute-force attacks, along with some error handling.

```python
# routes.py
from flask import render_template, request, redirect, url_for


# we used GET and POST methods, as we will be submitting form to database
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")
```



