from flask import Flask, render_template
from flask_simplelogin import SimpleLogin, is_logged_in, login_required
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
app.config['SIMPLELOGIN_USERNAME'] = 'chuck'
app.config['SIMPLELOGIN_PASSWORD'] = 'norris'


client = MongoClient("mongodb+srv://maryann:3j69q28gzRCbJxwo@cluster1-pdojm.mongodb.net/test?retryWrites=true")
db = client.dandelion

SimpleLogin(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/dashboard/<user>')
@login_required
def dashboard(user):
    return render_template('dashboard.html', user=user)

@app.route('/settings/<user>')
@login_required
def settings(user):
    return render_template('settings.html', user=user)

@app.route('/add_content/<user>')
@login_required
def add_content(user):
    return render_template('add_content.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')