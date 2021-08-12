from flask import Flask,flash,redirect,render_template,url_for
from flask_blog.forms import RegistrationForm,LoginForm
from flask_blog.models import User,Post
from flask_blog import app

posts = [
      
    {
        'author': 'Corey Schafer',
        'title': 'First Post',
        'content':'This is my first post',
        'date_posted': 'June 20, 2021',
    
    },

    {
        'author': 'Wilfred Bonny',
        'title': 'Second Post',
        'content':'This is my second post',
        'date_posted': 'June 25, 2021',
    
    },

]

@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html',posts = posts)


@app.route("/about")
def about():
     return render_template('about.html',title ="About")


@app.route("/register",methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.username.data}','success')
        return redirect(url_for('home'))
    return render_template('register.html',title ="Register",form = form)


@app.route("/login",methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == "12345678":
            flash('You have been logged in succeessfully','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check username and password!','danger')
    return render_template('login.html',title ="Login",form = form)