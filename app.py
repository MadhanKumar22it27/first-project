from flask import Flask, request, render_template, redirect, url_for, session,g
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secret key for your application
app.config['DATABASE'] = 'userdata.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['txt']
        email = request.form['email']
        password = request.form['psed']

        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO userdata (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        db.commit()
        c.close()
        return 'Signed up successfully!'

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pswd']

        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM userdata WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        c.close()

        if user:
            session['username'] = user[0]  # Store the username in the session
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid email or password. Please try again.'

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
