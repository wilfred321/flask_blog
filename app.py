from logging import DEBUG
from flask import Flask,flash,redirect
from flask import render_template
from flask.helpers import url_for
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = '63f4ce6948a9d40a72191bb94b9c23fb'

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
            flash('You have been Logged in Succeessfully','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check username and password!','danger')
    return render_template('login.html',title ="Login",form = form)

if __name__ == '__main__':
    app.run(debug=True)