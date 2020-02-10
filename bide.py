from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/')
def my_form():
    co = sqlite3.connect('users.db')
    c = co.cursor()

    users = []
    i = 1
    for vals in c.execute('SELECT * FROM users ORDER BY points DESC'):
        users.append(((vals[0], vals[1]), i))
        i += 1

    co.close()

    return render_template('index.html', users=users)


@app.route('/jokes')
def jokes():
    co = sqlite3.connect('users.db')
    c = co.cursor()

    # Save (commit) the changes
    co.close()

    return render_template('jokes.html')


@app.route("/adduser", methods=['POST'])
def insert_user():
    username = request.form.get("Name")
    if username == "":
        return redirect("/", code=302)
    print(type(username))

    # Connecting to the database and inserting the username
    co = sqlite3.connect("users.db")
    c = co.cursor()
    c.execute("INSERT INTO users VALUES (?, 0)", (username,))
    co.commit()
    co.close()

    return redirect("/", code=302)


@app.route("/ModPoints", methods=['GET'])
def addPoints():
    user = request.args.get('user')
    action = request.args.get('action')

    co = sqlite3.connect("users.db")
    c = co.cursor()

    base_points = c.execute("SELECT points FROM users WHERE nom=?", (user,))

    if action == "plus":
        base_points = base_points.fetchall()[0][0]+1
    elif action == "moins":
        base_points = base_points.fetchall()[0][0]-1
    else:
        co.close()
        return redirect("/", code=302)

    c.execute(
        "UPDATE users SET points=? where nom=?", (base_points, user))
    co.commit()
    co.close()

    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
