from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task

@app.route("/")
def home():
    return render_template("tasks.html")

# Whenever you use the url_for() method on your links, it's important to note that these are
# calling the actual Python functions ( def categories(): ), not the app.route ( @app.route("/categories") ), 
# even though these are often the same name.


@app.route("/categories")
def categories():
    return render_template("categories.html")

# we used GET and POST methods, as we will be submitting form to database
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")
