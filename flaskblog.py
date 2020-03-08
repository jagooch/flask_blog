from flask import Flask
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
# import sqlite3
from pprint import pprint
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

# with sqlite3.connect("posts.db") as conn:
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#     cursor.execute("select * from posts")
#     posts = [ dict(row) for row in cursor.fetchall()]

# pprint(posts)

# Create flask app
app = Flask(__name__)
#set app config
app.config['SECRET_KEY'] = '894f16ed082df645715f80256549fef5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 

#Create database 
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship( 'Post', backref='author', lazy=True ) # define relationship with posts

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}' )"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    content = db.Column(db.Text, nullable=False )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False  ) #id of the user author

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')

@app.route("/register", methods=[ 'GET', 'POST'  ])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect( url_for('home') ) 
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=[ 'GET', 'POST'])
def login():  
    form = LoginForm()
    if form.validate_on_submit():  
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect( url_for('home') ) 
        else:
            flash(f'Login Failed. Check u/p.', 'danger')
    return render_template('login.html', title='Login', form=form)



if __name__ == "__main__":
    app.run(debug=True)