from flask import Flask, render_template, redirect, session, flash
from flask_simplelogin import SimpleLogin, is_logged_in, login_required
from pymongo import MongoClient
from forms import JoinForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'

client = MongoClient("mongodb+srv://maryann:3j69q28gzRCbJxwo@cluster1-pdojm.mongodb.net/test?retryWrites=true")
db = client.dandelion

SimpleLogin(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join', methods=('GET', 'POST'))
def join(): 
    form = JoinForm()
    if form.validate_on_submit():
        # get form data
        username = form.username.data
        learner_name = form.learner_name.data
        email = form.email.data
        hashed_password = generate_password_hash(form.password.data)
        # add form data to database
        info = {
            "username": username,
            "password": hashed_password,
            "email": email,
            "learner_name": learner_name,
        }
        user_id = db.users.insert_one(info).inserted_id
        session["username"] = form.username.data
        print(session["username"])
        return redirect('/dashboard/')
    else:
        # add what happens if it doesn't validate
        for item in form.errors.items():
            print(item)
    return render_template('join.html', form=form)

@app.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # get form data
        # check password
        password = form.password.data
        username = form.username.data
        user_info = db.users.find_one({"username": username})
        hashed_password = user_info["password"]
        if check_password_hash(password, hashed_password):
            # add user to session and redirect to dashboard
            session['username'] = username
            flash('You have successfully logged in')
            return redirect("/dashboard/")
        else:
            # add what happens if passwords don't match
            flash('Please check your password and try again')
            return redirect("/login/")
    else:
        # add what happens if it doesn't validate
    return render_template('login.html')

@app.route('/dashboard/')
def dashboard():
    username = session['username']
    # add what happens if a user ends up here with no username in their session
    if username == None:
        return redirect("/login/")
    return render_template('dashboard.html', username=username)

@app.route('/settings/')
def settings():
    return render_template('settings.html')

@app.route('/add_content/')
def add_content():
    return render_template('add_content.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')