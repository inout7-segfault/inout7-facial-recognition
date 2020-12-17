from flask_bootstrap import Bootstrap
import numpy as np
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from database import add_attendance
import datetime
from flask_sqlalchemy import SQLAlchemy
from predict import find_student
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired,Email,Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETISTHATPRAHASITHISTHEBEST'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/prahasith/Desktop/inout7-facial-recognition/database.db'
Bootstrap(app)
db = SQLAlchemy(app)

slot = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(80))

class LoginForm(FlaskForm):
    username = StringField('username',validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password',validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password',validators=[InputRequired(), Length(min=8, max=80)])

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/capture")
def capture():
    return render_template("capture.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return redirect(url_for('dashboard'))
        return '<h1>Invalid Username or password</h1>'
    
    return render_template("login.html",form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
    return render_template("signup.html", form=form)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    global slot
    if request.method == "POST":
        image = request.files["image"]

        # course = request.files["course"]
        # slot = request.files["slot"]
        course = "CS510"
        slot+=1
        image = Image.open(image)

        student_details = find_student(np.array(image))

        add_attendance(student_id=student_details["Roll_num"],date = datetime.date.today(),course=course,slot=slot)

        print(f"present : {student_details['Name']} with acc : {student_details['accuracy']}")

    return render_template("upload.html")


if __name__ == "__main__":
    from livereload import Server

    server = Server(app.wsgi_app)
    server.serve(port=5000)
