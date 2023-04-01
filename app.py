from flask import Flask, render_template, url_for, request,redirect,flash
from flask_wtf import FlaskForm  # Import FlaskForm from Flask-WTF
from wtforms import StringField, PasswordField, SubmitField # Import form fields from WTForms
from wtforms.validators import DataRequired, Email, EqualTo  # Import validators from WTForms
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy from Flask-SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)  # Create a new Flask app instance
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Set the secret key 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:joeis97%TDH@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Set the database URI

db = SQLAlchemy(app)  # Create an instance of SQLAlchemy with the app




# Define a new class for the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username
    

   
# Define a new class for the registration form
class RegistrationForm(FlaskForm):
    # Define form fields and validators
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Define a new class for the login form 
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


# Define routes for the app
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # User is authenticated, redirect to home page
           return f'You are in, {form.username.data}!'
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return f'Thank you for registering, {form.username.data}!'
    return render_template('register.html', form=form)

# @app.route('/loggedin')
# def loggedin():
#     form = LoginForm(r)
#     return render_template('loggedin.html',
#                            form=form)

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
