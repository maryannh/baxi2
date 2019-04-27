from flask import Flask, render_template
from flask_simplelogin import SimpleLogin, is_logged_in, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
app.config['SIMPLELOGIN_USERNAME'] = 'chuck'
app.config['SIMPLELOGIN_PASSWORD'] = 'norris'

SimpleLogin(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard/<user>')
@login_required
def dashboard():
    return render_template('dashboard.html', user=user)

@app.route('/settings/<user>')
@login_required
def settings():
    return render_template('settings.html', user=user)

@app.route('/add_content/<user>')
@login_required
def add_content():
    return render_template('add_content.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')