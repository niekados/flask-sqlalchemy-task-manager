from taskmanager import db

class Category(db.Model):
    # schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        # there is another function that behaves simillar - def __str__(self):
        return self.category_name



class Task(db.Model):
    # schema for the Task model
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False) # db.ForeignKey("category.id") - points to class Category(db.Model):

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "{0} - Task: {1} | Urgent: {2}".format(
            self.id, self.task_name, self.is_urgent
        )