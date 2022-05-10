from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)

## users is gonna be the name of the table that we will reference to
## Config for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///users.db'

# Secret Key
app.config['SECRET_KEY'] = 'ruankey'

# Initialize the database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route("/")
def index():
    cars = ['volvo', 'toyota', 'hyundai']
    return render_template("index.html",
                           cars = cars)

# localhost:5000/user/Ruan
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", usr_name=name)

# Page not found function
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

# Create a Form class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/view")
def view():
    return render_template("view.html")

# Create name page
@app.route("/name", methods=["GET", "POST"])
def name():
    ## The form shows name, but when the page first loads, there is no name
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted successfully")

    return render_template("name.html",
                           name = name,
                           form = form)

