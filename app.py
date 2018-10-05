from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy

#CREATE DATABASE pythonflask
#the next two commands are in the terminal
#import db from app
#db.create_all()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I<3ECE1779'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/pythonflask?charset=utf8mb4'
Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    username = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = 'tianyue').first()
        if user:
            if user.password ==form.password.data:
                return redirect(url_for('test'))

        return 'Invalid User or Password'


    return render_template("login.html", form=form)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("signup.html", form = form)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/test')
def test():
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True)
