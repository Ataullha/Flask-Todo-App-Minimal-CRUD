
# for importing flask, render_template. request and redirect features from flask module
from flask import Flask, render_template, request, redirect
# for importing database functionality 
from flask_sqlalchemy import SQLAlchemy
# for importing datetime
from datetime import datetime

# name for our app
app = Flask(__name__)

# for sqlite in alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
# name of the database
db = SQLAlchemy(app)

# creating database class
class Todo(db.Model):
    # for serial no
    sno = db.Column(db.Integer, primary_key=True)
    # for title
    title = db.Column(db.String(200), nullable=False)
    # for description
    desc = db.Column(db.String(500), nullable=False)
    # for date created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# for viewing the element in the object
    def __repr__(self) -> str:
        # just show them when we call a object
        return f"{self.sno} - {self.title}"

# for get and post request in the / means index.html route
@app.route("/", methods=['GET', 'POST'])
# function in the route to execute
def hello_world():
    # if the request method is post
    if request.method == 'POST':
        # print(request.form['title'])
        title = request.form['title']
        # print(request.form['description'])
        desc = request.form['description']
        # initalize todo object and intialize with the form value from the index.html page
        todo = Todo(title=title, desc=desc)
        # have to do for add the todo in the database
        db.session.add(todo)
        # commit the database changes
        db.session.commit()

    # inserting data in the database
    # todo = Todo(title='First Todo', desc='First Description')
    # db.session.add(todo)
    # db.session.commit()

# for query all the elements from the database
    allTodo = Todo.query.all()
    print(allTodo)

    # for rendering html in app
    # for rendering them in the index.html page with the allTodo= allTodo variable
    return render_template('index.html', allTodo=allTodo)
    # return render_template('index.html')
    # return "<p>Hello, World!</p>"

# just a demo 
@app.route("/show")
def products():
    # read everything from the database
    allTodo = Todo.query.all()
    print(allTodo)
    # return "<p>This is a product page</p>"

# for update option get the serial number route
@app.route("/update/<int:sno>", methods=['GET', 'POST'])
# update function
def update(sno):
    # as before 
    if request.method == 'POST':
        # initalize title and desc.
        title = request.form['title']
        desc = request.form['description']
        # call the Todo object woth the serial number we get from the route
        todo = Todo.query.filter_by(sno=sno).first()
        # assign those previously assinded value after the button from the update.html is clicked 
        todo.title = title
        todo.desc = desc
        # todo things
        db.session.add(todo)
        db.session.commit()
        # redirect to the main page
        return redirect("/")
        # get all the info and render them to the html page to show the user
    todo = Todo.query.filter_by(sno=sno).first()
    # return it which we set in the update.html form using value = "{{todo.title}}" type of things
    return render_template('update.html', todo=todo)


# same as the update
@app.route("/delete/<int:sno>")
# get the delete function for the speicific serial no
def delete(sno):
    # for reading the first element with that specific serial number from the database
    todo = Todo.query.filter_by(sno=sno).first()
    # delete and commit
    db.session.delete(todo)
    db.session.commit()
    # for redicting to the index.html or / page
    return redirect('/')
    # print(allTodo)
    # return "<p>This is a product page</p>"

# app name 
if __name__ == "__main__":
    # debug option True, and running on the 5000 port
    app.run(debug=True, port=5000)


'''
flask shell
from app import db
db.create_all()

https://inloop.github.io/sqlite-viewer/
https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/

pip install virtualenv
virtualenv env
source/env/bin/activate

pip installv gunicorn
pip freeze > requirements.txt

'''
