from flask import render_template, request, redirect, url_for, session, Flask
from models import insert_user, get_user
import sqlite3

app = Flask(__name__)
app.secret_key = "1234567890"


@app.route('/')
def home():
    return render_template('home.html', session=session)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/info_table')
def info_table():
    username = session.get('username')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchall()
    print(user)
    conn.close()
    return render_template('user_info.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        anime = request.form['anime']
        film = request.form['movie']

        if insert_user(username, password, anime, film):
            return redirect(url_for('login'))
        else:
            return "This username is already taken! Please choose another one."

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username, password)

        if user:
            session['username'] = username
            return redirect(url_for('info_table'))
        else:
            return "Invalid username or password. Please try again."

    return render_template('login.html')
