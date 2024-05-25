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

## Extracting data from db

Now, it's time to start building the code that will extract the data from within our
database, so let's head over to the `routes.py` file.
In the previous video, we added a temporary placeholder route, which allows us to pull
up the categories template itself.
All we need to do here now, is add some code to query the database so we can use that within our template.
First, let's define a new variable within the categories function, which will also be
called categories to keep things consistent.
We just need to query the 'Category' model that is imported at the top of the file from
our models.py file, and we can do that by simply typing:
Category.query.all()
Sometimes though, categories might be added at different times, so this would have the
default method of sorting by the primary key when things get added.
Let's go ahead and use the .order_by() method, and have it sort by the key of 'category_name'.
We also need to make sure that we tell it the specific model as well, even though it
might seem redundant, it's possible to use other sorting methods.
You need to make sure the quantifier, which is .all() in this case, is at the end of the
query, after the .order_by() method.
Whenever we call this function by clicking the navbar link for Categories, it will query
the database and retrieve all records from this table, then sort them by the category name.
Now, all that's left to do here is to pass this variable into our rendered template,
so that we can use this data to display everything to our users.
By using the .all() method, this is actually what's known as a Cursor Object, which is
quite similar to an array or list of records.
Even if the result comes back with a single record, it's still considered a Cursor Object,
and sometimes Cursor Objects can be confusing when using them on front-end templates.
Thankfully, there's a simple Python method that can easily convert this Cursor Object
into a standard Python list, by wrapping the variable inside of 'list()'.
You might be slightly confused as to what 'categories=categories' represents, so let's quickly explain this part.
The first declaration of 'categories' is the variable name that we can now use within the HTML template.
The second 'categories', which is now a list(), is the variable defined within our function
above, which is why, once again, it's important to keep your naming convention quite similar.

```python
# routes.py
@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories) # categories=categories explained:
# The first declaration of 'categories' is the variable name that we can now use within the HTML template.
# The second 'categories', which is now a list(), is the variable defined within our function
```

Perfect, now that we have this template variable available to us, let's go back to our categories.html
template, and start incorporating it into our cards.
Eventually, we are going to have more than one category listed here, but so far we've
only added the single category of 'Travel'.
However, let's prepare the code to recognize multiple cards, by using the Jinja syntax of a for-loop.
We don't want each card to stack on top of each other, but instead, to flow within the
same row, each having their own column.
Make sure to add the for-loop just inside of the row, so everything within the row is repeated and looped.
The closing {% endfor %} should be just after the div for this column, so follow that down,
and add the closing element there.
Similar to JavaScript, we need to define a new index for each iteration of this loop,
so to keep things consistent, we will call ours 'category'.
This means that for each 'category' in the ‘list of categories' being passed over from
our Python function, it will generate a new column and card.
Finally, we need to display the actual category name that's stored within our database, so
we can update the card-title.
Since we are within a for-loop, we need to use the newly defined index variable of 'category'.
We also need to use dot-notation and tell it which key should be printed here, so in
this case, it should be 'category.category_name', which means, “this category’s key of category_name”.
If you wanted to show the primary key instead, that's stored within our database as 'id',
so it would be 'category.id' for example.
```html
<!-- categories.html -->
<div class="row">
    {% for category in categories %}
    <div class="col s12 m6 l3">
      <div class="card light-blue darken-4 center-align">
        <div class="card-content white-text">
          <span class="card-title">{{ category.category_name }}</span>

        </div>
        <div class="card-action">
          <a href="#" class="btn green accent-4">Edit</a>
          <a href="#" class="btn red ">Delete</a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
```

## Edit Category

Let's go over to the `routes.py` file, and we are going to create a new function.
For the app route URL, let's call this "/edit_category", and once again, we will be using this as a
dual-purpose for both the "GET" and "POST" methods.
The function name will match, so that will be "edit_category".
To start with, we will only focus on the "GET" method, which will get the template, and render it on screen for us.
We can simply return render_template using the new file we created, "edit_category.html".

```python
# routes.py
@app.route("/edit_category", methods=["GET", "POST"])
def edit_category():
    return render_template("edit_category.html")
```

However, we need some sort of mechanism for the app to know which specific category we intend to update.
In order to understand this, let's open the template for all categories, which contains
the for-loop we built in the last video.
If you recall, within this for-loop, we have the variable of '`category`' that is used for
each iteration of this loop, and we have targeted the 'category_name' field.
Due to the fact that our 'Edit' and 'Delete' buttons are still within the for-loop, we
can use that variable to identify the specific category primary key using '.id'.
Let's go ahead and create the href url_for() method, which will be wrapped in double curly-brackets.
This behaves in the same way that we called the navbar links, or the CSS and JavaScript
files from within our static directory.
In addition to calling our new 'edit_category' function, we need to pass another argument
to specify which particular category we are attempting to update.
Make sure you add a comma after the single-quotes, which identifies that we are calling the function with some data included.
For the argument name, it can be whatever we'd like, and since we need to use something
unique, it's best to use the primary key of the ID.
I'm going to call this 'category_id', and we can now set that equal to the current 'category.id' using dot-notation again.
Since we originally added the 'Travel' category as the first record on our database, its ID will be '1'.

```html
<!-- categories.html-->
        <div class="card-action">
          <a href="{{ url_for('edit_category', category_id=category.id) }}" class="btn green accent-4">Edit</a> 
          <a href="#" class="btn red ">Delete</a>
        </div>
```

Now, we can head back over to the `routes.py` file, and since we've given an argument of
'`category_id`' when clicking the 'Edit' button, this also needs to appear in our app.route.
These types of variables being passed back into our Python functions must be wrapped
inside of angle-brackets within the URL.
We know that all of our primary keys will be integers, so we can cast this as an 'int'.
We also need to pass the variable directly into the function as well, so we have the
value available to use within this function.

```python
# routes.py
@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    return render_template("edit_category.html")

```

---
**NOTE**

If you have attempted to save these changes and load the page, then you're going to get an error.
This is a very common error, and something that all developers should know how to understand,
so let's save everything, and load the live preview.
Once that's loaded, navigate to the Categories page, and then hover over any of the 'Edit'
buttons for some of the categories we've created.
If you notice in the bottom-left corner, you can see that the href for the 'Travel' card
shows our new function of '/edit_category', and then the number '1'.
You can do this same thing, by using the Developer Tools and inspect the Edit button in the DOM.
Jinja has converted the url_for() method into an actual href, and injected the respective
ID into the argument we added of 'category_id'.
It's the same for any of these cards, each with their own ID applied.
However, try clicking on one of the Edit buttons, and you'll notice the Werkzeug Error.
"Could not build url endpoint 'edit_category'. Did you forget to specify values ['category_id']?"
The really fantastic thing with any Flask error, is that it will always tell you exactly
which file and line number is causing the specific error.
Normally, this can be found towards the bottom of the error lines, and you want to look for
the code in the blue rows that matches your own code.
As you can see here, we're calling the URL for the edit_category function, which is listed
on the edit_category.html template, from line 7.
Essentially what happened is once we added the primary key of ID into our app.route function,
it will now always expect this for any link that calls this function.

---

Let's go back to the edit_category template, and sure enough on line 7 we have the url_for method.
All we need to do is provide the same exact argument of 'category_id' like we did on the href for the Edit button.
Again, separate the argument with a comma after the single-quotes, and the variable
name we assigned was 'category_id'.
This will be set to 'category.id' as well for the value.

```html
<!-- edit_category.html -->
<div class="row card-panel grey lighten-5">
    <form class="col s12" method="POST" action="{{ url_for('edit_category', category_id=category.id) }}">

```

Even though we added this to the URL now and saved the file, you will still get an error
saying "'category' is undefined".
You might be wondering where this 'category' value comes from, since this isn't part of
a for-loop like on the categories template.
That's the next step, so go ahead and return to your routes.py file.
In order for this function to know which specific category to load, we need to attempt to find
one in the database using the ID provided from the URL.
The template is expecting a variable 'category', so let's create that new variable now.
Using the imported Category model from the top of the file, we need to query the database,
and this time we know a specific record we'd like to retrieve.
There's a SQLAlchemy method called '.get_or_404()', which takes the argument of 'category_id'.
What this does is query the database and attempts to find the specified record using the data
provided, and if no match is found, it will trigger a 404 error page.
Now, we can pass that variable into the rendered template, which is expecting it to be called
'category', and that will be set to the defined 'category' variable above.

```python
# routes.py
@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template("edit_category.html", category=category)
```

The page should load now without any errors, however, if you notice, it doesn't show us
the current value of our category, and the form doesn't do anything just yet.
Within the edit_category template, now that we have the category retrieved from the database,
we need to add its value into the input field.
This is a variable, so we need to wrap it inside of double curly-brackets, and then
we can target the 'category_name' from this variable of 'category' using dot-notation again.
If you save those changes, and then reload the page and click on any of the Edit buttons
now, it should pre-fill the form with the existing value from our database.

```html
<!-- edit_category.html -->
    <input id="category_name" name="category_name" value="{{ category.category_name }}" type="text" class="validate" minlength="3" maxlength="25"
        required>
```

The final step now, is to add the "POST" functionality so the database actually gets updated with the requested changes.
Back within our routes.py file, just after the 'category' variable being defined, let's
conditionally check if the requested method is equal to "POST".
If so, then we want to update the category_name for our category variable, and we'll set that
to equal the form's name-attribute of 'category_name'.
After that, we need to commit the session over to our database.
Finally, if that's all successful, we should redirect the users back to the categories
function, which will display all of them in the cards once again.

```python
# routes.py
@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)
```

## Delete Category

The final CRUD method is to give users the ability to Delete records, which is what we will cover in this video.
In order to allow users to delete a record from the database, we actually don't need to create a new template.
The entire functionality is done from within our back-end function on the routes.py file, so let's open that file.
This will be a brand new function, so let's create a new app.route and call it "/delete_category".
As is tradition by now, our function name will take the same name, "delete_category".
In the same exact way that we specified which category we wanted to edit from our last video, we need to do the same thing here.
This function needs to know which particular category we would like to delete from the data base.
Let's actually copy a few things from the 'edit' function above.
First, we need to pass the category ID into our app route and function, and once again,
we are casting it as an integer.
Next, we should attempt to query the Category table using this ID, and store it inside of a variable called 'category'.
If there isn't a matching record found, then it should automatically return an error 404 page.
Then, using the database session, we need to perform the .delete() method using that
'category' variable, and then commit the session changes.
Finally, once that's been deleted and our session has been committed, we can simply
redirect the user back to the function above called "categories".

```python
@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))
```

The only thing that's left to do now, is to update our href link from the categories template.
The pattern is identical to the Edit button, so as a challenge, I want you to pause the
video here, and see if you can figure this out yourself.
Hopefully you've managed that on your own, but if not, all we need to do is simply copy
the Edit button href, and then paste it into the href for the delete button.
The only difference though, is that we need to update the function name to "delete_category".
As you can see, since we are within the for-loop of all categories, it's using the current
iteration variable of 'category', and then targeting the key of 'id' from that record.
The 'category_id' assigned is just the variable name we're passing into the app.route function
that we just created within the routes.py file.

```html
<a href="{{ url_for('delete_category', category_id=category.id) }}" class="btn red ">Delete</a>
```

---
**NOTE**

The first thing you should remember, is that once the delete button is clicked, then it
will completely delete the record from the database for good.
This is considered bad practice, since there isn't any form of defensive programming in place.
Ideally, you should include some sort of blocking mechanism that first has the user confirm
whether or not they'd actually like to delete the record.
A common method for this would be to use a modal for example.
Instead of calling the 'delete_category' function within the href, what it should do is to trigger the modal to open up.
Within this modal, you'll have some message to the user to confirm their action of deleting the record.
If they definitely want to delete the record, then the button within the modal would be
the actual href to call the delete function.
Also, something to note when using modals, is that they generally have a custom ID attached
to them in order to open the modal on screen.
You can see from the Materialize documentation here, the href to call the modal uses the
same ID name to launch the actual modal.
If you use this method within your Jinja for-loop of all categories, then it will only work
for the very first category, and the other modals will not open.
This is because IDs should always be unique, one per page.
The trick around that, is to use something unique within the for-loop to identify the
appropriate modal being generated per category.
We already know that each category has a unique primary key, so we can simply have each modal
being generated within this for-loop to utilize that primary key as well.
The example here would be to call the ID "modal-{{category.id}}" so each modal generated would be transpiled
to the HTML as modal-1, modal-2, modal-3, and so on.

---

---
**NOTE**

The other important thing to make note of on your projects, is considering user authentication.
In an ideal world, you wouldn't want just any random stranger to be able to edit and delete your database records.
You would normally only show these edit and delete buttons if the owner of those categories was the one viewing the page.
For example, if Bob added the Category of "Travel", and Bob is currently logged in to
his profile, then only Bob should be able to see these buttons.
That way, any guest other than Bob, such as Mary, would be able to see all categories,
but not have access to manipulate that data on the database.
This is why user authentication can be something to consider later, and there are several ways
to accomplish that on a project.
Now that I've mentioned both defensive programming and user authentication, it's finally time
to go ahead and delete one of these categories.
For this demonstration, I'm going to delete the category that we updated in the last video.

---

## Add Task

Go ahead and update the text to be "Add Task", and then update the function to match, "add_task".
This will also be the same URL that we apply to the navbar link, so open the base.html template.
Copy any of the existing url_for() methods from an existing href, and paste it into the link for 'New Task'.
Let's update that function to match the other file, which was "add_task", making sure to
also copy and paste that below into the sidenav as well.
Now, let's open up the routes.py file, and create this function that will render a new
template for users to add a new Task.
It's actually quite similar to the 'add_category' function, so let's just copy the entire function,
and paste it as a brand new one at the bottom of the file.
Then, we can start updating the app route and function name to "add_task" instead of category.
If you recall from the video where we designed our database schema, each task actually requires
the user to select a category for that task.
In order to do that, we first need to extract a list of all of the categories available from the database.
We've previously done this on the 'categories' function, so go ahead and copy that line above,
and paste it before the POST method.
This time, however, we aren't going to be inserting a new category into the database, but rather a new task.
From our models.py file, each task must have a few different elements, including a task
name, description, due date, category, and whether or not it's urgent.
That means we need to update the POST method to reflect each of the fields that will be
added from the form that we will create shortly.
Make sure to separate each field with a comma at the end of the line, to signify the end of that particular field.
Task name will be set to the form's name attribute of 'task_name'.
Task description will use the form's 'task_description' field
The 'is_urgent' field will be a Boolean, either true or false, so we'll make it True if the
form data is toggled on, otherwise it will be set to False by default.
Due date will of course be the form's 'due_date' input box.
Then finally, the last column for each Task will be the selected Category ID, which will
be generated as a dropdown list to choose from, using the 'categories' list above.
Once the form is submitted, we can add that new 'task' variable to the database session,
and then immediately commit those changes to the database.
If successful, then we can redirect the user back to the 'home' page where each task will eventually be displayed.
That concludes the POST functionality when users add a new Task to the database.
If, however, the method isn't POST, and a user is trying to add a new task, they need
to be displayed with the page that contains the form.
This should render the template for "add_task.html", and in order for the dropdown list to display
each available category, we need to pass that variable into the template.
As a reminder, the first 'categories' listed is the variable name that we will be able
to use on the template itself.
The second 'categories' is simply the list of categories retrieved from the database defined above.
That's all we need for the 'add_task' function, which will render the template for new tasks,
and then commit those new tasks to the database if the form is submitted.

```python
# routes.py
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            category_id=request.form.get("category_id")
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html", categories=categories)
```



The next field will be the 'due_date' of the task, so let's copy the entire row once again for the task name.
This time, however, instead of having users put a minimum or maximum value, we are going
to use another one of the Materialize helper classes called 'datepicker'.
Even though this is a standard input field, by using the 'datepicker' helper class, we
need to also initialize the datepicker using JavaScript.
From the Materialize documentation, let's copy the code snippet for the datepicker and
paste it into our custom JavaScript file.
I'm going to call this variable 'datepickers', and we can initialize that variable with some additional options.
Back on the Materialize site, you can see that they've got several options to include on the datepicker.
Let's keep this simple, so we are only going to include a few custom options.
First, we need to make sure that all tasks have a consistent date format, which uses the 'format' key.
For this project, I'm going to specify the date format of "dd mmmm, yyyy", which would
be for example, "01 February, 2024".
If you wanted, you could also include other options, such as the 'yearRange' to only show
3 years at a time, or the 'showClearBtn' as 'true'.
For demonstration purposes, I will also include the 'i18n' option, which itself will contain
a dictionary of elements.
The 'i18n' is the nickname given for 'internationalization' since there are 18 letters in the middle of
that word, starting with I and ending with N.
It allows programmers to customize text when dealing with foreign languages, if you want
the datepicker element to be translated into Gaelic or Klingon for example.
In this case, I'd like to change the text on the 'Done' button, instead of showing 'OK',
I want it to show 'Select'.
Using the list provided, you can change any of these, such as the months, dates, days of the week, etc.

```html
<!-- add_task.html -->
<!-- due_date -->
<div class="row">
    <div class="input-field col s12">
        <i class="fas fa-calendar-alt prefix light-blue-text text-darken-4"></i>
        <input id="due_date" name="due_date" type="text" class="datepicker validate" 
            required>
        <label for="due_date">Due Date</label>
    </div>
</div>
```

```js
// script.js
document.addEventListener('DOMContentLoaded', function() {
    // // sidenav initialization
    // let sidenav = document.querySelectorAll('.sidenav');
    // M.Sidenav.init(sidenav);

    // datepicker initialization
    let datepicker = document.querySelectorAll('.datepicker');
    M.Datepicker.init(datepicker, {
      format: "dd mmmm, yyyy",
      i18n: {done: "Select"}
    });
  });
```

The final field will be for our dropdown list to select the category applicable to this task.
Back within the Materialize docs, navigate to the 'Select' page for forms, and we're
only going to focus on the basic dropdown element at the top.
You'll notice that it's similar to a standard select element, nothing too fancy here, so
I'm going to copy the task_name one more time, and adjust the required elements.
This will be for 'category_id', so we can adjust that throughout this row, and update the icon if desired.
Since this will be a select element, I'll update that to be select, making sure to include
the closing /select tag as well, and removing the min, max, and type attributes.
For the category options, we'll start with a basic option that is disabled and selected
by default, which reads 'Choose Category' displayed to the users.
Then, we need to create a Jinja for-loop over the list of all categories that are being
retrieved from the database.
{% for category in categories %} making sure to also include the {% endfor %} block.
For each category in this loop, we need to create a new 'option' in the dropdown.
The value for each option will be the category's unique ID, but obviously the ID won't make
much sense to our users, so we'll use the 'category.category_name' for display purposes.
If you recall, whenever submitting a form to the back-end, Python uses the name="" attribute
to grab the data being stored within the database.
For select elements, the actual data being stored is the value of the selected option,
which will be the category ID, whether it's 1, 2, 3, 4, and so on.
```html
        <!-- category_id -->
        <div class="row">
            <div class="input-field col s12">
                <i class="fas fa-folder-open prefix light-blue-text text-darken-4"></i>
                <select name="category_id" id="category_id" class="validate" required>
                    <option value="" disabled selected>Choose Category</option>
                    {% for category in categories %}
                        <option value="{{ category.id }}">{{ category.category_name }}</option>
                    {% endfor %}
                </select>
                <label for="category_id">Task Name</label>
            </div>
        </div>
```
The final step we need to do for the dropdown to work, is to initialize it via JavaScript,
and that's because Materialize has a custom design for the select elements.
Copy the initialization code from their documentation, and paste it within your JavaScript file.
I'm going to call this variable 'selects' for any select element found, and then initialize those below.
```js
// script.js
document.addEventListener('DOMContentLoaded', function() {
//     // sidenav initialization
//     let sidenav = document.querySelectorAll('.sidenav');
//     M.Sidenav.init(sidenav);

//     // datepicker initialization
//     let datepicker = document.querySelectorAll('.datepicker');
//     M.Datepicker.init(datepicker, {
//       format: "dd mmmm, yyyy",
//       i18n: {done: "Select"}
//     });

    // select initialization
    let selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);
  });
```

## Viewing Tasks

If you recall, we opted for a specific date format when selecting a date from the datepicker,
but you may have noticed that it's not displaying properly on our list.
The templating engine we're using called Jinja actually comes with a helpful method of '.strftime()'
which stands for "string from time".
This is a Python directive that you can use within your Python files as well, and allows
you to format dates and times to your preference.
To see a full list of format options, visit strftime.org, which can be found in the link below this video.
In our case, the format we opted for was Date Month, comma, Year, so that would be the format
of "%d %B, %Y", making sure to be careful with case-sensitivity.
Another thing we could add, is the Jinja filter of "|sort()" which will allow us to sort our tasks.
You can find a link below this video for a list of the built-in Jinja filters.
Clicking on "sort", you can see a few ways to use this, including the parameter of "attribute"
using dot-notation from our database.
Let's go ahead and use the sort filter on our for-loop, and for the attribute, we'll
have it sort by the "due_date" column.

(Built In Jinja Filters)[https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters]
(strftime.org)[https://strftime.org/]

Another thing we could add, is the Jinja filter of "|sort()" which will allow us to sort our tasks.
You can find a link below this video for a list of the built-in Jinja filters.
Clicking on "sort", you can see a few ways to use this, including the parameter of "attribute"
using dot-notation from our database.
Let's go ahead and use the sort filter on our for-loop, and for the attribute, we'll
have it sort by the "due_date" column.


```html
<!-- tasks.html -->
<ul class="collapsible">
    <!-- THIS ONE -->
    {% for task in tasks|sort(attribute="due_date") %}
    <li>
      <div class="collapsible-header white-text light-blue darken-4">
        <i class="fas fa-caret-down"></i>
        <!-- THIS ONE BELLOW TOO-->
        <strong>{{ task.task_name }}</strong> : {{ task.due_date.strftime("%d %B, %Y") }} 
        {% if task.is_urgent == True %}
        <i class="fas fa-exclamation-circle light-blue-text text-lighten-2"></i>
        {% endif %}
    </div>
      <div class="collapsible-body">
        <strong>{{ task.category }}</strong>
        <p>{{ task.task_description }}</p>
      </div>
    </li>
    {% endfor %}
  </ul>
  ```

The final thing to mention on this video, is converting your database queries into actual Python lists.
Whenever you query the database, you actually get something returned called a Cursor Object,
sometimes called a QuerySet.
In some cases, you can't use a Cursor Object on the front-end, or with some of the Jinja template filters.
Oftentimes, it's actually better to convert your queries into Python lists.
Let's navigate to our routes.py file, and since we want this to occur only for queries
that have more than one result, let's find any that end with '.all()'.
As you can see, we've been doing this already, which is considered best practice, wrapping any query in a Python list().

```python
# Example
@app.route("/")
def home():
    tasks = list(Task.query.order_by(Task.id).all())
    return render_template("tasks.html", tasks=tasks)
```

## Edit Task

The easiest way to generate a form that allows users to update data, is to make a copy of
the original form which creates a new task.
Right-click the add_task.html file, click on 'Copy', then right-click on the 'templates'
directory, and finally, select 'Paste' to make a duplicate copy.
Rename the file to edit_task.html, and now we can start updating the text to read 'Edit Task' within the file itself.
In order to render the template, we need to create a new function inside of the routes.py file.
Let's copy the entire function for adding a new task, and paste it below, giving it a unique name of 'edit_task'.
The function needs to know which particular task we would like to edit, so we should include
the task's ID in the app root URL, which is cast as an integer.
Don't forget, we also need to pass that into the function itself as 'task_id'.
If you recall from when we created the edit_category function, we used the 'get_or_404()' method,
which queries the database using that task ID.
Now, instead of using the Task model, we can simply update each column-header using dot-notation.
We already have each field here, so we just need to adjust the formatting for Python to
remove the original Task() model, and give it proper indentation.
Do this for each field, adding 'task dot' in front of each column-header, such as 'task.task_name', or 'task.due_date'.
It's important to do this for all fields, even if the user would only like to update one of them.
If we don't include all fields, and the user only updates the task_name for example, then
the other fields risk being deleted entirely.
Since we are modifying the specific task here, we don't need to use session.add(), and only
session.commit() is required for saving these changes.
Finally, we just need to render our new template of 'edit_task.html', and along with the normal
'categories' selection, we need to pass through the task itself.

```python
# routes.py
@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = bool(True if request.form.get("is_urgent") else False)
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")
        db.session.commit()
    return render_template("edit_task.html", task=task, categories=categories)
```

Next, open up the tasks.html template, because we need a method for users to click a button
that opens up this template for editing.
Within the 'collapsible-body' element, just underneath the task-description paragraph,
let's add another paragraph tag.
This one will contain a link, styled like a button, in exactly the same way we created the Edit button for each category.
I'm going to copy that one from the categories.html template, and paste it within the paragraph tag here.
Make sure to update any reference to 'category', so that it calls the appropriate function for editing our task instead.
Copy the entire href, and then go back to the new 'edit_task' template, where we can
then paste that into the form's action attribute.
That way, once we've updated any field on the task, it will know which specific task
to update within our database.

If you notice, the URL here is pointing to the new function of 'edit_task', and it's
recognizing the primary key of 'task.id' which will be updated on the database.
However, it's not very intuitive right now, because all of the fields are blank, instead
of showing us the existing values stored for this task.
Let's go back to the 'edit_task' template, and start adding the existing values into their respective fields.
For the task name, the value-attribute will simply point to the current 'task.task_name'.
For the task description, since this is a 
, we need to add the existing value
between the opening and closing textarea tags.
The due date is another input field, so we can use the value-attribute of 'task.due_date',
however, we need to convert the date into a string to match our date format.
To keep things consistent, just copy the date string from the tasks.html template, and paste
it within the value, making sure to fix any single or double quotes as needed.
Unfortunately, the final two fields aren't as simple as adding the value-attribute.
For the 'is_urgent' toggle, we need to conditionally check to see if it's set to True, and if so, add the 'checked' attribute.
Duplicate the input line by pressing "Shift + Alt + Down" on Windows, or "Shift + Option + Down" on Mac.
One should be checked if it's True, so let's add some Jinja logic here.
If task.is_urgent is True, then add this checked input field, otherwise, within the 'else' block, show the normal input field.
Remember to close the {% endif %} block.
For the 'category' selection, our current for-loop is building anfor each category in our database.
Similar to the 'is_urgent' toggle, we need to conditionally check to see if the current
iteration of categories matches the actual task category that we are updating.
Again, duplicate this line, and if there is a match, then it should be the one with the 'selected' attribute.
If the current category is equal to the actual task.category, we will have that be 'selected'.
Otherwise, display the normalfield within the {% else %} block, making sure to close the {% endif %} block.
That should be everything now sorted, so let's save the changes, and reload the live preview page.
Select any of your tasks by clicking on the Edit button, and as you can see, all of the
existing details about this task are now pre-populated into our form.

`check taks.html for the code itself`

---
**NOTE**

The only issue we have now, is that the textarea for our task-description has a lot of whitespace
before and after the actual content.
Let's quickly go back to the file, and find the textarea.
**Jinja has several helper elements, and one of them is specifically designed for whitespace control.
If we include a minus-symbol at the beginning and end of this variable, it will remove any whitespace.
Alternatively, if you wanted to add whitespace, you would apply a plus-symbol only at the
beginning of the variable, not the end.**

---

