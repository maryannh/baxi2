from flask import Flask, render_template, redirect, session, flash, request
from pymongo import MongoClient
from forms import JoinForm, LoginForm, ContentForm, SettingsForm
from werkzeug.security import check_password_hash, generate_password_hash 
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')

client = MongoClient(app.config.get('MONGO_URI'))
db = client.dandelion

mail = Mail(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join', methods=['GET', 'POST'])
def join(): 
    form = JoinForm()
    if request.method == 'POST':
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
                'added': datetime.utcnow(),
            }
            db.users.insert_one(info)
            # add info to session
            session["email"] = email
            session["username"] = username
            session["learner_name"] = learner_name
            # flash message
            flash('You have successfully registered and logged in')
            return redirect('/dashboard')
        else:
            # add what happens if it doesn't validate
            for item in form.errors.items():
                print(item)
    return render_template('join.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" not in session:
        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                # get form data
                password = form.password.data
                username = form.username.data
                user_info = db.users.find_one({"username": username})
                # check password
                hashed_password = user_info["password"]
                if check_password_hash(hashed_password, password):
                    # add user to session and redirect to dashboard
                    session['username'] = username
                    flash('You have successfully logged in')
                    return redirect("/dashboard")
                else:
                    # add what happens if passwords don't match
                    flash('Please check your password and try again')
                    for item in form.errors.items():
                        print(item)
                    return redirect("/login")
    else:
        return redirect('/dashboard')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    username = session['username']
    # add what happens if a user ends up here with no username in their session
    if username == None:
        return redirect("/login")
    return render_template('dashboard.html', username=username)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # get form data
            test = form.test.data
            # add to db
            info = { "settings": {
                'test': test,
            }
            }
            db.users.update_one({
                "username": session['username']
            }, {
                "$set": info
            })
            # return to add content page
            flash("Settings updated")
            return redirect("/dashboard")
    return render_template('settings.html', form=form)

@app.route('/add_content', methods=['GET', 'POST'])
def add_content():
    form = ContentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # get form data
            title = form.title.data
            content = form.content.data
            category = form.category.data
            # add to db
            info = {
                'title': title,
                'content': content,
                'category': category,
                'added': datetime.utcnow(),
                'user': session['username'],
            }
            db.content.insert_one(info)
            # return to add content page
            message = '"' + title + '" added successfully'
            flash(message)
            return redirect("/add_content")
    return render_template('add_content.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')