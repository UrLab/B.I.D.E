from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
def my_form():
    co = sqlite3.connect("users.db")
    c = co.cursor()

    users = []
    i = 1
    for vals in c.execute("SELECT * FROM users ORDER BY points DESC"):
        users.append(((vals[0], vals[1]), i))
        i += 1

    co.close()

    return render_template("index.html", users=users)


@app.route("/jokes")
def jokes():
    co = sqlite3.connect("users.db")
    c = co.cursor()

    i = 1
    jokes = []
    for vals in c.execute("SELECT * FROM jokes ORDER BY points DESC"):
        jokes.append(((vals[0], vals[1], vals[2]), i))
        i += 1

    # Save (commit) the changes
    co.close()

    return render_template("jokes.html", jokes=jokes)


@app.route("/adduser", methods=["POST"])
def insert_user():
    username = request.form.get("Name")
    if username == "":
        return redirect("/", code=302)

    # Connecting to the database and inserting the username
    co = sqlite3.connect("users.db")
    c = co.cursor()
    c.execute("INSERT INTO users VALUES (?, 0)", (username,))
    co.commit()
    co.close()

    return redirect("/", code=302)


@app.route("/addjoke", methods=["POST"])
def insert_joke():
    joke = request.form.get("Joke")
    if joke == "":
        return redirect("/", code=302)

    co = sqlite3.connect("users.db")
    c = co.cursor()

    pk = int(c.execute("SELECT MAX(pk) FROM jokes").fetchall()[0][0])
    c.execute("INSERT INTO jokes VALUES (?, 0, ?)", (joke, pk + 1))

    co.commit()
    co.close()

    return redirect("/jokes", code=302)


@app.route("/vote", methods=["GET"])
def vote_joke():
    joke_pk = request.args.get("joke")
    action = request.args.get("action")
    if joke_pk == "":
        return redirect("/jokes", code=302)

    co = sqlite3.connect("users.db")
    c = co.cursor()

    base_points = c.execute("SELECT points FROM jokes WHERE pk=?", (joke_pk,))
    if action == "plus":
        points = int(base_points.fetchall()[0][0] + 1)
    elif action == "moins":
        points = int(base_points.fetchall()[0][0] - 1)
    else:
        c.close()
        return redirect("/jokes", code=302)

    c.execute("UPDATE jokes SET points=? WHERE pk=?", (points, joke_pk))

    co.commit()
    co.close()

    return redirect("/jokes", code=302)


@app.route("/ModPoints", methods=["GET"])
def addPoints():
    user = request.args.get("user")
    action = request.args.get("action")

    co = sqlite3.connect("users.db")
    c = co.cursor()

    base_points = c.execute("SELECT points FROM users WHERE username=?", (user,))

    if action == "plus":
        base_points = base_points.fetchall()[0][0] + 1
    elif action == "moins":
        base_points = base_points.fetchall()[0][0] - 1
    else:
        co.close()
        return redirect("/", code=302)

    c.execute("UPDATE users SET points=? where username=?", (base_points, user))
    co.commit()
    co.close()

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
