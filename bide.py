from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/')
def my_form():
    co = sqlite3.connect('users.db')
    c = co.cursor()

    users = []
    for vals in c.execute('SELECT * FROM users ORDER BY points'):
        users.append((vals[0], vals[1]))

    co.close()

    return render_template('index.html', users=users)


@app.route('/jokes')
def jokes():
    co = sqlite3.connect('users.db')

    # c = co.cursor()

    # Save (commit) the changes
    co.close()

    return render_template('jokes.html')


@app.route("/adduser")
def add_user():
    return render_template('adduser.html')


@app.route("/adduser", methods=['POST'])
def insert_user():
    username = request.form.get("Name")
    print(type(username))

    # Connecting to the database and inserting the username
    co = sqlite3.connect("users.db")
    c = co.cursor()
    c.execute("INSERT INTO users VALUES (?, 0)", (username,))
    co.commit()
    co.close()

    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
